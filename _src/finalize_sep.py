# -*- coding: utf-8 -*-
"""Apply Sepehr Fathi's final copy, prompt-engineering section and metadata."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
LANGS = ("fa", "en", "ar", "zh", "ru", "es", "no")
DOMAIN = "https://sep.onwebs.ir"

SPARK = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5'
    'M15.5 15.5 18 18M18 6l-2.5 2.5M8.5 15.5 6 18"/></svg>'
)
QUOTE = (
    '<svg viewBox="0 0 24 24" fill="currentColor" stroke="none">'
    '<path d="M7 7h5v6a4 4 0 0 1-4 4H7v-2h1a2 2 0 0 0 2-2v-1H7V7Z'
    'm8 0h5v6a4 4 0 0 1-4 4h-1v-2h1a2 2 0 0 0 2-2v-1h-3V7Z"/></svg>'
)
STAR = (
    '<span class="star"><svg viewBox="0 0 24 24" fill="currentColor" stroke="none">'
    '<path d="m12 2 2.6 6.3L21 9l-5 4.3L17.5 20 12 16.3 6.5 20 '
    '8 13.3 3 9l6.4-.7L12 2Z"/></svg></span>'
)

PROMPT = {
    "fa": {
        "eyebrow": "تخصص",
        "title": "مهندسی پرامپت و سامانه‌های هوش مصنوعی",
        "lead": (
            "مهندسی پرامپت را صرفاً نوشتن چند دستور نمی‌دانم؛ آن را طراحی لایهٔ تعامل میان مدل، "
            "داده و نرم‌افزار می‌بینم. این لایه باید رفتار مدل را قابل‌اندازه‌گیری، قابل‌کنترل و "
            "قابل‌نگهداری کند تا هوش مصنوعی بخشی مطمئن از یک محصول واقعی باشد."
        ),
        "cards": [
            ("معماری دستور و زمینه", "نقش مدل، هدف، محدودیت‌ها، مثال‌ها و اولویت منابع را صریح تعریف می‌کنم و فقط زمینهٔ مرتبط را وارد می‌کنم تا مدل از مسئله منحرف نشود."),
            ("خروجی ساخت‌یافته", "برای ارتباط مطمئن با نرم‌افزار از Structured Outputs و JSON Schema استفاده می‌کنم؛ خروجی اعتبارسنجی می‌شود و برای خطا، تلاش مجدد و مسیر جایگزین دارد."),
            ("ابزارها و گردش‌کار عامل‌محور", "فراخوانی ابزار و تابع با دسترسی حداقلی، ثبت رویداد و تأیید عملیات حساس طراحی می‌شود؛ مدل پیشنهاد و هماهنگی می‌کند و کد، قواعد قطعی را اجرا می‌کند."),
            ("اتصال به دانش معتبر", "با RAG، بازیابی هدفمند، ذکر منبع و کنترل تازگی داده، پاسخ‌ها به شواهد قابل‌بررسی متصل می‌شوند؛ نبود اطلاعات نیز به‌صورت صریح اعلام می‌شود."),
            ("ارزیابی و نسخه‌بندی", "پرامپت، مدل و تنظیمات مانند کد نسخه‌بندی می‌شوند. مجموعه‌دادهٔ ارزیابی، موارد مرزی و آزمون رگرسیون، کیفیت، هزینه و زمان پاسخ را پیش از انتشار می‌سنجند."),
            ("ایمنی و مقاوم‌سازی", "در برابر Prompt Injection، افشای داده و استفادهٔ خارج از دامنه لایه‌های دفاعی می‌گذارم و در تصمیم‌های حساس، بازبینی انسانی و توقف ایمن را حفظ می‌کنم."),
        ],
        "note": "هدف، تولید یک پاسخ چشمگیر نیست؛ ساخت رفتاری پایدار، قابل‌سنجش و مسئولانه در مقیاس واقعی است.",
        "skill": "مهندسی پرامپت و سامانه‌های هوش مصنوعی",
        "items": ["System / Developer Prompts", "معماری Context", "Structured Outputs و JSON Schema", "Tool / Function Calling", "RAG و Grounding", "Evals و آزمون رگرسیون", "Prompt Injection و Guardrails", "پایش هزینه و زمان پاسخ"],
    },
    "en": {
        "eyebrow": "Specialism",
        "title": "Prompt & AI Systems Engineering",
        "lead": (
            "I treat prompt engineering as the design of the interaction layer between models, data and "
            "software—not as writing a clever instruction. That layer must make model behaviour measurable, "
            "controllable and maintainable before AI can become a dependable part of a real product."
        ),
        "cards": [
            ("Instruction & context architecture", "I define the model's role, objective, constraints, examples and source priorities explicitly, then supply only the context relevant to the task."),
            ("Structured outputs", "Structured Outputs and JSON Schema turn model responses into reliable software contracts, backed by validation, retries and explicit fallback paths."),
            ("Tools & agentic workflows", "Tool and function calls use least privilege, auditable traces and confirmation for sensitive actions; the model coordinates while deterministic code enforces rules."),
            ("Grounded knowledge", "RAG, targeted retrieval, citations and freshness checks connect answers to verifiable evidence and make missing information explicit."),
            ("Evaluation & versioning", "Prompts, models and settings are versioned like code. Golden datasets, edge cases and regression tests measure quality, latency and cost before release."),
            ("Safety & resilience", "I design defences against prompt injection, data leakage and out-of-scope use, with human review and safe stopping points for consequential decisions."),
        ],
        "note": "The goal is not one impressive answer; it is stable, measurable and responsible behaviour at production scale.",
        "skill": "Prompt & AI Systems Engineering",
        "items": ["System / developer prompts", "Context architecture", "Structured Outputs & JSON Schema", "Tool / function calling", "RAG & grounding", "Evals & regression testing", "Prompt-injection defence", "Cost & latency observability"],
    },
    "ar": {
        "eyebrow": "تخصص",
        "title": "هندسة الأوامر وأنظمة الذكاء الاصطناعي",
        "lead": "أتعامل مع هندسة الأوامر بوصفها تصميم طبقة التفاعل بين النموذج والبيانات والبرمجيات، لا مجرد كتابة تعليمات ذكية. يجب أن تجعل هذه الطبقة سلوك النموذج قابلاً للقياس والتحكم والصيانة قبل اعتماده داخل منتج حقيقي.",
        "cards": [
            ("بنية التعليمات والسياق", "أحدّد الدور والهدف والقيود والأمثلة وأولوية المصادر بوضوح، وأمرّر إلى النموذج السياق المرتبط بالمهمة فقط."),
            ("مخرجات منظّمة", "أستخدم Structured Outputs وJSON Schema كعقد برمجي موثوق، مع التحقق وإعادة المحاولة ومسارات بديلة واضحة عند الخطأ."),
            ("الأدوات ومسارات الوكلاء", "تعمل استدعاءات الأدوات والصوالحيات وفق الحد الأدنى من الصلاحيات، مع سجل قابل للتدقيق وتأكيد للعمليات الحساسة."),
            ("معرفة موثّقة", "يربط RAG والاسترجاع المستهدف والاستشهاد بالمصادر وفحص حداثة البيانات كل إجابة بأدلة قابلة للتحقق."),
            ("التقييم وإدارة الإصدارات", "تُدار الأوامر والنماذج والإعدادات كالكود، وتُقاس الجودة والزمن والتكلفة ببيانات تقييم واختبارات حدود وانحدار."),
            ("السلامة والمرونة", "أصمّم دفاعات ضد حقن الأوامر وتسريب البيانات والاستخدام خارج النطاق، مع مراجعة بشرية للقرارات الحساسة."),
        ],
        "note": "الهدف ليس إجابة مبهرة واحدة، بل سلوك ثابت وقابل للقياس ومسؤول على مستوى الإنتاج.",
        "skill": "هندسة الأوامر وأنظمة الذكاء الاصطناعي",
        "items": ["System / Developer Prompts", "بنية السياق", "Structured Outputs وJSON Schema", "استدعاء الأدوات والدوال", "RAG والتأسيس بالمصادر", "التقييم واختبارات الانحدار", "مقاومة حقن الأوامر", "مراقبة التكلفة والزمن"],
    },
    "zh": {
        "eyebrow": "专业方向",
        "title": "提示工程与 AI 系统工程",
        "lead": "我把提示工程视为模型、数据与软件之间交互层的设计，而不是编写一句巧妙指令。只有当这一层让模型行为可度量、可控制、可维护时，AI 才能成为真实产品中可靠的组成部分。",
        "cards": [
            ("指令与上下文架构", "明确模型角色、目标、约束、示例与信息源优先级，只提供与当前任务相关的上下文。"),
            ("结构化输出", "使用 Structured Outputs 与 JSON Schema 建立可靠的软件契约，并配套验证、重试和明确的降级路径。"),
            ("工具与智能体工作流", "工具调用遵循最小权限，保留可审计轨迹，敏感操作需要确认；模型负责协调，确定性代码负责执行规则。"),
            ("有依据的知识", "通过 RAG、定向检索、来源引用与时效检查，把回答连接到可验证证据，并明确表达信息缺失。"),
            ("评估与版本管理", "像管理代码一样管理提示、模型和参数；用黄金数据集、边界案例和回归测试衡量质量、延迟与成本。"),
            ("安全与韧性", "针对提示注入、数据泄露和越界使用设计防护，并为高影响决策保留人工复核与安全停止点。"),
        ],
        "note": "目标不是得到一次惊艳回答，而是在生产规模下实现稳定、可度量且负责任的行为。",
        "skill": "提示工程与 AI 系统工程",
        "items": ["系统与开发者提示", "上下文架构", "Structured Outputs 与 JSON Schema", "工具与函数调用", "RAG 与依据化", "评估与回归测试", "提示注入防护", "成本与延迟监控"],
    },
    "ru": {
        "eyebrow": "Специализация",
        "title": "Промпт-инжиниринг и AI-системы",
        "lead": "Я рассматриваю промпт-инжиниринг как проектирование слоя взаимодействия между моделью, данными и программным обеспечением, а не как написание удачной инструкции. Этот слой должен делать поведение модели измеримым, управляемым и сопровождаемым.",
        "cards": [
            ("Архитектура инструкций и контекста", "Я явно задаю роль, цель, ограничения, примеры и приоритет источников, передавая модели только релевантный контекст."),
            ("Структурированный вывод", "Structured Outputs и JSON Schema создают надёжный программный контракт с валидацией, повторами и явными резервными сценариями."),
            ("Инструменты и агентные процессы", "Вызовы инструментов работают с минимальными правами, аудитом и подтверждением чувствительных действий; правила исполняет детерминированный код."),
            ("Знания с опорой на источники", "RAG, целевой поиск, ссылки и проверка актуальности связывают ответы с проверяемыми данными и явно показывают пробелы."),
            ("Оценка и версионирование", "Промпты, модели и настройки версионируются как код; эталонные наборы, граничные случаи и регрессионные тесты измеряют качество, задержку и стоимость."),
            ("Безопасность и устойчивость", "Я проектирую защиту от prompt injection, утечек данных и выхода за рамки задачи, сохраняя человеческую проверку для значимых решений."),
        ],
        "note": "Цель — не один эффектный ответ, а стабильное, измеримое и ответственное поведение в промышленной эксплуатации.",
        "skill": "Промпт-инжиниринг и AI-системы",
        "items": ["System / developer prompts", "Архитектура контекста", "Structured Outputs и JSON Schema", "Tool / function calling", "RAG и grounding", "Evals и регрессионные тесты", "Защита от prompt injection", "Мониторинг стоимости и задержки"],
    },
    "es": {
        "eyebrow": "Especialidad",
        "title": "Ingeniería de prompts y sistemas de IA",
        "lead": "Entiendo la ingeniería de prompts como el diseño de la capa de interacción entre modelos, datos y software, no como la redacción de una instrucción ingeniosa. Esa capa debe volver el comportamiento del modelo medible, controlable y mantenible.",
        "cards": [
            ("Arquitectura de instrucciones y contexto", "Defino explícitamente el rol, objetivo, restricciones, ejemplos y prioridad de fuentes, aportando solo el contexto relevante para la tarea."),
            ("Salidas estructuradas", "Structured Outputs y JSON Schema crean contratos de software fiables, con validación, reintentos y rutas de respaldo explícitas."),
            ("Herramientas y flujos agénticos", "Las llamadas a herramientas aplican privilegio mínimo, trazabilidad y confirmación para acciones sensibles; el código determinista hace cumplir las reglas."),
            ("Conocimiento fundamentado", "RAG, recuperación dirigida, citas y controles de vigencia conectan las respuestas con evidencia verificable y hacen explícita la información ausente."),
            ("Evaluación y versionado", "Prompts, modelos y ajustes se versionan como código; conjuntos de referencia, casos límite y pruebas de regresión miden calidad, latencia y coste."),
            ("Seguridad y resiliencia", "Diseño defensas ante inyección de prompts, fuga de datos y uso fuera de alcance, con revisión humana para decisiones de impacto."),
        ],
        "note": "El objetivo no es una respuesta espectacular, sino un comportamiento estable, medible y responsable a escala de producción.",
        "skill": "Ingeniería de prompts y sistemas de IA",
        "items": ["System / developer prompts", "Arquitectura de contexto", "Structured Outputs y JSON Schema", "Tool / function calling", "RAG y grounding", "Evals y pruebas de regresión", "Defensa ante prompt injection", "Observabilidad de coste y latencia"],
    },
    "no": {
        "eyebrow": "Spesialfelt",
        "title": "Prompt- og AI-systemutvikling",
        "lead": "Jeg behandler promptutvikling som design av samhandlingslaget mellom modeller, data og programvare – ikke som formuleringen av én smart instruksjon. Laget må gjøre modellatferd målbar, styrbar og vedlikeholdbar.",
        "cards": [
            ("Instruksjons- og kontekstarkitektur", "Jeg definerer rolle, mål, begrensninger, eksempler og kildeprioritet tydelig, og gir modellen bare kontekst som er relevant for oppgaven."),
            ("Strukturerte utdata", "Structured Outputs og JSON Schema gir pålitelige programvarekontrakter med validering, nye forsøk og eksplisitte reserveveier."),
            ("Verktøy og agentbaserte arbeidsflyter", "Verktøykall bruker minste privilegium, sporbarhet og bekreftelse for sensitive handlinger; deterministisk kode håndhever reglene."),
            ("Kildebasert kunnskap", "RAG, målrettet henting, kildehenvisninger og ferskhetskontroll knytter svar til etterprøvbare bevis og synliggjør manglende informasjon."),
            ("Evaluering og versjonering", "Prompter, modeller og innstillinger versjoneres som kode; referansedatasett, grensetilfeller og regresjonstester måler kvalitet, svartid og kostnad."),
            ("Sikkerhet og robusthet", "Jeg bygger forsvar mot prompt injection, datalekkasje og bruk utenfor formålet, med menneskelig kontroll ved viktige beslutninger."),
        ],
        "note": "Målet er ikke ett imponerende svar, men stabil, målbar og ansvarlig atferd i produksjon.",
        "skill": "Prompt- og AI-systemutvikling",
        "items": ["System- og developer-prompter", "Kontekstarkitektur", "Structured Outputs og JSON Schema", "Tool / function calling", "RAG og grounding", "Evals og regresjonstesting", "Forsvar mot prompt injection", "Måling av kostnad og svartid"],
    },
}


COPY_REPLACEMENTS = {
    "fa": {
        "نرم‌افزاری می‌سازم که واقعاً کار می‌کند — از اپلیکیشن‌های کراس‌پلتفرم با Flutter تا سامانه‌های هوش مصنوعی و بینایی ماشین — و یک اختراع از خودم دارم: دستگاه تصفیهٔ آب با حباب نانو.": "در تقاطع مهندسی نرم‌افزار، هوش مصنوعی و توسعهٔ محصول کار می‌کنم؛ از اپلیکیشن‌های چندسکویی و سامانه‌های سازمانی تا بینایی ماشین، تحلیل داده و فناوری تصفیهٔ آب مبتنی بر نانوحباب.",
        "مهندس نرم‌افزار، مخترع و بنیان‌گذارم؛ سامانه‌هایی می‌سازم که واقعاً کار می‌کنند — نه نمونهٔ نمایشی.": "مهندس نرم‌افزار، مخترع و بنیان‌گذارم و تمرکزم بر تبدیل مسئله‌های پیچیده به محصولات قابل‌اعتماد، قابل‌توسعه و قابل‌استفاده است.",
        "من سپهر فتحی هستم. از سال ۱۴۰۰ به‌صورت تخصصی روی نرم‌افزار کار می‌کنم — اپلیکیشن‌های کراس‌پلتفرم با Flutter، PWA، پنل‌های مدیریتی و سوپراپ‌های شهروندی شهرداری‌ها (از جمله بردسکن)، و همچنین وب و بک‌اند. شرکت «ویرا وب آریا» را بنیان گذاشتم و اکنون رئیس هیئت‌مدیرهٔ آن هستم.": "من سپهر فتحی هستم. از سال ۱۴۰۰ به‌صورت حرفه‌ای در توسعهٔ نرم‌افزار فعالیت می‌کنم؛ از اپلیکیشن‌های چندسکویی Flutter و PWA تا پنل‌های مدیریتی، سامانه‌های تحت وب و سوپراپ‌های خدمات شهروندی. «ویرا وب آریا» را بنیان گذاشتم و اکنون به‌عنوان رئیس هیئت‌مدیره، در راهبری محصول و مسیر فنی آن نقش دارم.",
        "من سپهر فتحی هستم. از سال ۱۴۰۰ به‌صورت حرفه‌ای در توسعهٔ نرم‌افزار فعالیت می‌کنم؛ از اپلیکیشن‌های چندسکویی Flutter و PWA تا پنل‌های مدیریتی، سامانه‌های تحت وب و سوپراپ‌های خدمات شهروندی. «ویرا وب آریا» را بنیان گذاشتم و اکنون به‌عنوان رئیس هیئت‌مدیره، در راهبری محصول و مسیر فنی آن نقش دارم.": "من سپهر فتحی هستم. از سال ۱۴۰۰ به‌صورت حرفه‌ای در توسعهٔ نرم‌افزار فعالیت می‌کنم؛ از اپلیکیشن‌های چندسکویی Flutter و PWA تا پنل‌های مدیریتی و سامانه‌های تحت وب. برنامه‌نویس ارشد سوپراپلیکیشن شهروندی بردسکن برای Android و Web هستم و «ویرا وب آریا» را بنیان گذاشته‌ام؛ اکنون نیز به‌عنوان رئیس هیئت‌مدیره در راهبری محصول و مسیر فنی آن نقش دارم.",
        "امروز هم‌بنیان‌گذار چند استارتاپ (شناسنامه خودرو، اپ مصرف، اوانوبت)، مدیرعامل نانو حباب روشنا و مخترع دستگاه تصفیهٔ آب با حباب نانو، و برنامه‌نویس ارشد شرکت‌های نروژی Cuatro و NanoMAR هستم. در کنار این‌ها سامانه‌های هوش مصنوعی و بینایی ماشین می‌سازم — یک یابندهٔ خودروی آفلاین بر پایهٔ پلاک، یک پلتفرم ارزیابی ریسک ملک برای بیمه‌گران نروژی، و یک موتور بیوانفورماتیک برای شناسایی هدف CAR-T.": "در کنار فعالیت‌های کارآفرینانه در شناسنامه خودرو، اپ مصرف و اوانوبت، مدیرعامل نانو حباب روشنا و مخترع یک سامانهٔ تصفیهٔ آب مبتنی بر نانوحباب هستم. همچنین به‌عنوان مهندس نرم‌افزار ارشد با Cuatro و NanoMAR در نروژ همکاری می‌کنم و روی راهکارهای هوش مصنوعی، بینایی ماشین، تحلیل ریسک مکانی و بیوانفورماتیک کار می‌کنم.",
        "یک ایدهٔ محصول، سامانهٔ هوش مصنوعی‌ای که باید درست کار کند، یا یک همکاری دیپ‌تک — دوست دارم دربارهٔ آن بشنوم.": "برای توسعهٔ محصول، طراحی سامانه‌های هوش مصنوعی یا همکاری‌های پژوهشی و دیپ‌تک، می‌توانید مستقیماً با من در ارتباط باشید.",
    },
    "en": {
        "I build software that actually works — from cross-platform Flutter apps to AI and computer-vision systems — and I hold an invention of my own: a nano-bubble water purifier.": "I work at the intersection of software engineering, applied AI and product development—from cross-platform applications and enterprise systems to computer vision, data analysis and nano-bubble water-treatment technology.",
        "I'm a software engineer, inventor and founder who ships real, working systems — not demos.": "I am a software engineer, inventor and founder focused on turning complex problems into dependable, maintainable products.",
        "I'm Sepehr Fathi. Since 2021 I've worked professionally on software — cross-platform Flutter apps, PWAs, municipal admin panels and citizen super-apps (Bardaskan and others), plus web and backend. I founded Vira Web Aria and today serve as its chairman of the board.": "I am Sepehr Fathi. Since 2021 I have worked professionally across software engineering: cross-platform Flutter applications, PWAs, administrative platforms, web systems and municipal citizen services. I founded Vira Web Aria and now contribute to its product and technical direction as chairman.",
        "I am Sepehr Fathi. Since 2021 I have worked professionally across software engineering: cross-platform Flutter applications, PWAs, administrative platforms, web systems and municipal citizen services. I founded Vira Web Aria and now contribute to its product and technical direction as chairman.": "I am Sepehr Fathi. Since 2021 I have worked professionally across software engineering: cross-platform Flutter applications, PWAs, administrative platforms and web systems. I am the senior developer of the Bardaskan citizen super app for Android and the web, and I founded Vira Web Aria, where I now guide product and technical direction as chairman.",
        "Today I'm a co-founder of several startups (Shenasnameh Khodro, Masraf, AvaNobat), CEO of Nano Hobab Roshana and the inventor of its nano-bubble water purifier, and a senior engineer for the Norwegian companies Cuatro and NanoMAR. Alongside that I build AI and computer-vision systems — an offline Iranian license-plate car-finder, a property-risk platform for Norwegian insurers, and a bioinformatics engine for CAR-T target discovery.": "Alongside entrepreneurial work with Shenasnameh Khodro, Masraf and AvaNobat, I am CEO of Nano Hobab Roshana and inventor of a nano-bubble water-treatment system. I also work as a senior software engineer with Cuatro and NanoMAR in Norway, developing applied-AI, computer-vision, geospatial-risk and bioinformatics systems.",
        "A product idea, an AI system that has to be correct, or a deep-tech collaboration — I'd like to hear about it.": "For product development, applied-AI systems or research and deep-tech collaboration, you are welcome to contact me directly.",
    },
}

SEO = {
    "fa": {
        "title": "سپهر فتحی | رزومه مهندس نرم‌افزار، هوش مصنوعی و مخترع",
        "description": "رزومه و نمونه‌کارهای سپهر فتحی (Sepehr Fathi)، مهندس نرم‌افزار، مخترع و برنامه‌نویس ارشد سوپراپلیکیشن شهروندی بردسکن؛ فعال در Flutter، هوش مصنوعی و توسعهٔ محصول.",
        "keywords": "سپهر فتحی, سپهر, Sepehr Fathi, Sepehr, Sepehr Fatehi, رزومه سپهر فتحی, رزومه شخصی سپهر فتحی, نمونه کار سپهر فتحی, پورتفولیو سپهر فتحی, سپهر فتحی بردسکن, سپهر بردسکن, بردسکن, اپ بردسکن, اپلیکیشن بردسکن, سوپر اپ بردسکن, سوپراپلیکیشن شهروندی بردسکن, برنامه نویس ارشد بردسکن, شهرداری بردسکن, app.bardaskan.ir, مهندس نرم افزار, برنامه نویس, توسعه دهنده فول استک, مهندس هوش مصنوعی, مهندسی پرامپت, بینایی ماشین, Flutter, Python, FastAPI, React, مخترع, بنیان گذار, مشهد",
    },
    "en": {
        "title": "Sepehr Fathi | Software Engineer, AI Builder & Inventor",
        "description": "The résumé and portfolio of Sepehr Fathi, software engineer, inventor and senior developer of the Bardaskan citizen super app, working across Flutter, applied AI and product engineering.",
        "keywords": "Sepehr Fathi, Sepehr, Sepehr Fatehi, Sepehr Fathy, Sepehr Fathi resume, Sepehr Fathi portfolio, Sepehr Fathi Bardaskan, Bardaskan, Bardaskan app, Bardaskan citizen super app, Bardaskan municipality app, app.bardaskan.ir, senior software engineer, personal resume, software engineer portfolio, full-stack developer, AI engineer, prompt engineering, computer vision, Flutter developer, Python, FastAPI, React, inventor, founder, Mashhad",
    },
}

FAQ = {
    "fa": {
        "eyebrow": "پرسش‌های پرتکرار",
        "title": "سؤال‌های متداول",
        "sub": "پاسخ کوتاه به جست‌وجوهای رایج دربارهٔ رزومه، تخصص‌ها و راه‌های ارتباطی.",
        "items": [
            (
                "سپهر فتحی کیست؟",
                "سپهر فتحی (Sepehr Fathi) مهندس نرم‌افزار، مخترع و بنیان‌گذار مستقر در مشهد است. او بنیان‌گذار و رئیس هیئت‌مدیرهٔ ویرا وب آریا، مدیرعامل نانو حباب روشنا و مهندس نرم‌افزار ارشد همکار با Cuatro و NanoMAR در نروژ است.",
            ),
            (
                "رزومه و نمونه‌کارهای سپهر فتحی شامل چه حوزه‌هایی است؟",
                "رزومهٔ شخصی سپهر فتحی مجموعه‌ای از پروژه‌های توسعهٔ وب و موبایل، Flutter، Python و FastAPI، هوش مصنوعی کاربردی، بینایی ماشین، تحلیل داده، سامانه‌های مکانی، بیوانفورماتیک و فناوری نانوحباب را پوشش می‌دهد.",
            ),
            (
                "تخصص Sepehr Fathi در هوش مصنوعی و مهندسی پرامپت چیست؟",
                "تمرکز او بر ساخت سامانه‌های قابل‌اتکای هوش مصنوعی است: معماری زمینه و دستور، Structured Outputs، فراخوانی ابزار، RAG و اتصال به منبع، ارزیابی و آزمون رگرسیون، و مقاوم‌سازی در برابر Prompt Injection.",
            ),
            (
                "چگونه با سپهر فتحی تماس بگیرم؟",
                "برای همکاری نرم‌افزاری، پروژه‌های هوش مصنوعی یا فعالیت‌های پژوهشی می‌توانید از طریق ایمیل ftsepi@gmail.com، لینکدین، گیت‌هاب یا تلگرام درج‌شده در همین صفحه با سپهر در ارتباط باشید.",
            ),
        ],
    },
    "en": {
        "eyebrow": "Frequently asked questions",
        "title": "Frequently asked questions",
        "sub": "Concise answers about Sepehr's résumé, portfolio, specialist work and contact details.",
        "items": [
            (
                "Who is Sepehr Fathi?",
                "Sepehr Fathi is a software engineer, inventor and founder based in Mashhad, Iran. He founded and chairs Vira Web Aria, leads Nano Hobab Roshana, and works as a senior software engineer with Cuatro and NanoMAR in Norway.",
            ),
            (
                "What does Sepehr Fathi's résumé and portfolio cover?",
                "Sepehr's personal portfolio covers web and mobile engineering, Flutter, Python and FastAPI, applied AI, computer vision, data analysis, geospatial systems, bioinformatics and nano-bubble technology.",
            ),
            (
                "What is Sepehr's prompt and AI systems engineering expertise?",
                "His work includes instruction and context architecture, Structured Outputs, tool calling, RAG and grounded retrieval, evaluation and regression testing, and defences against prompt injection.",
            ),
            (
                "How can I contact Sepehr Fathi?",
                "For software, applied-AI or research collaboration, contact Sepehr at ftsepi@gmail.com or use the LinkedIn, GitHub and Telegram links on this page.",
            ),
        ],
    },
}

NAME_VARIANTS = [
    "سپهر فتحی",
    "سپهر",
    "Sepehr Fathi",
    "Sepehr",
]


def upgrade_profile_schema(text: str, lang: str) -> str:
    def replace(match: re.Match[str]) -> str:
        data = json.loads(match.group(1))
        if data.get("@type") == "ProfilePage":
            person = data["mainEntity"]
        else:
            person = data
        person.pop("@context", None)
        person.update(
            {
                "@id": f"{DOMAIN}/{lang}/#person",
                "@type": "Person",
                "alternateName": NAME_VARIANTS,
                "url": f"{DOMAIN}/{lang}/",
                "image": f"{DOMAIN}/assets/images/sepehr-fathi-knit-portrait.webp",
                "description": SEO.get(lang, {}).get("description", person.get("description", "")),
                "knowsAbout": [
                    "Software Engineering",
                    "Full-stack Development",
                    "Applied AI",
                    "Prompt Engineering",
                    "Computer Vision",
                    "Flutter",
                    "Python",
                    "FastAPI",
                    "Bioinformatics",
                    "Geospatial Intelligence",
                    "Nano-bubble Technology",
                    "Bardaskan Citizen Super App",
                ],
                "alumniOf": [
                    {"@type": "CollegeOrUniversity", "name": "Ferdowsi University of Mashhad", "department": "Mechanical Engineering"},
                    {"@type": "CollegeOrUniversity", "name": "Islamic Azad University", "department": "Computer Studies"},
                    {"@type": "HighSchool", "name": "Shahid Hasheminejad 4 High School (NODET), Mashhad"},
                ],
            }
        )
        profile = {
            "@context": "https://schema.org",
            "@type": "ProfilePage",
            "@id": f"{DOMAIN}/{lang}/#profile",
            "url": f"{DOMAIN}/{lang}/",
            "dateModified": "2026-07-30",
            "mainEntity": person,
        }
        payload = json.dumps(profile, ensure_ascii=False, separators=(",", ":"))
        return f'<script type="application/ld+json">{payload}</script>'

    return re.sub(
        r'<script type="application/ld\+json">(\{.*?\})</script>',
        replace,
        text,
        count=1,
        flags=re.S,
    )


def faq_section(lang: str) -> str:
    d = FAQ[lang]
    items = []
    for question, answer in d["items"]:
        items.append(
            f'          <details class="faq__item reveal"{" open" if not items else ""}>\n'
            f"            <summary><h3>{html.escape(question)}</h3></summary>\n"
            f"            <p>{html.escape(answer)}</p>\n"
            "          </details>"
        )
    return (
        "    <!-- SEO FAQ -->\n"
        '    <section class="section" id="faq">\n'
        '      <div class="container">\n'
        '        <div class="section-head reveal">\n'
        f'          <span class="eyebrow">{html.escape(d["eyebrow"])}</span>\n'
        f'          <h2 class="section-title">{html.escape(d["title"])}</h2>\n'
        f'          <p class="section-sub">{html.escape(d["sub"])}</p>\n'
        "        </div>\n"
        '        <div class="faq__list">\n'
        + "\n".join(items)
        + "\n        </div>\n"
        "      </div>\n"
        "    </section>\n\n"
    )


def faq_schema(lang: str) -> str:
    entities = [
        {
            "@type": "Question",
            "name": question,
            "acceptedAnswer": {"@type": "Answer", "text": answer},
        }
        for question, answer in FAQ[lang]["items"]
    ]
    payload = json.dumps(
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities},
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return f'  <script id="seo-faq-jsonld" type="application/ld+json">{payload}</script>\n'


def prompt_section(lang: str) -> str:
    d = PROMPT[lang]
    cards = []
    for number, (title, body) in enumerate(d["cards"], 1):
        cards.append(
            '        <div class="pf-card reveal">\n'
            f'          <span class="pf-card__n">{number:02d}</span>\n'
            f'          <h4>{html.escape(title)}</h4>\n'
            f'          <p>{html.escape(body)}</p>\n'
            "        </div>"
        )
    return (
        "    <!-- PROMPT ENGINEERING -->\n"
        '    <section class="section" id="prompt">\n'
        '      <div class="container">\n'
        '        <div class="promptfx reveal">\n'
        f'          <span class="eyebrow">{SPARK}{html.escape(d["eyebrow"])}</span>\n'
        f'          <h2 class="section-title">{html.escape(d["title"])}</h2>\n'
        f'          <p class="promptfx__lead">{html.escape(d["lead"])}</p>\n'
        '          <div class="promptfx__grid">\n'
        + "\n".join(cards)
        + "</div>\n"
        f'          <p class="promptfx__note">{QUOTE}{html.escape(d["note"])}</p>\n'
        "        </div>\n"
        "      </div>\n"
        "    </section>\n\n"
        "    <!-- SKILLS -->"
    )


def featured_skill(lang: str) -> str:
    d = PROMPT[lang]
    items = "".join(f"<li>{html.escape(item)}</li>" for item in d["items"])
    return (
        f"\n        <h3>{STAR}{html.escape(d['skill'])}</h3>\n"
        f'        <ul class="skillgroup__items">{items}</ul>\n      '
    )


def update_page(lang: str) -> None:
    path = ROOT / lang / "index.html"
    text = path.read_text(encoding="utf-8")
    text = text.replace("https://sep.onwebs.dev", DOMAIN)
    text = text.replace("sep.onwebs.dev", "sep.onwebs.ir")
    text = text.replace("../assets/images/sepehr-fathi-profile.jpeg", "../assets/images/sepehr-fathi-knit-portrait.webp")
    text = text.replace("../assets/images/sepehrft.png", "../assets/images/sepehr-fathi-knit-portrait.webp")
    text = text.replace("../assets/images/sepehr-fathi-velvet-portrait.png", "../assets/images/sepehr-fathi-knit-portrait.webp")
    text = text.replace("../assets/images/sepehr-fathi-velvet-portrait.webp", "../assets/images/sepehr-fathi-knit-portrait.webp")
    text = re.sub(r'\.\./assets/css/styles\.css(?:\?v=\d+)?"', '../assets/css/styles.css?v=28"', text)
    text = re.sub(r'\.\./assets/js/app\.js(?:\?v=\d+)?"', '../assets/js/app.js?v=22"', text)
    text = re.sub(r'\n  <meta property="og:image(?::alt)?"[^>]*>', "", text)
    text = re.sub(r'\n  <meta name="twitter:image"[^>]*>', "", text)
    for old, new in COPY_REPLACEMENTS.get(lang, {}).items():
        text = text.replace(old, new)
    if lang in SEO:
        seo = SEO[lang]
        text = re.sub(r"<title>.*?</title>", f"<title>{html.escape(seo['title'])}</title>", text, count=1)
        text = re.sub(
            r'<meta name="description" content="[^"]*" />',
            f'<meta name="description" content="{html.escape(seo["description"], quote=True)}" />',
            text,
            count=1,
        )
        text = re.sub(
            r'<meta name="keywords" content="[^"]*" />',
            f'<meta name="keywords" content="{html.escape(seo["keywords"], quote=True)}" />',
            text,
            count=1,
        )
        text = re.sub(
            r'<meta property="og:title" content="[^"]*" />',
            f'<meta property="og:title" content="{html.escape(seo["title"], quote=True)}" />',
            text,
            count=1,
        )
        text = re.sub(
            r'<meta property="og:description" content="[^"]*" />',
            f'<meta property="og:description" content="{html.escape(seo["description"], quote=True)}" />',
            text,
            count=1,
        )
        text = re.sub(
            r'<meta name="twitter:title" content="[^"]*" />',
            f'<meta name="twitter:title" content="{html.escape(seo["title"], quote=True)}" />',
            text,
            count=1,
        )
        text = re.sub(
            r'<meta name="twitter:description" content="[^"]*" />',
            f'<meta name="twitter:description" content="{html.escape(seo["description"], quote=True)}" />',
            text,
            count=1,
        )

    text, count = re.subn(
        r"    <!-- PROMPT ENGINEERING -->.*?    <!-- SKILLS -->",
        prompt_section(lang),
        text,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise RuntimeError(f"prompt section not found in {path}")

    text, count = re.subn(
        r'(?<=<div class="skillgroup skillgroup--feat reveal">).*?(?=</div>)',
        featured_skill(lang),
        text,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise RuntimeError(f"featured skill not found in {path}")

    text = upgrade_profile_schema(text, lang)
    text = re.sub(r'\n  <script id="seo-faq-jsonld".*?</script>', "", text, flags=re.S)
    text = re.sub(
        r"\n    <!-- SEO FAQ -->.*?(?=\n    <!-- CONTACT -->)",
        "",
        text,
        count=1,
        flags=re.S,
    )
    if lang in FAQ:
        text = text.replace("    <!-- CONTACT -->", faq_section(lang) + "    <!-- CONTACT -->", 1)
        text = text.replace("</head>", faq_schema(lang) + "</head>", 1)

    path.write_text(text, encoding="utf-8")


for language in LANGS:
    update_page(language)

root_path = ROOT / "index.html"
root = root_path.read_text(encoding="utf-8")
root = root.replace("https://sep.onwebs.dev", DOMAIN)
root = root.replace("sep.onwebs.dev", "sep.onwebs.ir")
root = root.replace('<html lang="en">', '<html lang="fa" dir="rtl">')
root = re.sub(
    r"<script>\s*\(function\(\).*?</script>",
    '<script>location.replace("./fa/");</script>',
    root,
    count=1,
    flags=re.S,
)
root = re.sub(
    r"<title>.*?</title>",
    "<title>سپهر فتحی | رزومه مهندس نرم‌افزار، هوش مصنوعی و مخترع</title>",
    root,
    count=1,
)
root = re.sub(
    r'<meta name="description" content="[^"]*" />',
    '<meta name="description" content="رزومه و نمونه‌کارهای سپهر فتحی (Sepehr Fathi)، مهندس نرم‌افزار، مخترع و برنامه‌نویس ارشد سوپراپلیکیشن شهروندی بردسکن." />',
    root,
    count=1,
)
root = re.sub(r'\n  <meta name="keywords"[^>]*>', "", root)
root = root.replace(
    '  <meta name="description"',
    '  <meta name="keywords" content="سپهر فتحی, سپهر, Sepehr Fathi, Sepehr, سپهر فتحی بردسکن, بردسکن, اپ بردسکن, سوپراپلیکیشن شهروندی بردسکن, رزومه سپهر فتحی, رزومه شخصی, نمونه کار, مهندس نرم افزار, هوش مصنوعی, برنامه نویس" />\n  <meta name="description"',
    1,
)
root = root.replace(
    '<h1>Sepehr Fathi</h1>\n  <p>Deep-tech founder &amp; senior software engineer</p>',
    "<h1>سپهر فتحی</h1>\n  <p>مهندس نرم‌افزار · مخترع · بنیان‌گذار</p>",
)
root = re.sub(r'\n  <script id="website-jsonld".*?</script>', "", root, flags=re.S)
website_schema = json.dumps(
    {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "سپهر فتحی",
        "alternateName": ["Sepehr Fathi", "سپهر", "sep.onwebs.ir"],
        "url": f"{DOMAIN}/",
    },
    ensure_ascii=False,
    separators=(",", ":"),
)
root = root.replace(
    "</head>",
    f'  <script id="website-jsonld" type="application/ld+json">{website_schema}</script>\n</head>',
    1,
)
root_path.write_text(root, encoding="utf-8")

for filename in ("sitemap.xml", "robots.txt"):
    path = ROOT / filename
    text = path.read_text(encoding="utf-8").replace("https://sep.onwebs.dev", DOMAIN)
    if filename == "sitemap.xml":
        text = re.sub(
            r"(<loc>.*?</loc>)(?!\s*<lastmod>)",
            r"\1\n    <lastmod>2026-07-29</lastmod>",
            text,
        )
    path.write_text(text, encoding="utf-8")

manifest = ROOT / "manifest.webmanifest"
manifest_data = json.loads(manifest.read_text(encoding="utf-8"))
manifest_data.update(
    {
        "name": "سپهر فتحی | Sepehr Fathi",
        "short_name": "سپهر فتحی",
        "description": "رزومه و نمونه‌کارهای سپهر فتحی؛ مهندس نرم‌افزار، مخترع و بنیان‌گذار.",
        "lang": "fa",
    }
)
manifest.write_text(
    json.dumps(manifest_data, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
