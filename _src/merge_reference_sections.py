# -*- coding: utf-8 -*-
"""Merge the requested Amir-reference sections into Sepehr's multilingual site."""

from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REFERENCE = Path("/Users/sepehrfathi2000/Downloads/portfolio")
LANGS = ("fa", "en", "ar", "zh", "ru", "es", "no")
EDU_LABEL = {
    "fa": "تحصیلات", "en": "Education", "ar": "التعليم", "zh": "教育",
    "ru": "Образование", "es": "Formación", "no": "Utdanning",
}
RESUME_HEADINGS = {
    "fa": ("تجربه", "کارهای منتخب", "پروژه‌های بیشتر"),
    "en": ("Experience", "Selected work", "More projects"),
    "ar": ("الخبرة", "أعمال مختارة", "مشاريع أخرى"),
    "zh": ("经历", "精选作品", "更多项目"),
    "ru": ("Опыт", "Избранные работы", "Другие проекты"),
    "es": ("Experiencia", "Trabajo seleccionado", "Más proyectos"),
    "no": ("Erfaring", "Utvalgt arbeid", "Flere prosjekter"),
}

PIN = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
    'stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 '
    '12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="2.6"/></svg>'
)

EDUCATION = {
    "fa": {
        "sub": "پایهٔ مهندسی و مسیر میان مکانیک، نرم‌افزار و فناوری.",
        "items": [
            ("کارشناسی", "دانشگاه فردوسی مشهد", "مهندسی مکانیک",
             "آموزش مهندسی مکانیک با تمرکز بر تحلیل، طراحی و نگاه سیستمی؛ پایه‌ای که در معماری محصول و حل مسئله‌های فنی به کار می‌گیرم.", "مشهد، ایران"),
            ("کارشناسی", "دانشگاه آزاد", "رشتهٔ کامپیوتر",
             "تحصیل در حوزهٔ کامپیوتر و تکمیل مسیر حرفه‌ای توسعهٔ نرم‌افزار، طراحی سامانه و فناوری‌های هوشمند.", "ایران"),
            ("دیپلم", "دبیرستان شهید هاشمی‌نژاد ۴", "استعدادهای درخشان (سمپاد)",
             "دورهٔ دبیرستان در مجموعهٔ استعدادهای درخشان؛ زمینهٔ شکل‌گیری تفکر تحلیلی، حل مسئله و علاقه به مهندسی.", "مشهد، ایران"),
        ],
    },
    "en": {
        "sub": "An engineering foundation spanning mechanics, software and technology.",
        "items": [
            ("Bachelor's", "Ferdowsi University of Mashhad", "Mechanical Engineering",
             "Mechanical-engineering studies centred on analysis, design and systems thinking—the same foundation I apply to product architecture and technical problem-solving.", "Mashhad, Iran"),
            ("Bachelor's", "Islamic Azad University", "Computer Studies",
             "Computer studies complementing my professional path in software development, systems design and intelligent technologies.", "Iran"),
            ("Diploma", "Shahid Hasheminejad 4 High School", "NODET — National Organization for Development of Exceptional Talents",
             "Secondary education in Iran's gifted-student programme, where analytical thinking, problem-solving and an interest in engineering took shape.", "Mashhad, Iran"),
        ],
    },
    "ar": {
        "sub": "أساس هندسي يجمع بين الميكانيكا والبرمجيات والتقنية.",
        "items": [
            ("بكالوريوس", "جامعة فردوسي في مشهد", "الهندسة الميكانيكية", "دراسة هندسية تركّز على التحليل والتصميم والتفكير المنظومي؛ وهي قاعدة أستخدمها في هندسة المنتجات وحل المشكلات التقنية.", "مشهد، إيران"),
            ("بكالوريوس", "الجامعة الإسلامية الحرة", "علوم الحاسوب", "دراسة الحاسوب استكمالاً لمساري المهني في تطوير البرمجيات وتصميم الأنظمة والتقنيات الذكية.", "إيران"),
            ("دبلوم ثانوي", "ثانوية الشهيد هاشمي نجاد ٤", "مدرسة الموهوبين (NODET)", "تعليم ثانوي ضمن برنامج الطلبة الموهوبين، حيث تشكّل التفكير التحليلي والاهتمام بالهندسة.", "مشهد، إيران"),
        ],
    },
    "zh": {
        "sub": "横跨机械、软件与技术的工程基础。",
        "items": [
            ("本科", "马什哈德菲尔多西大学", "机械工程", "以分析、设计和系统思维为核心的机械工程学习，并将这些基础用于产品架构与技术问题解决。", "伊朗马什哈德"),
            ("本科", "伊斯兰阿扎德大学", "计算机专业", "计算机领域学习，进一步完善软件开发、系统设计与智能技术的职业路径。", "伊朗"),
            ("高中毕业", "沙希德·哈希米内贾德第四中学", "伊朗国家英才组织（NODET）", "在英才教育体系完成高中阶段学习，培养了分析思维、问题解决能力与工程兴趣。", "伊朗马什哈德"),
        ],
    },
    "ru": {
        "sub": "Инженерная база на стыке механики, программного обеспечения и технологий.",
        "items": [
            ("Бакалавриат", "Университет Фирдоуси в Мешхеде", "Машиностроение", "Инженерная подготовка с упором на анализ, проектирование и системное мышление — основа для архитектуры продуктов и решения технических задач.", "Мешхед, Иран"),
            ("Бакалавриат", "Исламский университет Азад", "Компьютерные науки", "Обучение в области компьютеров дополняет профессиональный путь в разработке ПО, проектировании систем и интеллектуальных технологиях.", "Иран"),
            ("Диплом", "Школа им. Шахида Хашеминежада № 4", "NODET — школа для одарённых", "Среднее образование в национальной программе для одарённых учащихся, сформировавшее аналитическое мышление и интерес к инженерии.", "Мешхед, Иран"),
        ],
    },
    "es": {
        "sub": "Una base de ingeniería entre mecánica, software y tecnología.",
        "items": [
            ("Grado", "Universidad Ferdowsi de Mashhad", "Ingeniería mecánica", "Formación centrada en análisis, diseño y pensamiento sistémico, una base que aplico a la arquitectura de producto y a la resolución de problemas técnicos.", "Mashhad, Irán"),
            ("Grado", "Universidad Islámica Azad", "Informática", "Estudios de informática que complementan mi trayectoria en desarrollo de software, diseño de sistemas y tecnologías inteligentes.", "Irán"),
            ("Diploma", "Instituto Shahid Hasheminejad 4", "NODET — alumnado con altas capacidades", "Educación secundaria en el programa nacional para estudiantes con talento, donde desarrollé pensamiento analítico e interés por la ingeniería.", "Mashhad, Irán"),
        ],
    },
    "no": {
        "sub": "Et ingeniørgrunnlag på tvers av mekanikk, programvare og teknologi.",
        "items": [
            ("Bachelor", "Ferdowsi-universitetet i Mashhad", "Maskinteknikk", "Ingeniørutdanning med vekt på analyse, design og systemtenkning—et grunnlag jeg bruker i produktarkitektur og teknisk problemløsning.", "Mashhad, Iran"),
            ("Bachelor", "Islamic Azad University", "Datastudier", "Datastudier som utfyller min profesjonelle vei innen programvareutvikling, systemdesign og intelligente teknologier.", "Iran"),
            ("Vitnemål", "Shahid Hasheminejad 4 videregående skole", "NODET — skole for særlig begavede", "Videregående opplæring i Irans nasjonale talentprogram, der analytisk tenkning og interessen for ingeniørfag tok form.", "Mashhad, Iran"),
        ],
    },
}

BARDASKAN = {
    "fa": ("برنامه‌نویس ارشد", "سوپراپلیکیشن شهروندی بردسکن", "برنامه‌نویس ارشد سوپراپ",
           "رهبری فنی و توسعهٔ سوپراپلیکیشن خدمات شهروندی بردسکن برای اندروید و وب؛ یکپارچه‌سازی خدمات شهری، اطلاع‌رسانی و ارتباط مردم با شهرداری در یک محصول چندسکویی.", "بردسکن، ایران",
           "نسخهٔ اندروید در بازار", "وب‌اپ بردسکن"),
    "en": ("Senior developer", "Bardaskan Citizen Super App", "Senior super-app developer",
           "Technical leadership and development of Bardaskan's citizen-services super app for Android and the web, bringing municipal services, public information and citizen communication into one cross-platform product.", "Bardaskan, Iran",
           "Android on Cafe Bazaar", "Bardaskan web app"),
    "ar": ("مطور أول", "تطبيق بردسكن الشامل للمواطنين", "المطور الأول للتطبيق الشامل",
           "القيادة التقنية وتطوير تطبيق خدمات المواطنين في بردسكن لنظام أندرويد والويب، جامعاً الخدمات البلدية والمعلومات والتواصل مع المواطنين في منتج متعدد المنصات.", "بردسكن، إيران",
           "نسخة أندرويد على بازار", "تطبيق بردسكن على الويب"),
    "zh": ("高级开发工程师", "巴尔达斯坎市民超级应用", "超级应用高级开发工程师",
           "负责巴尔达斯坎市民服务超级应用的技术开发，覆盖 Android 与 Web，将市政服务、公共信息和市民沟通整合为一个跨平台产品。", "伊朗巴尔达斯坎",
           "Cafe Bazaar 安卓版", "巴尔达斯坎 Web 应用"),
    "ru": ("Старший разработчик", "Городское суперприложение Бардескана", "Старший разработчик суперприложения",
           "Техническое руководство и разработка городского суперприложения Бардескана для Android и веба: муниципальные услуги, информирование и связь жителей с администрацией в одном продукте.", "Бардескан, Иран",
           "Android в Cafe Bazaar", "Веб-приложение Бардескана"),
    "es": ("Desarrollador sénior", "Superapp ciudadana de Bardaskan", "Desarrollador sénior de la superapp",
           "Liderazgo técnico y desarrollo de la superapp de servicios ciudadanos de Bardaskan para Android y web, unificando servicios municipales, información y comunicación ciudadana.", "Bardaskan, Irán",
           "Android en Cafe Bazaar", "Web app de Bardaskan"),
    "no": ("Seniorutvikler", "Bardaskan innbygger-superapp", "Seniorutvikler for superappen",
           "Teknisk ledelse og utvikling av Bardaskans superapp for innbyggertjenester på Android og nett, med kommunale tjenester, informasjon og innbyggerdialog i ett produkt.", "Bardaskan, Iran",
           "Android på Cafe Bazaar", "Bardaskan webapp"),
}

FAQ_CONTENT = {
    "ar": [
        ("من هو سبهر فتحي؟", "سبهر فتحي مهندس برمجيات ومخترع ومؤسس مقيم في مشهد، إيران. أسّس ويرأس مجلس إدارة Vira Web Aria، ويقود Nano Hobab Roshana، ويعمل مهندس برمجيات أول مع Cuatro وNanoMAR في النرويج."),
        ("ما مجالات عمل سبهر فتحي؟", "يعمل في تطوير الويب وتطبيقات Flutter والأنظمة الخلفية والذكاء الاصطناعي التطبيقي والرؤية الحاسوبية وتحليل البيانات والأنظمة الجغرافية والمعلوماتية الحيوية وتقنية الفقاعات النانوية."),
        ("ما هو تطبيق بردسكن الشامل؟", "هو تطبيق خدمات المواطنين لبلدية بردسكن على أندرويد والويب. يعمل سبهر فتحي مطوراً أول للمشروع، جامعاً الخدمات البلدية والمعلومات والتواصل مع المواطنين في منتج واحد."),
        ("ما هي دراسة سبهر فتحي؟", "درس الهندسة الميكانيكية في جامعة فردوسي في مشهد وعلوم الحاسوب في الجامعة الإسلامية الحرة، وتخرّج في ثانوية الشهيد هاشمي نجاد ٤ للطلاب الموهوبين."),
        ("كيف أتواصل مع سبهر فتحي؟", "يمكن التواصل عبر البريد ftsepi@gmail.com أو نموذج هذه الصفحة، وكذلك عبر GitHub وLinkedIn وTelegram."),
    ],
    "zh": [
        ("塞佩尔·法蒂是谁？", "塞佩尔·法蒂是一位常驻伊朗马什哈德的软件工程师、发明人和创业者。他创办并担任 Vira Web Aria 董事长，领导 Nano Hobab Roshana，并与挪威的 Cuatro 和 NanoMAR 合作担任高级软件工程师。"),
        ("塞佩尔·法蒂从事哪些领域？", "他的工作涵盖 Web 与 Flutter 应用、后端系统、应用型人工智能、计算机视觉、数据分析、地理空间系统、生物信息学和纳米气泡技术。"),
        ("什么是巴尔达斯坎市民超级应用？", "这是面向巴尔达斯坎市民的 Android 与 Web 城市服务平台。塞佩尔担任高级开发工程师，将市政服务、公共信息和市民沟通整合在一个产品中。"),
        ("塞佩尔·法蒂的教育背景是什么？", "他在马什哈德菲尔多西大学学习机械工程，在伊斯兰阿扎德大学学习计算机专业，高中毕业于 NODET 英才教育体系的沙希德·哈希米内贾德第四中学。"),
        ("如何联系塞佩尔·法蒂？", "可通过 ftsepi@gmail.com、本页联系表单，或页面中的 GitHub、LinkedIn 与 Telegram 链接联系。"),
    ],
    "ru": [
        ("Кто такой Сепехр Фатхи?", "Сепехр Фатхи — инженер-программист, изобретатель и основатель из Мешхеда, Иран. Он основал Vira Web Aria и возглавляет её совет директоров, руководит Nano Hobab Roshana и работает старшим инженером с Cuatro и NanoMAR в Норвегии."),
        ("В каких областях работает Сепехр Фатхи?", "Его опыт охватывает веб-разработку, Flutter, серверные системы, прикладной ИИ, компьютерное зрение, анализ данных, геоинформационные системы, биоинформатику и нанопузырьковые технологии."),
        ("Что такое суперприложение Бардескана?", "Это платформа городских услуг для Android и веба. Сепехр работает старшим разработчиком проекта, объединяющего муниципальные услуги, информацию и связь жителей с администрацией."),
        ("Какое образование у Сепехра Фатхи?", "Он изучал машиностроение в Университете Фирдоуси в Мешхеде и компьютерные науки в Исламском университете Азад, а также окончил школу для одарённых им. Шахида Хашеминежада № 4."),
        ("Как связаться с Сепехром Фатхи?", "Напишите на ftsepi@gmail.com, воспользуйтесь формой на этой странице или ссылками GitHub, LinkedIn и Telegram."),
    ],
    "es": [
        ("¿Quién es Sepehr Fathi?", "Sepehr Fathi es ingeniero de software, inventor y fundador radicado en Mashhad, Irán. Fundó y preside Vira Web Aria, dirige Nano Hobab Roshana y trabaja como ingeniero de software sénior con Cuatro y NanoMAR en Noruega."),
        ("¿En qué áreas trabaja Sepehr Fathi?", "Su experiencia abarca desarrollo web, Flutter, sistemas backend, IA aplicada, visión por computador, análisis de datos, sistemas geoespaciales, bioinformática y tecnología de nanoburbujas."),
        ("¿Qué es la superapp ciudadana de Bardaskan?", "Es una plataforma de servicios municipales para Android y web. Sepehr es desarrollador sénior del proyecto, que reúne servicios urbanos, información pública y comunicación ciudadana."),
        ("¿Qué formación tiene Sepehr Fathi?", "Estudió Ingeniería mecánica en la Universidad Ferdowsi de Mashhad e Informática en la Universidad Islámica Azad; cursó secundaria en el instituto para alumnado con talento Shahid Hasheminejad 4."),
        ("¿Cómo contactar con Sepehr Fathi?", "Escribe a ftsepi@gmail.com, utiliza el formulario de esta página o los enlaces de GitHub, LinkedIn y Telegram."),
    ],
    "no": [
        ("Hvem er Sepehr Fathi?", "Sepehr Fathi er programvareingeniør, oppfinner og gründer fra Mashhad i Iran. Han grunnla og er styreleder i Vira Web Aria, leder Nano Hobab Roshana og arbeider som senior programvareingeniør med Cuatro og NanoMAR i Norge."),
        ("Hvilke fagområder arbeider Sepehr Fathi med?", "Arbeidet hans omfatter webutvikling, Flutter, backend-systemer, anvendt KI, datasyn, dataanalyse, geospatiale systemer, bioinformatikk og nanobobleteknologi."),
        ("Hva er Bardaskan innbygger-superapp?", "Det er en plattform for kommunale tjenester på Android og nett. Sepehr er seniorutvikler for prosjektet, som samler tjenester, informasjon og innbyggerdialog i ett produkt."),
        ("Hvilken utdanning har Sepehr Fathi?", "Han studerte maskinteknikk ved Ferdowsi-universitetet i Mashhad og datafag ved Islamic Azad University, og gikk på NODET-skolen Shahid Hasheminejad 4."),
        ("Hvordan kontakter jeg Sepehr Fathi?", "Send e-post til ftsepi@gmail.com, bruk kontaktskjemaet på siden eller lenkene til GitHub, LinkedIn og Telegram."),
    ],
}


def section(text: str, section_id: str) -> str:
    match = re.search(
        rf'    <!--[^\n]*-->\n    <section\b[^>]*\bid="{re.escape(section_id)}"[^>]*>.*?\n    </section>',
        text,
        flags=re.S,
    )
    if not match:
        raise RuntimeError(f"section #{section_id} not found")
    return match.group(0)


def replace_section(text: str, section_id: str, replacement: str) -> str:
    old = section(text, section_id)
    return text.replace(old, replacement, 1)


def education_card(item: tuple[str, str, str, str, str]) -> str:
    badge, org, role, detail, loc = (html.escape(v) for v in item)
    return (
        '\n      <article class="role reveal">\n'
        f'        <div><span class="role__badge">{badge}</span></div>\n'
        '        <div class="role__main">\n'
        f'          <h3 class="role__org">{org}</h3>\n'
        f'          <div class="role__role">{role}</div>\n'
        f'          <p class="role__detail">{detail}</p>\n'
        f'          <span class="role__loc">{PIN}{loc}</span>\n'
        '        </div>\n'
        '      </article>'
    )


def build_education(ref: str, lang: str) -> str:
    ref_edu = section(ref, "edu")
    data = EDUCATION[lang]
    cards = "".join(education_card(item) for item in data["items"])
    ref_edu = re.sub(
        r'<p class="section-sub">.*?</p>',
        f'<p class="section-sub">{html.escape(data["sub"])}</p>',
        ref_edu,
        count=1,
        flags=re.S,
    )
    return re.sub(
        r'<div class="roles__list">.*?</article></div>',
        f'<div class="roles__list">{cards}</div>',
        ref_edu,
        count=1,
        flags=re.S,
    )


def bardaskan_card(lang: str) -> str:
    badge, org, role, detail, loc, market_label, web_label = (html.escape(v) for v in BARDASKAN[lang])
    return (
        '\n      <article class="role reveal role--bardaskan">\n'
        f'        <div><span class="role__badge">{badge}</span></div>\n'
        '        <div class="role__main">\n'
        f'          <h3 class="role__org">{org}</h3>\n'
        f'          <div class="role__role">{role}</div>\n'
        f'          <p class="role__detail">{detail}</p>\n'
        '          <div class="role__links">'
        f'<a href="https://cafebazaar.ir/app/com.example.flutter_application_1" target="_blank" rel="noopener">{market_label}</a>'
        f'<a href="https://app.bardaskan.ir" target="_blank" rel="noopener">{web_label}</a>'
        '</div>\n'
        f'          <span class="role__loc">{PIN}{loc}</span>\n'
        '        </div>\n'
        '      </article>'
    )


def grid_articles(sec: str) -> list[str]:
    return re.findall(r'<article class="venture[^"]*">.*?</article>', sec, flags=re.S)


def replace_venture_grid(sec: str, articles: list[str]) -> str:
    return re.sub(
        r'(<div class="ventures__grid">).*?(</div>\s*</div>\s*</section>)',
        lambda m: m.group(1) + "\n      " + "".join(articles) + m.group(2),
        sec,
        count=1,
        flags=re.S,
    )


def work_inner(sec: str) -> str:
    match = re.search(
        r'<div class="work__list">(.*?)</div>\s*<p class="work__note"',
        sec,
        flags=re.S,
    )
    if not match:
        raise RuntimeError("work list not found")
    return match.group(1)


def replace_work_inner(sec: str, inner: str) -> str:
    return re.sub(
        r'(<div class="work__list">).*?(</div>\s*<p class="work__note")',
        lambda m: m.group(1) + inner + m.group(2),
        sec,
        count=1,
        flags=re.S,
    )


def add_education_nav(text: str, ref: str, lang: str) -> str:
    if 'href="#edu"' in text:
        return text
    desktop = re.search(r'<a href="#edu">.*?</a>', ref, flags=re.S)
    mobile = re.search(r'<a class="mlink" href="#edu">.*?</a>', ref, flags=re.S)
    desktop_link = desktop.group(0) if desktop else f'<a href="#edu">{EDU_LABEL[lang]}</a>'
    text = text.replace('<a href="#ventures">', desktop_link + '<a href="#ventures">', 1)
    if mobile:
        text = text.replace(
            '<a class="mlink" href="#ventures">',
            mobile.group(0) + '<a class="mlink" href="#ventures">',
            1,
        )
    return text


def adapt_contact(current: str, ref: str) -> str:
    contact = section(ref, "contact")
    replacements = {
        "amir@onwebs.ir": "ftsepi@gmail.com",
        "https://github.com/AmirMoghtader": "https://github.com/sepehrfathi",
        "https://www.linkedin.com/in/amir-h-moghtader-a83437417/": "https://www.linkedin.com/in/sepehr-fathi",
        "https://t.me/Amir_Mg6": "https://t.me/sepehrfathi",
    }
    for old, new in replacements.items():
        contact = contact.replace(old, new)
    contact = re.sub(
        r'\s*<a class="channel" href="https://instagram\.com/Amir_Mg6".*?</a>',
        "",
        contact,
        count=1,
        flags=re.S,
    )
    return contact


def build_faq(ref: str, lang: str) -> str:
    faq = section(ref, "faq")
    items = "".join(
        '<details class="faq__item reveal"%s><summary><h3>%s</h3></summary><p>%s</p></details>'
        % (" open" if index == 0 else "", html.escape(question), html.escape(answer))
        for index, (question, answer) in enumerate(FAQ_CONTENT[lang])
    )
    return re.sub(
        r'<div class="faq__list">.*?</div>',
        f'<div class="faq__list">{items}</div>',
        faq,
        count=1,
        flags=re.S,
    )


def resume_section(text: str, heading: str) -> str:
    match = re.search(
        rf'<div class="r-sec"[^>]*><h2>{re.escape(heading)}</h2>.*?(?=\n\s*<div class="r-sec"|\n\s*<div class="r-foot")',
        text,
        flags=re.S,
    )
    if not match:
        raise RuntimeError(f"resume section not found: {heading}")
    return match.group(0)


def resume_education(lang: str) -> str:
    blocks = []
    for _badge, org, role, detail, loc in EDUCATION[lang]["items"]:
        blocks.append(
            '\n        <div class="r-exp">\n'
            f'          <div class="r-exp-h"><span class="r-exp-org">{html.escape(org)}</span>'
            f'<span class="r-exp-loc">{html.escape(loc)}</span></div>\n'
            f'          <div class="r-exp-role">{html.escape(role)}</div>\n'
            f'          <p>{html.escape(detail)}</p>\n'
            '        </div>'
        )
    return (
        f'      <div class="r-sec" data-resume-education><h2>{EDU_LABEL[lang]}</h2>'
        + "".join(blocks)
        + "</div>\n"
    )


def sync_resume(text: str, ref: str, lang: str) -> str:
    experience_heading, selected_heading, more_heading = RESUME_HEADINGS[lang]

    experience = resume_section(text, experience_heading)
    if 'data-resume-bardaskan' not in experience:
        badge, org, role, detail, loc, _market, _web = BARDASKAN[lang]
        bard = (
            '\n        <div class="r-exp" data-resume-bardaskan>\n'
            f'          <div class="r-exp-h"><span class="r-exp-org">{html.escape(org)}</span>'
            f'<span class="r-exp-loc">{html.escape(loc)}</span></div>\n'
            f'          <div class="r-exp-role">{html.escape(role)}</div>\n'
            f'          <p>{html.escape(detail)}</p>\n'
            '        </div>'
        )
        experience = experience.rstrip()
        experience = experience[:-6] + bard + "</div>"
        text = text.replace(resume_section(text, experience_heading), experience, 1)

    if 'data-resume-education' not in text:
        selected = resume_section(text, selected_heading)
        text = text.replace(selected, resume_education(lang) + "      " + selected, 1)

    current_selected = resume_section(text, selected_heading)
    if 'data-resume-reference-merged' not in current_selected:
        ref_selected = resume_section(ref, selected_heading)
        own_vents = [
            item for item in re.findall(r'<div class="r-vent">.*?</div>', current_selected, flags=re.S)
            if "HomAI" not in item
        ]
        ref_vents = re.findall(r'<div class="r-vent">.*?</div>', ref_selected, flags=re.S)
        merged_selected = re.sub(
            r'(<div class="r-sec")><h2>(.*?)</h2>.*',
            lambda m: (
                m.group(1) + ' data-resume-reference-merged><h2>' + m.group(2)
                + "</h2>\n        " + "".join(ref_vents + own_vents) + "</div>"
            ),
            current_selected,
            count=1,
            flags=re.S,
        )
        text = text.replace(current_selected, merged_selected, 1)

    current_more = resume_section(text, more_heading)
    if 'data-resume-reference-merged' not in current_more:
        ref_more = resume_section(ref, "Ещё проекты" if lang == "ru" else more_heading)
        current_spans = re.findall(r'<span>.*?</span>', current_more, flags=re.S)
        ref_spans = re.findall(r'<span>.*?</span>', ref_more, flags=re.S)
        merged_more = current_more.replace(
            '<div class="r-sec">',
            '<div class="r-sec" data-resume-reference-merged>',
            1,
        )
        merged_more = re.sub(
            r'<div class="r-work">.*?</div>',
            '<div class="r-work">' + "".join(ref_spans + current_spans) + "</div>",
            merged_more,
            count=1,
            flags=re.S,
        )
        text = text.replace(current_more, merged_more, 1)
    return text


def merge_page(lang: str) -> None:
    path = ROOT / lang / "index.html"
    ref_path = REFERENCE / lang / "index.html"
    text = path.read_text(encoding="utf-8")
    ref = ref_path.read_text(encoding="utf-8")

    text = add_education_nav(text, ref, lang)

    if 'id="edu"' not in text:
        roles = section(text, "roles")
        text = text.replace(roles, roles + "\n\n" + build_education(ref, lang), 1)

    roles = section(text, "roles")
    if "app.bardaskan.ir" not in roles:
        prefix, suffix = roles.rsplit("</article></div>", 1)
        roles = prefix + "</article>" + bardaskan_card(lang) + "</div>" + suffix
        text = replace_section(text, "roles", roles)

    current_ventures = section(text, "ventures")
    if 'data-reference-merged="true"' not in current_ventures:
        ref_ventures = section(ref, "ventures")
        ref_cards = grid_articles(ref_ventures)
        own_cards = [card for card in grid_articles(current_ventures) if "HomAI" not in card]
        merged = replace_venture_grid(ref_ventures, ref_cards + own_cards)
        merged = merged.replace(
            '<section class="section" id="ventures">',
            '<section class="section" id="ventures" data-reference-merged="true">',
            1,
        )
        text = replace_section(text, "ventures", merged)

    text = replace_section(text, "portfolio", section(ref, "portfolio"))

    current_work = section(text, "work")
    if 'data-reference-merged="true"' not in current_work:
        ref_work = section(ref, "work")
        combined = work_inner(ref_work) + work_inner(current_work)
        merged_work = replace_work_inner(ref_work, combined)
        merged_work = merged_work.replace(
            '<section class="section" id="work">',
            '<section class="section" id="work" data-reference-merged="true">',
            1,
        )
        text = replace_section(text, "work", merged_work)

    ref_faq = section(ref, "faq")
    if 'id="faq"' in text:
        current_faq = section(text, "faq")
        ref_head = re.search(r'<div class="section-head reveal">.*?</div>', ref_faq, flags=re.S)
        if ref_head:
            current_faq = re.sub(
                r'<div class="section-head reveal">.*?</div>',
                ref_head.group(0),
                current_faq,
                count=1,
                flags=re.S,
            )
        current_faq = re.sub(
            r'<details class="faq__item reveal"(?: open)?>',
            '<details class="faq__item reveal" open>',
            current_faq,
            count=1,
        )
        text = replace_section(text, "faq", current_faq)
    else:
        text = text.replace("    <!-- CONTACT -->", build_faq(ref, lang) + "\n\n    <!-- CONTACT -->", 1)

    text = replace_section(text, "contact", adapt_contact(text, ref))
    text = sync_resume(text, ref, lang)
    text = re.sub(r'\.\./assets/css/styles\.css(?:\?v=\d+)?"', '../assets/css/styles.css?v=28"', text)
    text = re.sub(r'\.\./assets/js/app\.js(?:\?v=\d+)?"', '../assets/js/app.js?v=22"', text)
    path.write_text(text, encoding="utf-8")


if not REFERENCE.exists():
    raise SystemExit(f"Reference portfolio not found: {REFERENCE}")

for language in LANGS:
    merge_page(language)
    print(f"merged reference sections: {language}")
