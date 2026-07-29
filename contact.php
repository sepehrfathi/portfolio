<?php
/**
 * Secure contact endpoint for sep.onwebs.ir.
 *
 * Delivers through authenticated SMTP over TLS. Credentials are loaded from
 * server environment variables first and fall back to .smtp-config.php, whose
 * direct web access is denied by .htaccess.
 */

declare(strict_types=1);

const SITE_NAME = 'sep.onwebs.ir';
const MAX_PER_HOUR = 8;

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

function fail(int $code, string $message): never {
    http_response_code($code);
    echo json_encode(['ok' => false, 'error' => $message], JSON_UNESCAPED_UNICODE);
    exit;
}

function config_value(array $fileConfig, string $envName, string $key, mixed $default = ''): mixed {
    $env = getenv($envName);
    return ($env !== false && $env !== '') ? $env : ($fileConfig[$key] ?? $default);
}

function smtp_config(): array {
    $configPath = __DIR__ . '/.smtp-config.php';
    $fileConfig = is_readable($configPath) ? (array) require $configPath : [];
    return [
        'host' => (string) config_value($fileConfig, 'SMTP_HOST', 'host'),
        'port' => (int) config_value($fileConfig, 'SMTP_PORT', 'port', 465),
        'encryption' => strtolower((string) config_value($fileConfig, 'SMTP_ENCRYPTION', 'encryption', 'ssl')),
        'username' => (string) config_value($fileConfig, 'SMTP_USERNAME', 'username'),
        'password' => (string) config_value($fileConfig, 'SMTP_PASSWORD', 'password'),
        'from_email' => (string) config_value($fileConfig, 'SMTP_FROM_EMAIL', 'from_email'),
        'from_name' => (string) config_value($fileConfig, 'SMTP_FROM_NAME', 'from_name', SITE_NAME),
        'to_email' => (string) config_value($fileConfig, 'CONTACT_TO_EMAIL', 'to_email', 'ftsepi@gmail.com'),
    ];
}

function smtp_read($socket): array {
    $response = '';
    while (($line = fgets($socket, 2048)) !== false) {
        $response .= $line;
        if (strlen($line) >= 4 && $line[3] === ' ') {
            break;
        }
    }
    if ($response === '') {
        throw new RuntimeException('smtp_no_response');
    }
    return [(int) substr($response, 0, 3), $response];
}

function smtp_expect($socket, array $allowed): string {
    [$code, $response] = smtp_read($socket);
    if (!in_array($code, $allowed, true)) {
        throw new RuntimeException('smtp_response_' . $code);
    }
    return $response;
}

function smtp_command($socket, string $command, array $allowed): string {
    if (fwrite($socket, $command . "\r\n") === false) {
        throw new RuntimeException('smtp_write_failed');
    }
    return smtp_expect($socket, $allowed);
}

function encoded_header(string $value): string {
    return '=?UTF-8?B?' . base64_encode($value) . '?=';
}

function smtp_send(array $config, string $replyName, string $replyEmail, string $subject, string $body): void {
    foreach (['host', 'username', 'password', 'from_email', 'to_email'] as $required) {
        if ($config[$required] === '') {
            throw new RuntimeException('smtp_config_missing');
        }
    }

    $scheme = $config['encryption'] === 'ssl' ? 'ssl://' : 'tcp://';
    $ssl = [
        'verify_peer' => true,
        'verify_peer_name' => true,
        'allow_self_signed' => false,
        'peer_name' => $config['host'],
        'SNI_enabled' => true,
    ];
    $context = stream_context_create(['ssl' => $ssl]);
    $errno = 0;
    $error = '';
    $socket = @stream_socket_client(
        $scheme . $config['host'] . ':' . $config['port'],
        $errno,
        $error,
        15,
        STREAM_CLIENT_CONNECT,
        $context
    );
    if (!is_resource($socket)) {
        throw new RuntimeException('smtp_connect_failed');
    }

    stream_set_timeout($socket, 15);
    try {
        smtp_expect($socket, [220]);
        $helo = preg_replace('/[^a-z0-9.-]/i', '', (string) ($_SERVER['SERVER_NAME'] ?? SITE_NAME)) ?: SITE_NAME;
        smtp_command($socket, 'EHLO ' . $helo, [250]);

        if ($config['encryption'] === 'tls') {
            smtp_command($socket, 'STARTTLS', [220]);
            if (!stream_socket_enable_crypto($socket, true, STREAM_CRYPTO_METHOD_TLS_CLIENT)) {
                throw new RuntimeException('smtp_tls_failed');
            }
            smtp_command($socket, 'EHLO ' . $helo, [250]);
        }

        smtp_command($socket, 'AUTH LOGIN', [334]);
        smtp_command($socket, base64_encode($config['username']), [334]);
        smtp_command($socket, base64_encode($config['password']), [235]);
        smtp_command($socket, 'MAIL FROM:<' . $config['from_email'] . '>', [250]);
        smtp_command($socket, 'RCPT TO:<' . $config['to_email'] . '>', [250, 251]);
        smtp_command($socket, 'DATA', [354]);

        $headers = [
            'Date: ' . date(DATE_RFC2822),
            'From: ' . encoded_header($config['from_name']) . ' <' . $config['from_email'] . '>',
            'To: <' . $config['to_email'] . '>',
            'Reply-To: ' . encoded_header($replyName) . ' <' . $replyEmail . '>',
            'Subject: ' . encoded_header($subject),
            'Message-ID: <' . bin2hex(random_bytes(12)) . '@' . SITE_NAME . '>',
            'MIME-Version: 1.0',
            'Content-Type: text/plain; charset=UTF-8',
            'Content-Transfer-Encoding: 8bit',
            'X-Mailer: onwebs-contact-smtp',
        ];
        $normalizedBody = preg_replace("/\r\n|\r|\n/", "\r\n", $body);
        $payload = implode("\r\n", $headers) . "\r\n\r\n" . $normalizedBody;
        $payload = preg_replace('/(?m)^\./', '..', $payload);
        if (fwrite($socket, $payload . "\r\n.\r\n") === false) {
            throw new RuntimeException('smtp_data_failed');
        }
        smtp_expect($socket, [250]);
        smtp_command($socket, 'QUIT', [221]);
    } finally {
        fclose($socket);
    }
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    fail(405, 'method_not_allowed');
}

$origin = (string) ($_SERVER['HTTP_ORIGIN'] ?? '');
if ($origin !== '') {
    $originHost = strtolower((string) parse_url($origin, PHP_URL_HOST));
    $siteHost = strtolower((string) ($_SERVER['HTTP_HOST'] ?? SITE_NAME));
    $siteHost = preg_replace('/:\d+$/', '', $siteHost);
    if ($originHost !== '' && !in_array($originHost, [$siteHost, 'sep.onwebs.ir', '127.0.0.1', 'localhost'], true)) {
        fail(403, 'origin_not_allowed');
    }
}

// Honeypot: a real visitor never fills this hidden field.
if (trim((string) ($_POST['company'] ?? '')) !== '') {
    echo json_encode(['ok' => true], JSON_UNESCAPED_UNICODE);
    exit;
}

$name = trim((string) ($_POST['name'] ?? ''));
$email = trim((string) ($_POST['email'] ?? ''));
$message = trim((string) ($_POST['message'] ?? ''));

if ($name === '' || $email === '' || $message === '') {
    fail(422, 'missing_fields');
}
if (mb_strlen($name) > 120 || mb_strlen($email) > 190 || mb_strlen($message) > 5000) {
    fail(422, 'too_long');
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    fail(422, 'bad_email');
}
if (preg_match('/[\r\n]/', $name . $email)) {
    fail(422, 'bad_input');
}

// File-based per-IP rate limiting: no database required.
$ip = (string) ($_SERVER['REMOTE_ADDR'] ?? '0.0.0.0');
$rateDir = sys_get_temp_dir() . '/onwebs-contact';
@mkdir($rateDir, 0700, true);
$bucket = $rateDir . '/' . sha1($ip) . '.txt';
$now = time();
$hits = [];
if (is_readable($bucket)) {
    $hits = array_filter(
        array_map('intval', explode(',', (string) file_get_contents($bucket))),
        static fn(int $time): bool => $time > $now - 3600
    );
}
if (count($hits) >= MAX_PER_HOUR) {
    fail(429, 'rate_limited');
}
$hits[] = $now;
@file_put_contents($bucket, implode(',', $hits), LOCK_EX);

$subject = '[' . SITE_NAME . '] ' . $name;
$body = "پیام جدید از فرم تماس " . SITE_NAME . "\n"
    . "New message from the " . SITE_NAME . " contact form\n\n"
    . "نام / Name: " . $name . "\n"
    . "ایمیل / Email: " . $email . "\n"
    . "IP: " . $ip . "\n"
    . "زمان / Time: " . gmdate('Y-m-d H:i:s') . " UTC\n"
    . str_repeat('-', 48) . "\n\n"
    . $message . "\n";

try {
    smtp_send(smtp_config(), $name, $email, $subject, $body);
} catch (Throwable $exception) {
    // Preserve the message without recording SMTP credentials or internals.
    @file_put_contents(
        __DIR__ . '/.contact-fallback.log',
        "==== " . gmdate('c') . " ====\n" . $body . "\n",
        FILE_APPEND | LOCK_EX
    );
    error_log('Contact SMTP delivery failed: ' . $exception->getMessage());
    fail(502, 'send_failed');
}

echo json_encode(['ok' => true], JSON_UNESCAPED_UNICODE);
