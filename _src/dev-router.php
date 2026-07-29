<?php
// Local preview router: execute PHP endpoints and never serve private dotfiles.
$path = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/';
if (preg_match('~/(?:\.|_src/)~', $path)) {
    http_response_code(404);
    exit;
}
return false;
