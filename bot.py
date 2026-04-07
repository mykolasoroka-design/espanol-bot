import os
import json
import random
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)

TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# ══════════════════════════════════════════════════════════
# НАВЧАЛЬНИЙ КОНТЕНТ
# ══════════════════════════════════════════════════════════

LESSONS = [
    {
        "id": 1,
        "title": "🔤 Урок 1: Привітання",
        "theory": (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "📖 *УРОК 1: Привітання*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "*Основні привітання:*\n\n"
            "🌅 *Hola* — Привіт\n"
            "🌄 *Buenos días* — Доброго ранку\n"
            "☀️ *Buenas tardes* — Добрий день\n"
            "🌙 *Buenas noches* — Добрий вечір/ніч\n"
            "👋 *¿Cómo estás?* — Як справи?\n"
            "😊 *Bien, gracias* — Добре, дякую\n"
            "🤝 *Mucho gusto* — Приємно познайомитись\n"
            "👋 *Adiós* — До побачення\n"
            "💬 *Hasta luego* — До зустрічі\n\n"
            "💡 *Підказка:* В іспанській є два «ти»:\n"
            "• *tú* — неформальне (друзі, діти)\n"
            "• *usted* — формальне (незнайомці, старші)"
        ),
        "quiz": [
            {"q": "Як сказати 'Привіт' іспанською?", "a": "Hola", "options": ["Hola", "Adiós", "Gracias", "Buenos"]},
            {"q": "Що означає 'Buenos días'?", "a": "Доброго ранку", "options": ["Добрий вечір", "Доброго ранку", "Добрий день", "До побачення"]},
            {"q": "Як спитати 'Як справи?'", "a": "¿Cómo estás?", "options": ["¿Qué hora es?", "¿Cómo te llamas?", "¿Cómo estás?", "¿Dónde estás?"]},
        ]
    },
    {
        "id": 2,
        "title": "🔢 Урок 2: Числа 1–20",
        "theory": (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "📖 *УРОК 2: Числа 1–20*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "1️⃣ uno   2️⃣ dos   3️⃣ tres\n"
            "4️⃣ cuatro   5️⃣ cinco   6️⃣ seis\n"
            "7️⃣ siete   8️⃣ ocho   9️⃣ nueve\n"
            "🔟 diez\n\n"
            "1️⃣1️⃣ once   1️⃣2️⃣ doce   1️⃣3️⃣ trece\n"
            "1️⃣4️⃣ catorce   1️⃣5️⃣ quince\n"
            "1️⃣6️⃣ dieciséis   1️⃣7️⃣ diecisiete\n"
            "1️⃣8️⃣ dieciocho   1️⃣9️⃣ diecinueve\n"
            "2️⃣0️⃣ veinte\n\n"
            "💡 *Лайфхак:* 11-15 треба просто вивчити.\n"
            "16-19 = dieci + (6-9)"
        ),
        "quiz": [
            {"q": "Як буде '5' іспанською?", "a": "cinco", "options": ["cuatro", "cinco", "seis", "siete"]},
            {"q": "Що означає 'diez'?", "a": "10", "options": ["7", "8", "9", "10"]},
            {"q": "Як буде '15' іспанською?", "a": "quince", "options": ["catorce", "quince", "trece", "dieciséis"]},
        ]
    },
    {
        "id": 3,
        "title": "🎨 Урок 3: Кольори",
        "theory": (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "📖 *УРОК 3: Кольори*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "❤️ *rojo* — червоний\n"
            "💛 *amarillo* — жовтий\n"
            "💙 *azul* — синій\n"
            "💚 *verde* — зелений\n"
            "🤍 *blanco* — білий\n"
            "🖤 *negro* — чорний\n"
            "🟠 *naranja* — помаранчевий\n"
            "🟣 *morado / violeta* — фіолетовий\n"
            "🩷 *rosa* — рожевий\n"
            "🟤 *marrón* — коричневий\n"
            "⚪ *gris* — сірий\n\n"
            "💡 *Граматика:* Прикметники в іспанській\n"
            "узгоджуються з іменником за родом:\n"
            "• El coche *rojo* (машина червона — м.р.)\n"
            "• La casa *roja* (будинок червоний — ж.р.)"
        ),
        "quiz": [
            {"q": "Як буде 'синій' іспанською?", "a": "azul", "options": ["verde", "azul", "rojo", "amarillo"]},
            {"q": "Що означає 'negro'?", "a": "чорний", "options": ["білий", "сірий", "чорний", "коричневий"]},
            {"q": "Як буде 'зелений' іспанською?", "a": "verde", "options": ["verde", "blanco", "naranja", "rosa"]},
        ]
    },
    {
        "id": 4,
        "title": "👨‍👩‍👧 Урок 4: Родина",
        "theory": (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "📖 *УРОК 4: Родина*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "👨 *el padre* — батько\n"
            "👩 *la madre* — мати\n"
            "👦 *el hijo* — син\n"
            "👧 *la hija* — дочка\n"
            "👴 *el abuelo* — дідусь\n"
            "👵 *la abuela* — бабуся\n"
            "👱 *el hermano* — брат\n"
            "👱‍♀️ *la hermana* — сестра\n"
            "👨‍💼 *el tío* — дядько\n"
            "👩‍💼 *la tía* — тітка\n\n"
            "💡 *Артиклі:*\n"
            "• *el* — чоловічий рід (el padre)\n"
            "• *la* — жіночий рід (la madre)\n"
            "• *los / las* — множина"
        ),
        "quiz": [
            {"q": "Як буде 'мати' іспанською?", "a": "la madre", "options": ["el padre", "la madre", "la hija", "la abuela"]},
            {"q": "Що означає 'el hermano'?", "a": "брат", "options": ["сестра", "брат", "дядько", "кузен"]},
            {"q": "Який артикль у слова 'hijo' (син)?", "a": "el", "options": ["la", "el", "los", "las"]},
        ]
    },
    {
        "id": 5,
        "title": "🍎 Урок 5: Їжа",
        "theory": (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "📖 *УРОК 5: Їжа*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🍞 *el pan* — хліб\n"
            "🥛 *la leche* — молоко\n"
            "🍳 *el huevo* — яйце\n"
            "🍗 *el pollo* — курка\n"
            "🐟 *el pescado* — риба\n"
            "🍚 *el arroz* — рис\n"
            "🥗 *la ensalada* — салат\n"
            "☕ *el café* — кава\n"
            "💧 *el agua* — вода\n"
            "🍷 *el vino* — вино\n\n"
            "💡 *Корисні фрази:*\n"
            "• *Tengo hambre* — Я голодний/а\n"
            "• *Tengo sed* — Я хочу пити\n"
            "• *¡Buen provecho!* — Смачного!"
        ),
        "quiz": [
            {"q": "Як буде 'хліб' іспанською?", "a": "el pan", "options": ["la leche", "el pan", "el agua", "el café"]},
            {"q": "Що означає 'el pollo'?", "a": "курка", "options": ["риба", "яйце", "курка", "рис"]},
            {"q": "Як сказати 'Я голодний'?", "a": "Tengo hambre", "options": ["Tengo sed", "Tengo hambre", "Tengo frío", "Tengo sueño"]},
        ]
    },
    {
        "id": 6,
        "title": "🕐 Урок 6: Час і дні тижня",
        "theory": (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "📖 *УРОК 6: Час і дні тижня*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "*Дні тижня:*\n"
            "Пн *lunes* | Вт *martes* | Ср *miércoles*\n"
            "Чт *jueves* | Пт *viernes*\n"
            "Сб *sábado* | Нд *domingo*\n\n"
            "*Час:*\n"
            "• *¿Qué hora es?* — Котра година?\n"
            "• *Es la una* — Перша година\n"
            "• *Son las dos* — Друга година\n"
            "• *Son las tres y media* — Пів на четверту\n"
            "• *Son las cinco menos cuarto* — Без чверті п'ять\n\n"
            "💡 *Запам'ятай:* 'es' для 1-ї год,\n"
            "'son' для решти!"
        ),
        "quiz": [
            {"q": "Як буде 'понеділок' іспанською?", "a": "lunes", "options": ["martes", "lunes", "miércoles", "jueves"]},
            {"q": "Що означає '¿Qué hora es?'", "a": "Котра година?", "options": ["Який день?", "Котра година?", "Яке число?", "Який рік?"]},
            {"q": "Як сказати 'Друга година'?", "a": "Son las dos", "options": ["Es la dos", "Son las dos", "Es las dos", "Son la dos"]},
        ]
    },
    {
        "id": 7,
        "title": "🏠 Урок 7: Дієслово SER і ESTAR",
        "theory": (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "📖 *УРОК 7: SER і ESTAR*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Обидва = 'бути', але різні!\n\n"
            "*SER* — постійні характеристики:\n"
            "yo *soy* | tú *eres* | él/ella *es*\n"
            "nosotros *somos* | ellos *son*\n\n"
            "*ESTAR* — тимчасовий стан, місце:\n"
            "yo *estoy* | tú *estás* | él/ella *está*\n"
            "nosotros *estamos* | ellos *están*\n\n"
            "💡 *SER:* Soy ucraniano. (Я українець)\n"
            "💡 *ESTAR:* Estoy cansado. (Я втомлений)\n\n"
            "🧠 *Правило:* 'де знаходиться?' = ESTAR\n"
            "'хто такий / який за природою?' = SER"
        ),
        "quiz": [
            {"q": "Яка форма SER для 'я'?", "a": "soy", "options": ["estoy", "soy", "eres", "es"]},
            {"q": "Я втомлений = ?", "a": "Estoy cansado", "options": ["Soy cansado", "Estoy cansado", "Es cansado", "Estar cansado"]},
            {"q": "Яке дієслово для постійних рис?", "a": "SER", "options": ["ESTAR", "SER", "TENER", "HACER"]},
        ]
    },
    {
        "id": 8,
        "title": "🚶 Урок 8: Дієслово TENER і вік",
        "theory": (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "📖 *УРОК 8: TENER — мати*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "*Відмінювання TENER:*\n"
            "yo *tengo* — я маю\n"
            "tú *tienes* — ти маєш\n"
            "él/ella *tiene* — він/вона має\n"
            "nosotros *tenemos* — ми маємо\n"
            "ellos *tienen* — вони мають\n\n"
            "💡 *Вік через TENER:*\n"
            "• *¿Cuántos años tienes?* — Скільки тобі років?\n"
            "• *Tengo 30 años* — Мені 30 років\n\n"
            "💡 *Інші вирази з TENER:*\n"
            "• *tener hambre* — бути голодним\n"
            "• *tener sed* — хотіти пити\n"
            "• *tener sueño* — хотіти спати\n"
            "• *tener miedo* — боятися"
        ),
        "quiz": [
            {"q": "Як сказати 'Мені 25 років'?", "a": "Tengo 25 años", "options": ["Soy 25 años", "Tengo 25 años", "Estoy 25 años", "Tiene 25 años"]},
            {"q": "Яка форма TENER для 'вони'?", "a": "tienen", "options": ["tenemos", "tienen", "tiene", "tengo"]},
            {"q": "Що означає 'tener sueño'?", "a": "хотіти спати", "options": ["боятися", "хотіти пити", "хотіти спати", "бути голодним"]},
        ]
    },
]

FLASHCARDS = [
    # Базові слова
    {"es": "hola", "ua": "привіт", "category": "привітання"},
    {"es": "gracias", "ua": "дякую", "category": "ввічливість"},
    {"es": "por favor", "ua": "будь ласка", "category": "ввічливість"},
    {"es": "sí", "ua": "так", "category": "базові"},
    {"es": "no", "ua": "ні", "category": "базові"},
    {"es": "perdón", "ua": "вибачте", "category": "ввічливість"},
    {"es": "de nada", "ua": "нема за що", "category": "ввічливість"},
    # Числа
    {"es": "uno", "ua": "один", "category": "числа"},
    {"es": "dos", "ua": "два", "category": "числа"},
    {"es": "tres", "ua": "три", "category": "числа"},
    {"es": "diez", "ua": "десять", "category": "числа"},
    {"es": "veinte", "ua": "двадцять", "category": "числа"},
    {"es": "cien", "ua": "сто", "category": "числа"},
    # Кольори
    {"es": "rojo", "ua": "червоний", "category": "кольори"},
    {"es": "azul", "ua": "синій", "category": "кольори"},
    {"es": "verde", "ua": "зелений", "category": "кольори"},
    {"es": "negro", "ua": "чорний", "category": "кольори"},
    {"es": "blanco", "ua": "білий", "category": "кольори"},
    {"es": "amarillo", "ua": "жовтий", "category": "кольори"},
    # Їжа
    {"es": "el pan", "ua": "хліб", "category": "їжа"},
    {"es": "el agua", "ua": "вода", "category": "їжа"},
    {"es": "el café", "ua": "кава", "category": "їжа"},
    {"es": "el pollo", "ua": "курка", "category": "їжа"},
    {"es": "la leche", "ua": "молоко", "category": "їжа"},
    {"es": "el arroz", "ua": "рис", "category": "їжа"},
    # Родина
    {"es": "la madre", "ua": "мати", "category": "родина"},
    {"es": "el padre", "ua": "батько", "category": "родина"},
    {"es": "el hermano", "ua": "брат", "category": "родина"},
    {"es": "la hermana", "ua": "сестра", "category": "родина"},
    # Дієслова
    {"es": "hablar", "ua": "говорити", "category": "дієслова"},
    {"es": "comer", "ua": "їсти", "category": "дієслова"},
    {"es": "vivir", "ua": "жити", "category": "дієслова"},
    {"es": "trabajar", "ua": "працювати", "category": "дієслова"},
    {"es": "estudiar", "ua": "вчитися", "category": "дієслова"},
    {"es": "ir", "ua": "йти/їхати", "category": "дієслова"},
    {"es": "tener", "ua": "мати", "category": "дієслова"},
    {"es": "ser", "ua": "бути (постійно)", "category": "дієслова"},
    {"es": "estar", "ua": "бути (тимчасово)", "category": "дієслова"},
    # Місця
    {"es": "la casa", "ua": "будинок", "category": "місця"},
    {"es": "la ciudad", "ua": "місто", "category": "місця"},
    {"es": "la calle", "ua": "вулиця", "category": "місця"},
    {"es": "el trabajo", "ua": "робота", "category": "місця"},
    {"es": "la tienda", "ua": "магазин", "category": "місця"},
    # Транспорт
    {"es": "el coche", "ua": "машина", "category": "транспорт"},
    {"es": "el autobús", "ua": "автобус", "category": "транспорт"},
    {"es": "el tren", "ua": "поїзд", "category": "транспорт"},
    {"es": "la bicicleta", "ua": "велосипед", "category": "транспорт"},
]

# ══════════════════════════════════════════════════════════
# БАЗА ДАНИХ КОРИСТУВАЧІВ (in-memory)
# ══════════════════════════════════════════════════════════

users_db = {}

def get_user(user_id: int) -> dict:
    uid = str(user_id)
    if uid not in users_db:
        users_db[uid] = {
            "xp": 0,
            "streak": 0,
            "last_activity": None,
            "completed_lessons": [],
            "quiz_scores": {},
            "flashcard_index": 0,
            "known_cards": [],
            "state": None,
            "current_quiz": None,
            "quiz_q_index": 0,
            "quiz_correct": 0,
        }
    return users_db[uid]

def add_xp(user_id: int, amount: int):
    u = get_user(user_id)
    u["xp"] += amount
    today = datetime.now().date().isoformat()
    if u["last_activity"] != today:
        u["streak"] += 1
        u["last_activity"] = today

def get_level(xp: int) -> tuple:
    levels = [
        (0,   "🥚 Початківець"),
        (100, "🐣 Новачок"),
        (300, "📚 Студент"),
        (600, "🎓 Учень"),
        (1000,"⭐ Знавець"),
        (1500,"🌟 Майстер"),
        (2500,"🏆 Експерт"),
    ]
    for i in range(len(levels)-1, -1, -1):
        if xp >= levels[i][0]:
            return levels[i][1], levels[i+1][0] if i < len(levels)-1 else xp
    return levels[0][1], levels[1][0]

# ══════════════════════════════════════════════════════════
# КЛАВІАТУРИ
# ══════════════════════════════════════════════════════════

def main_menu_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📖 Уроки", callback_data="menu_lessons"),
         InlineKeyboardButton("🃏 Флешкарти", callback_data="menu_flash")],
        [InlineKeyboardButton("🧠 Квіз", callback_data="menu_quiz"),
         InlineKeyboardButton("📊 Прогрес", callback_data="menu_progress")],
        [InlineKeyboardButton("📝 Словник", callback_data="menu_vocab")],
    ])

def back_kb(to="menu_main"):
    return InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Назад", callback_data=to)]])

# ══════════════════════════════════════════════════════════
# HANDLERS
# ══════════════════════════════════════════════════════════

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    get_user(user.id)
    text = (
        f"🇪🇸 *¡Hola, {user.first_name}!*\n\n"
        "Ласкаво просимо до бота для вивчення іспанської!\n\n"
        "Тут ти знайдеш:\n"
        "📖 *Уроки* — теорія з нуля\n"
        "🃏 *Флешкарти* — слова з перекладом\n"
        "🧠 *Квіз* — перевір себе\n"
        "📊 *Прогрес* — твої досягнення\n\n"
        "З чого починаємо? 👇"
    )
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=main_menu_kb())

async def handle_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    uid = q.from_user.id

    # ── ГОЛОВНЕ МЕНЮ ──────────────────────────────────────
    if data == "menu_main":
        await q.edit_message_text(
            "🇪🇸 *Головне меню*\n\nОбирай що хочеш робити:",
            parse_mode="Markdown", reply_markup=main_menu_kb()
        )

    # ── УРОКИ ─────────────────────────────────────────────
    elif data == "menu_lessons":
        u = get_user(uid)
        rows = []
        for i, l in enumerate(LESSONS):
            done = l["id"] in u["completed_lessons"]
            mark = "✅" if done else f"{l['id']}."
            rows.append([InlineKeyboardButton(f"{mark} {l['title']}", callback_data=f"lesson_{l['id']}")])
        rows.append([InlineKeyboardButton("◀️ Назад", callback_data="menu_main")])
        await q.edit_message_text(
            "📖 *Уроки*\n\nОбирай урок:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(rows)
        )

    elif data.startswith("lesson_"):
        lid = int(data.split("_")[1])
        lesson = next(l for l in LESSONS if l["id"] == lid)
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🧠 Пройти квіз по уроку", callback_data=f"quiz_lesson_{lid}")],
            [InlineKeyboardButton("◀️ До уроків", callback_data="menu_lessons")],
        ])
        await q.edit_message_text(lesson["theory"], parse_mode="Markdown", reply_markup=kb)

    # ── ФЛЕШКАРТИ ─────────────────────────────────────────
    elif data == "menu_flash":
        await show_flashcard(q, uid, mode="es")

    elif data.startswith("flash_"):
        action = data.split("_")[1]
        u = get_user(uid)
        if action == "show":
            await show_flashcard(q, uid, reveal=True)
        elif action == "know":
            idx = u["flashcard_index"]
            card = FLASHCARDS[idx % len(FLASHCARDS)]
            if card["es"] not in u["known_cards"]:
                u["known_cards"].append(card["es"])
            add_xp(uid, 5)
            u["flashcard_index"] = (idx + 1) % len(FLASHCARDS)
            await show_flashcard(q, uid, mode="es")
        elif action == "learn":
            u["flashcard_index"] = (u["flashcard_index"] + 1) % len(FLASHCARDS)
            await show_flashcard(q, uid, mode="es")
        elif action == "random":
            u["flashcard_index"] = random.randint(0, len(FLASHCARDS)-1)
            await show_flashcard(q, uid, mode="es")

    # ── КВІЗ ──────────────────────────────────────────────
    elif data == "menu_quiz":
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{l['title']}", callback_data=f"quiz_lesson_{l['id']}")]
            for l in LESSONS
        ] + [[InlineKeyboardButton("🎲 Випадковий", callback_data="quiz_random")],
             [InlineKeyboardButton("◀️ Назад", callback_data="menu_main")]])
        await q.edit_message_text("🧠 *Квіз*\n\nОбирай тему:", parse_mode="Markdown", reply_markup=kb)

    elif data.startswith("quiz_lesson_") or data == "quiz_random":
        if data == "quiz_random":
            lesson = random.choice(LESSONS)
        else:
            lid = int(data.split("_")[2])
            lesson = next(l for l in LESSONS if l["id"] == lid)
        u = get_user(uid)
        u["current_quiz"] = lesson["quiz"]
        u["quiz_q_index"] = 0
        u["quiz_correct"] = 0
        await show_quiz_question(q, uid)

    elif data == "quiz_next":
        await show_quiz_question(q, uid)

    elif data.startswith("ans_"):
        await handle_quiz_answer(q, uid, data)

    # ── ПРОГРЕС ───────────────────────────────────────────
    elif data == "menu_progress":
        u = get_user(uid)
        level_name, next_xp = get_level(u["xp"])
        bar_len = 10
        if next_xp > 0:
            filled = int((u["xp"] % next_xp) / next_xp * bar_len) if next_xp > u["xp"] else bar_len
        else:
            filled = bar_len
        bar = "█" * filled + "░" * (bar_len - filled)
        lessons_done = len(u["completed_lessons"])
        cards_known = len(u["known_cards"])

        text = (
            f"📊 *Твій прогрес*\n\n"
            f"🏅 Рівень: *{level_name}*\n"
            f"⭐ XP: *{u['xp']}*\n"
            f"[{bar}]\n\n"
            f"🔥 Серія днів: *{u['streak']}*\n"
            f"📖 Уроків пройдено: *{lessons_done}/{len(LESSONS)}*\n"
            f"🃏 Слів вивчено: *{cards_known}/{len(FLASHCARDS)}*\n\n"
        )
        if lessons_done == 0:
            text += "💡 Починай з першого уроку!"
        elif lessons_done < len(LESSONS):
            text += f"💪 Продовжуй! Ще {len(LESSONS)-lessons_done} уроків"
        else:
            text += "🎉 Усі уроки пройдено! ¡Fantástico!"

        await q.edit_message_text(text, parse_mode="Markdown", reply_markup=back_kb())

    # ── СЛОВНИК ───────────────────────────────────────────
    elif data == "menu_vocab":
        categories = {}
        for c in FLASHCARDS:
            cat = c["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(c)

        text = "📝 *Словник*\n\n"
        for cat, words in categories.items():
            text += f"*{cat.capitalize()}:*\n"
            for w in words[:5]:
                text += f"  • {w['es']} — {w['ua']}\n"
            if len(words) > 5:
                text += f"  _...та ще {len(words)-5}_\n"
            text += "\n"

        await q.edit_message_text(text, parse_mode="Markdown", reply_markup=back_kb())


async def show_flashcard(q, uid: int, reveal=False, mode="es"):
    u = get_user(uid)
    idx = u["flashcard_index"] % len(FLASHCARDS)
    card = FLASHCARDS[idx]
    total = len(FLASHCARDS)
    known = len(u["known_cards"])

    if not reveal:
        text = (
            f"🃏 *Флешкарта {idx+1}/{total}*\n"
            f"_Категорія: {card['category']}_\n\n"
            f"🇪🇸 *{card['es']}*\n\n"
            f"Знаєш переклад?"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("👁 Показати переклад", callback_data="flash_show")],
            [InlineKeyboardButton("➡️ Пропустити", callback_data="flash_learn"),
             InlineKeyboardButton("🎲 Випадкова", callback_data="flash_random")],
            [InlineKeyboardButton("◀️ Меню", callback_data="menu_main")],
        ])
    else:
        is_known = card["es"] in u["known_cards"]
        text = (
            f"🃏 *Флешкарта {idx+1}/{total}*\n"
            f"_Категорія: {card['category']}_\n\n"
            f"🇪🇸 *{card['es']}*\n"
            f"🇺🇦 *{card['ua']}*\n\n"
            f"✅ Вивчено: {known}/{total}"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Знаю!", callback_data="flash_know"),
             InlineKeyboardButton("🔄 Вчити ще", callback_data="flash_learn")],
            [InlineKeyboardButton("◀️ Меню", callback_data="menu_main")],
        ])

    await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)


async def show_quiz_question(q, uid: int):
    u = get_user(uid)
    quiz = u["current_quiz"]
    qi = u["quiz_q_index"]

    if qi >= len(quiz):
        # Квіз завершено
        correct = u["quiz_correct"]
        total = len(quiz)
        xp_earned = correct * 20
        add_xp(uid, xp_earned)

        pct = int(correct / total * 100)
        if pct == 100:
            result = "🏆 Ідеально! ¡Perfecto!"
        elif pct >= 66:
            result = "👍 Добре! ¡Muy bien!"
        else:
            result = "📚 Треба повторити! ¡Practica más!"

        text = (
            f"✅ *Квіз завершено!*\n\n"
            f"Правильних відповідей: *{correct}/{total}*\n"
            f"Результат: {pct}%\n\n"
            f"{result}\n\n"
            f"⭐ +{xp_earned} XP"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Ще раз", callback_data="menu_quiz")],
            [InlineKeyboardButton("◀️ Меню", callback_data="menu_main")],
        ])
        await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
        return

    question = quiz[qi]
    options = question["options"].copy()
    random.shuffle(options)

    text = (
        f"🧠 *Питання {qi+1}/{len(quiz)}*\n\n"
        f"{question['q']}"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(opt, callback_data=f"ans_{opt}")] for opt in options
    ])
    await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)


async def handle_quiz_answer(q, uid: int, data: str):
    answer = data[4:]  # remove "ans_"
    u = get_user(uid)
    quiz = u["current_quiz"]
    qi = u["quiz_q_index"]
    question = quiz[qi]

    if answer == question["a"]:
        u["quiz_correct"] += 1
        feedback = "✅ *Правильно!* ¡Correcto!"
    else:
        feedback = f"❌ *Неправильно.*\nПравильна відповідь: *{question['a']}*"

    u["quiz_q_index"] += 1

    # Mark lesson as completed if this was lesson quiz
    # (simplified: mark based on quiz content match)

    text = f"{feedback}\n\n_Питання {qi+1} з {len(quiz)}_"
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("➡️ Далі", callback_data="quiz_next")]
    ])
    await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)


async def handle_callback_quiz_next(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    pass  # handled in main callback





if __name__ == "__main__":
  
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    print("🤖 Бот запущено!")
    app.run_polling(drop_pending_updates=True)

# This file is complete above
