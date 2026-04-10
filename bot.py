import os
import random
import asyncio
from datetime import date
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)

TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# ══════════════════════════════════════════════════════════
# ПЕРЕКЛАДИ ІНТЕРФЕЙСУ
# ══════════════════════════════════════════════════════════
UI = {
    "ua": {
        "welcome": "Ласкаво просимо до бота для вивчення іспанської!",
        "choose": "З чого починаємо? 👇",
        "lessons": "📖 Уроки",
        "flashcards": "🃏 Флешкарти",
        "quiz": "🧠 Квіз",
        "game": "🎮 Гра",
        "progress": "📊 Прогрес",
        "notify": "🔔 Нагадування",
        "vocab": "📚 Словник",
        "lang": "🇷🇺 РУ",
        "main_menu": "◀️ Головне меню",
        "back": "◀️ Назад",
        "lessons_title": "📖 *Уроки*\n\nОбирай урок:",
        "quiz_title": "🧠 *Квіз*\n\nОбирай тему:",
        "vocab_title": "📚 *Словник по темах*\n\nОбирай тему:",
        "game_title": "🎮 *Ігровий режим*\n\nОбери тип:",
        "game_mc": "🎯 Вгадай переклад",
        "game_write": "✍️ Напиши слово",
        "notify_title": "🔔 *Нагадування*",
        "notify_on": "🔔 Увімкнути",
        "notify_off": "🔕 Вимкнути",
        "notify_time": "⏰ Змінити час",
        "notify_status_on": "🟢 Увімкнено",
        "notify_status_off": "🔴 Вимкнено",
        "question": "🧠 *Питання {i}/{total}*\n\n{q}",
        "correct": "✅ *Правильно!* ¡Correcto!\n\n✔️ *{a}*",
        "wrong": "❌ *Неправильно.*\nТи обрав: _{ans}_\n✅ Правильно: *{a}*",
        "next": "➡️ Далі",
        "quiz_done": "✅ *Квіз завершено!*\n\nПравильно: *{c}/{t}* ({p}%)\n{e}\n\n⭐ +{xp} XP!",
        "again": "🔄 Ще раз",
        "progress_title": "📊 *Твій прогрес*",
        "level": "🏅 Рівень",
        "streak": "🔥 Серія",
        "days": "днів",
        "lessons_done": "📖 Уроків",
        "words_done": "🃏 Слів вивчено",
        "flash_know": "Знаєш переклад?",
        "flash_show": "👁 Показати",
        "flash_knew": "✅ Знаю!",
        "flash_next": "🔄 Далі",
        "flash_random": "🎲 Випадкова",
        "menu": "Головне меню 👇",
        "words_title": "📖 *{theme}*\n\n",
        "word_line": "🇪🇸 *{es}* — {ua}\n💬 _{example}_\n\n",
        "quiz_words": "🧠 Квіз по темі",
        "flash_words": "🃏 Флешкарти теми",
        "quiz_random": "🎲 Випадковий урок",
        "try_again": "🔄 Ще раз (нові питання!)",
        "wrote": "Ти написав",
        "correct_ans": "Правильно",
        "skipped": "⏭ Пропущено",
        "skip": "⏭ Пропустити",
        "game_done": "🎮 *Гру завершено!*\n\nПравильно: *{c}/{t}* ({p}%)\n⭐ +{xp} XP",
        "translate_q": "Як перекласти?",
        "write_q": "Напиши іспанською:",
        "all_lessons": "Починай з першого уроку! 💡",
        "some_lessons": "Ще {n} уроків! 💪",
        "all_done": "Усі уроки пройдено! ¡Fantástico! 🎉",
    },
    "ru": {
        "welcome": "Добро пожаловать в бот для изучения испанского!",
        "choose": "С чего начинаем? 👇",
        "lessons": "📖 Уроки",
        "flashcards": "🃏 Карточки",
        "quiz": "🧠 Квиз",
        "game": "🎮 Игра",
        "progress": "📊 Прогресс",
        "notify": "🔔 Напоминания",
        "vocab": "📚 Словарь",
        "lang": "🇺🇦 УКР",
        "main_menu": "◀️ Главное меню",
        "back": "◀️ Назад",
        "lessons_title": "📖 *Уроки*\n\nВыбери урок:",
        "quiz_title": "🧠 *Квиз*\n\nВыбери тему:",
        "vocab_title": "📚 *Словарь по темам*\n\nВыбери тему:",
        "game_title": "🎮 *Игровой режим*\n\nВыбери тип:",
        "game_mc": "🎯 Угадай перевод",
        "game_write": "✍️ Напиши слово",
        "notify_title": "🔔 *Напоминания*",
        "notify_on": "🔔 Включить",
        "notify_off": "🔕 Выключить",
        "notify_time": "⏰ Изменить время",
        "notify_status_on": "🟢 Включено",
        "notify_status_off": "🔴 Выключено",
        "question": "🧠 *Вопрос {i}/{total}*\n\n{q}",
        "correct": "✅ *Правильно!* ¡Correcto!\n\n✔️ *{a}*",
        "wrong": "❌ *Неправильно.*\nТы выбрал: _{ans}_\n✅ Правильно: *{a}*",
        "next": "➡️ Далее",
        "quiz_done": "✅ *Квиз завершён!*\n\nПравильно: *{c}/{t}* ({p}%)\n{e}\n\n⭐ +{xp} XP!",
        "again": "🔄 Ещё раз",
        "progress_title": "📊 *Твой прогресс*",
        "level": "🏅 Уровень",
        "streak": "🔥 Серия",
        "days": "дней",
        "lessons_done": "📖 Уроков",
        "words_done": "🃏 Слов изучено",
        "flash_know": "Знаешь перевод?",
        "flash_show": "👁 Показать",
        "flash_knew": "✅ Знаю!",
        "flash_next": "🔄 Далее",
        "flash_random": "🎲 Случайная",
        "menu": "Главное меню 👇",
        "words_title": "📖 *{theme}*\n\n",
        "word_line": "🇪🇸 *{es}* — {ru}\n💬 _{example}_\n\n",
        "quiz_words": "🧠 Квиз по теме",
        "flash_words": "🃏 Карточки темы",
        "quiz_random": "🎲 Случайный урок",
        "try_again": "🔄 Ещё раз (новые вопросы!)",
        "wrote": "Ты написал",
        "correct_ans": "Правильно",
        "skipped": "⏭ Пропущено",
        "skip": "⏭ Пропустить",
        "game_done": "🎮 *Игра завершена!*\n\nПравильно: *{c}/{t}* ({p}%)\n⭐ +{xp} XP",
        "translate_q": "Как перевести?",
        "write_q": "Напиши по-испански:",
        "all_lessons": "Начинай с первого урока! 💡",
        "some_lessons": "Ещё {n} уроков! 💪",
        "all_done": "Все уроки пройдены! ¡Fantástico! 🎉",
    }
}

def t(uid, key, **kwargs):
    lang = users_db.get(str(uid), {}).get("lang", "ua")
    text = UI[lang].get(key, UI["ua"].get(key, key))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except:
            pass
    return text

# ══════════════════════════════════════════════════════════
# УРОКИ
# ══════════════════════════════════════════════════════════
LESSONS = [
    {
        "id":1,"title":"🔤 Урок 1: Привітання / Приветствие",
        "theory":(
            "━━━━━━━━━━━━━━━━━━━━━━\n📖 *Урок 1: Привітання*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🌅 *Hola* — Привіт / Привет\n🌄 *Buenos días* — Доброго ранку / Доброе утро\n"
            "☀️ *Buenas tardes* — Добрий день / Добрый день\n🌙 *Buenas noches* — Добрий вечір / Добрый вечер\n"
            "👋 *¿Cómo estás?* — Як справи? / Как дела?\n😊 *Bien, gracias* — Добре, дякую / Хорошо, спасибо\n"
            "🤝 *Mucho gusto* — Приємно познайомитись / Приятно познакомиться\n"
            "💬 *Hasta luego* — До зустрічі / До свидания\n"
            "🙏 *Por favor* — Будь ласка / Пожалуйста\n"
            "💙 *Gracias* — Дякую / Спасибо\n\n"
            "💡 *tú* = неформальне ти / неформальное ты\n💡 *usted* = формальне Ви / формальное Вы"
        ),
        "all_questions":[
            {"q":"Як сказати 'Привіт'? / Как сказать 'Привет'?","a":"Hola","wrong":["Adiós","Gracias","Buenos días","Lo siento","Por favor"]},
            {"q":"Що означає 'Buenos días'? / Что значит 'Buenos días'?","a":"Доброго ранку / Доброе утро","wrong":["Добрий вечір","Добрий день","До побачення","Як справи?","Дякую"]},
            {"q":"Як спитати 'Як справи?' / Как спросить 'Как дела'?","a":"¿Cómo estás?","wrong":["¿Qué hora es?","¿Cómo te llamas?","¿Dónde estás?","¿Cuántos años tienes?","Hasta luego"]},
            {"q":"Що означає 'Mucho gusto'?","a":"Приємно познайомитись","wrong":["Дякую","Добре","До побачення","Вибачте","Будь ласка"]},
            {"q":"Як сказати 'До зустрічі'?","a":"Hasta luego","wrong":["Adiós","Hola","Gracias","Por favor","De nada"]},
            {"q":"Що означає 'Buenas noches'?","a":"Добрий вечір/ніч","wrong":["Доброго ранку","Добрий день","Привіт","До побачення","Як справи?"]},
            {"q":"Як сказати 'Дякую'?","a":"Gracias","wrong":["Por favor","De nada","Lo siento","Hola","Adiós"]},
            {"q":"Як сказати 'Будь ласка'?","a":"Por favor","wrong":["Gracias","De nada","Lo siento","Mucho gusto","Hola"]},
            {"q":"Що означає 'Bien, gracias'?","a":"Добре, дякую","wrong":["Як справи?","Вибачте","До побачення","Приємно познайомитись","Будь ласка"]},
            {"q":"Яке звернення формальне?","a":"usted","wrong":["tú","yo","él","ella","nosotros"]},
            {"q":"Що означає 'Buenas tardes'?","a":"Добрий день","wrong":["Доброго ранку","Добрий вечір","Привіт","До побачення","Дякую"]},
            {"q":"Як сказати 'Вибачте'?","a":"Lo siento","wrong":["Gracias","Por favor","Hola","Adiós","De nada"]},
        ]
    },
    {
        "id":2,"title":"🔢 Урок 2: Числа / Числа",
        "theory":(
            "━━━━━━━━━━━━━━━━━━━━━━\n📖 *Урок 2: Числа 1–20*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "1️⃣ uno  2️⃣ dos  3️⃣ tres  4️⃣ cuatro  5️⃣ cinco\n"
            "6️⃣ seis  7️⃣ siete  8️⃣ ocho  9️⃣ nueve  🔟 diez\n\n"
            "1️⃣1️⃣ once  1️⃣2️⃣ doce  1️⃣3️⃣ trece\n"
            "1️⃣4️⃣ catorce  1️⃣5️⃣ quince\n"
            "1️⃣6️⃣ dieciséis  1️⃣7️⃣ diecisiete\n"
            "1️⃣8️⃣ dieciocho  1️⃣9️⃣ diecinueve  2️⃣0️⃣ veinte\n\n"
            "💡 16-19 = dieci + (6-9)"
        ),
        "all_questions":[
            {"q":"Як буде '5'? / Как будет '5'?","a":"cinco","wrong":["cuatro","seis","siete","tres","ocho"]},
            {"q":"Що означає 'diez'?","a":"10","wrong":["7","8","9","11","6"]},
            {"q":"Як буде '15'?","a":"quince","wrong":["catorce","trece","dieciséis","once","doce"]},
            {"q":"Що означає 'veinte'?","a":"20","wrong":["10","15","12","18","19"]},
            {"q":"Як буде '3'?","a":"tres","wrong":["dos","cuatro","uno","cinco","seis"]},
            {"q":"Що означає 'nueve'?","a":"9","wrong":["6","7","8","10","5"]},
            {"q":"Як буде '12'?","a":"doce","wrong":["once","trece","catorce","quince","diez"]},
            {"q":"Що означає 'ocho'?","a":"8","wrong":["6","7","9","10","5"]},
            {"q":"Як буде '17'?","a":"diecisiete","wrong":["dieciséis","dieciocho","diecinueve","veinte","quince"]},
            {"q":"Що означає 'catorce'?","a":"14","wrong":["13","15","12","16","11"]},
            {"q":"Як буде '1'?","a":"uno","wrong":["dos","tres","cuatro","cinco","seis"]},
            {"q":"Що означає 'siete'?","a":"7","wrong":["5","6","8","9","10"]},
        ]
    },
    {
        "id":3,"title":"🎨 Урок 3: Кольори / Цвета",
        "theory":(
            "━━━━━━━━━━━━━━━━━━━━━━\n📖 *Урок 3: Кольори / Цвета*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "❤️ *rojo* — червоний / красный\n💛 *amarillo* — жовтий / жёлтый\n"
            "💙 *azul* — синій / синий\n💚 *verde* — зелений / зелёный\n"
            "🤍 *blanco* — білий / белый\n🖤 *negro* — чорний / чёрный\n"
            "🟠 *naranja* — помаранчевий / оранжевый\n🟣 *morado* — фіолетовий / фиолетовый\n"
            "🩷 *rosa* — рожевий / розовый\n🟤 *marrón* — коричневий / коричневый\n⚪ *gris* — сірий / серый\n\n"
            "💡 El coche *rojo* (м.р.) — La casa *roja* (ж.р.)"
        ),
        "all_questions":[
            {"q":"Як буде 'синій'?","a":"azul","wrong":["verde","rojo","amarillo","blanco","negro"]},
            {"q":"Що означає 'negro'?","a":"чорний / чёрный","wrong":["білий","сірий","коричневий","фіолетовий","рожевий"]},
            {"q":"Як буде 'зелений'?","a":"verde","wrong":["blanco","naranja","rosa","azul","rojo"]},
            {"q":"Що означає 'amarillo'?","a":"жовтий / жёлтый","wrong":["помаранчевий","червоний","рожевий","коричневий","синій"]},
            {"q":"Як буде 'білий'?","a":"blanco","wrong":["negro","rojo","verde","azul","morado"]},
            {"q":"Що означає 'rosa'?","a":"рожевий / розовый","wrong":["червоний","фіолетовий","помаранчевий","коричневий","сірий"]},
            {"q":"Як буде 'коричневий'?","a":"marrón","wrong":["gris","negro","morado","naranja","rojo"]},
            {"q":"Що означає 'gris'?","a":"сірий / серый","wrong":["коричневий","чорний","білий","фіолетовий","рожевий"]},
            {"q":"Як буде 'помаранчевий'?","a":"naranja","wrong":["rojo","amarillo","rosa","marrón","verde"]},
            {"q":"Яке закінчення у 'rojo' для ж.р.?","a":"roja","wrong":["roje","rojos","rojas","roji","rojо"]},
            {"q":"Як буде 'фіолетовий'?","a":"morado","wrong":["rosa","azul","turquesa","celeste","gris"]},
            {"q":"Що означає 'marrón'?","a":"коричневий / коричневый","wrong":["сірий","бежевий","чорний","темний","золотий"]},
        ]
    },
    {
        "id":4,"title":"👨‍👩‍👧 Урок 4: Родина / Семья",
        "theory":(
            "━━━━━━━━━━━━━━━━━━━━━━\n📖 *Урок 4: Родина / Семья*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "👨 *el padre* — батько / отец\n👩 *la madre* — мати / мать\n"
            "👦 *el hijo* — син / сын\n👧 *la hija* — дочка / дочь\n"
            "👴 *el abuelo* — дідусь / дедушка\n👵 *la abuela* — бабуся / бабушка\n"
            "👱 *el hermano* — брат / брат\n👱‍♀️ *la hermana* — сестра / сестра\n"
            "👨‍💼 *el tío* — дядько / дядя\n👩‍💼 *la tía* — тітка / тётя\n\n"
            "💡 *el* = чоловічий рід / мужской род\n💡 *la* = жіночий рід / женский род"
        ),
        "all_questions":[
            {"q":"Як буде 'мати'?","a":"la madre","wrong":["el padre","la hija","la abuela","la hermana","la tía"]},
            {"q":"Що означає 'el hermano'?","a":"брат","wrong":["сестра","дядько","батько","дідусь","кузен"]},
            {"q":"Який артикль у 'hijo'?","a":"el","wrong":["la","los","las","un","una"]},
            {"q":"Що означає 'la abuela'?","a":"бабуся / бабушка","wrong":["дідусь","мати","тітка","сестра","дочка"]},
            {"q":"Як буде 'дочка'?","a":"la hija","wrong":["el hijo","la hermana","la madre","la tía","la abuela"]},
            {"q":"Що означає 'el tío'?","a":"дядько / дядя","wrong":["тітка","брат","батько","дідусь","кузен"]},
            {"q":"Як буде 'дідусь'?","a":"el abuelo","wrong":["la abuela","el padre","el tío","el hermano","el hijo"]},
            {"q":"Що означає 'los padres'?","a":"батьки / родители","wrong":["діти","брати","дідусь і бабуся","дядьки","сестри"]},
            {"q":"Як буде 'сестра'?","a":"la hermana","wrong":["el hermano","la hija","la madre","la tía","la abuela"]},
            {"q":"Як буде 'тітка'?","a":"la tía","wrong":["el tío","la hermana","la madre","la abuela","la hija"]},
            {"q":"Що означає 'el padre'?","a":"батько / отец","wrong":["дідусь","брат","дядько","син","чоловік"]},
            {"q":"Як буде 'бабуся'?","a":"la abuela","wrong":["el abuelo","la madre","la tía","la hermana","la hija"]},
        ]
    },
    {
        "id":5,"title":"🍎 Урок 5: Їжа / Еда",
        "theory":(
            "━━━━━━━━━━━━━━━━━━━━━━\n📖 *Урок 5: Їжа / Еда*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🍞 *el pan* — хліб / хлеб\n🥛 *la leche* — молоко / молоко\n"
            "🍳 *el huevo* — яйце / яйцо\n🍗 *el pollo* — курка / курица\n"
            "🐟 *el pescado* — риба / рыба\n🍚 *el arroz* — рис / рис\n"
            "🥗 *la ensalada* — салат / салат\n☕ *el café* — кава / кофе\n"
            "💧 *el agua* — вода / вода\n🍷 *el vino* — вино / вино\n\n"
            "💡 *Tengo hambre* — Я голодний/а / Я голоден\n"
            "💡 *¡Buen provecho!* — Смачного! / Приятного аппетита!"
        ),
        "all_questions":[
            {"q":"Як буде 'хліб'?","a":"el pan","wrong":["la leche","el agua","el café","el arroz","el vino"]},
            {"q":"Що означає 'el pollo'?","a":"курка / курица","wrong":["риба","яйце","рис","хліб","салат"]},
            {"q":"Як сказати 'Я голодний'?","a":"Tengo hambre","wrong":["Tengo sed","Tengo frío","Tengo sueño","Tengo miedo","Tengo razón"]},
            {"q":"Що означає 'el agua'?","a":"вода / вода","wrong":["молоко","кава","вино","сік","чай"]},
            {"q":"Як буде 'кава'?","a":"el café","wrong":["el vino","la leche","el agua","el pan","el arroz"]},
            {"q":"Що означає 'la leche'?","a":"молоко / молоко","wrong":["вода","кава","сік","вино","чай"]},
            {"q":"Як буде 'риба'?","a":"el pescado","wrong":["el pollo","el arroz","el huevo","el pan","el queso"]},
            {"q":"Як буде 'яйце'?","a":"el huevo","wrong":["el pan","el queso","el arroz","el pollo","la leche"]},
            {"q":"Що означає 'la ensalada'?","a":"салат / салат","wrong":["суп","рис","хліб","сир","курка"]},
            {"q":"Що означає '¡Buen provecho!'?","a":"Смачного! / Приятного аппетита!","wrong":["Будь ласка!","Дякую!","На здоров'я!","Привіт!","До побачення!"]},
            {"q":"Як буде 'вино'?","a":"el vino","wrong":["el café","la leche","el agua","el arroz","el pan"]},
            {"q":"Що означає 'el arroz'?","a":"рис / рис","wrong":["хліб","картопля","макарони","курка","яйце"]},
        ]
    },
    {
        "id":6,"title":"🕐 Урок 6: Час / Время",
        "theory":(
            "━━━━━━━━━━━━━━━━━━━━━━\n📖 *Урок 6: Час і дні тижня*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Пн *lunes* | Вт *martes* | Ср *miércoles*\n"
            "Чт *jueves* | Пт *viernes* | Сб *sábado* | Нд *domingo*\n\n"
            "⏰ *¿Qué hora es?* — Котра година? / Который час?\n"
            "• *Es la una* — Перша година / Первый час\n"
            "• *Son las dos* — Друга година / Два часа\n"
            "• *Son las tres y media* — Пів на четверту / Полтретьего\n\n"
            "💡 'es' для 1-ї год, 'son' для решти!"
        ),
        "all_questions":[
            {"q":"Як буде 'понеділок'?","a":"lunes","wrong":["martes","miércoles","jueves","viernes","sábado"]},
            {"q":"Що означає '¿Qué hora es?'","a":"Котра година? / Который час?","wrong":["Який день?","Яке число?","Як справи?","Де ти?","Скільки коштує?"]},
            {"q":"Як сказати 'Друга година'?","a":"Son las dos","wrong":["Es la dos","Es las dos","Son la dos","Son dos","Es dos"]},
            {"q":"Який день — 'viernes'?","a":"П'ятниця / Пятница","wrong":["Четвер","Субота","Середа","Неділя","Понеділок"]},
            {"q":"Як буде 'неділя'?","a":"domingo","wrong":["sábado","viernes","lunes","martes","jueves"]},
            {"q":"Що означає 'miércoles'?","a":"Середа / Среда","wrong":["Вівторок","Четвер","П'ятниця","Субота","Понеділок"]},
            {"q":"Як сказати 'Перша година'?","a":"Es la una","wrong":["Son la una","Es las una","Son las una","Es uno","Son uno"]},
            {"q":"Що означає 'sábado'?","a":"Субота / Суббота","wrong":["Неділя","П'ятниця","Четвер","Середа","Понеділок"]},
            {"q":"Як буде 'вівторок'?","a":"martes","wrong":["lunes","miércoles","jueves","viernes","domingo"]},
            {"q":"Що означає 'jueves'?","a":"Четвер / Четверг","wrong":["Середа","П'ятниця","Вівторок","Субота","Понеділок"]},
            {"q":"Як сказати 'пів на четверту'?","a":"Son las tres y media","wrong":["Son las cuatro y media","Es la tres y media","Son las tres menos media","Son tres y media","Es tres y media"]},
            {"q":"Як буде 'субота'?","a":"sábado","wrong":["domingo","viernes","jueves","miércoles","martes"]},
        ]
    },
    {
        "id":7,"title":"🔵 Урок 7: SER і ESTAR",
        "theory":(
            "━━━━━━━━━━━━━━━━━━━━━━\n📖 *Урок 7: SER і ESTAR*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Обидва = 'бути' / Оба = 'быть', але різні!\n\n"
            "*SER* — постійні риси / постоянные черты:\n"
            "yo *soy* | tú *eres* | él *es*\n"
            "nosotros *somos* | ellos *son*\n\n"
            "*ESTAR* — стан, місце / состояние, место:\n"
            "yo *estoy* | tú *estás* | él *está*\n"
            "nosotros *estamos* | ellos *están*\n\n"
            "💡 *Soy ucraniano* — Я українець / Я украинец\n"
            "💡 *Estoy cansado* — Я втомлений / Я устал\n"
            "💡 *Está en casa* — Він вдома / Он дома"
        ),
        "all_questions":[
            {"q":"Яка форма SER для 'я'?","a":"soy","wrong":["estoy","eres","es","somos","son"]},
            {"q":"Я втомлений = ?","a":"Estoy cansado","wrong":["Soy cansado","Es cansado","Estar cansado","Estás cansado","Somos cansados"]},
            {"q":"Яке дієслово для постійних рис?","a":"SER","wrong":["ESTAR","TENER","HACER","IR","PODER"]},
            {"q":"Яка форма ESTAR для 'він'?","a":"está","wrong":["es","estoy","estás","estamos","están"]},
            {"q":"Він вдома = ?","a":"Está en casa","wrong":["Es en casa","Estoy en casa","Son en casa","Ser en casa","Estás en casa"]},
            {"q":"Яка форма SER для 'ми'?","a":"somos","wrong":["estamos","son","eres","soy","es"]},
            {"q":"Я українець = ?","a":"Soy ucraniano","wrong":["Estoy ucraniano","Es ucraniano","Ser ucraniano","Somos ucranianos","Estás ucraniano"]},
            {"q":"Яке дієслово для місцезнаходження?","a":"ESTAR","wrong":["SER","TENER","IR","HACER","PODER"]},
            {"q":"Яка форма SER для 'вони'?","a":"son","wrong":["están","somos","eres","soy","es"]},
            {"q":"Ми в Польщі = ?","a":"Estamos en Polonia","wrong":["Somos en Polonia","Están en Polonia","Estoy en Polonia","Es en Polonia","Estar en Polonia"]},
            {"q":"Яка форма ESTAR для 'ти'?","a":"estás","wrong":["eres","estoy","está","estamos","están"]},
            {"q":"Яка форма ESTAR для 'ми'?","a":"estamos","wrong":["somos","están","estás","estoy","está"]},
        ]
    },
    {
        "id":8,"title":"🚶 Урок 8: TENER",
        "theory":(
            "━━━━━━━━━━━━━━━━━━━━━━\n📖 *Урок 8: TENER — мати / иметь*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "yo *tengo* | tú *tienes* | él *tiene*\n"
            "nosotros *tenemos* | ellos *tienen*\n\n"
            "💡 *¿Cuántos años tienes?* — Скільки років? / Сколько лет?\n"
            "💡 *Tengo 30 años* — Мені 30 / Мне 30\n\n"
            "*Вирази / Выражения:*\n"
            "• *tener hambre* — бути голодним / быть голодным\n"
            "• *tener sed* — хотіти пити / хотеть пить\n"
            "• *tener sueño* — хотіти спати / хотеть спать\n"
            "• *tener miedo* — боятися / бояться\n"
            "• *tener prisa* — поспішати / торопиться"
        ),
        "all_questions":[
            {"q":"Як сказати 'Мені 25 років'?","a":"Tengo 25 años","wrong":["Soy 25 años","Estoy 25 años","Tiene 25 años","Tienes 25 años","Tenemos 25 años"]},
            {"q":"Яка форма TENER для 'вони'?","a":"tienen","wrong":["tenemos","tiene","tengo","tienes","tener"]},
            {"q":"Що означає 'tener sueño'?","a":"хотіти спати / хотеть спать","wrong":["боятися","хотіти пити","бути голодним","бути правим","поспішати"]},
            {"q":"Яка форма TENER для 'ми'?","a":"tenemos","wrong":["tienen","tengo","tiene","tienes","tener"]},
            {"q":"Як запитати 'Скільки тобі років?'","a":"¿Cuántos años tienes?","wrong":["¿Cómo estás?","¿Qué hora es?","¿Dónde vives?","¿Cómo te llamas?","¿Qué haces?"]},
            {"q":"Що означає 'tener prisa'?","a":"поспішати / торопиться","wrong":["боятися","хотіти пити","бути правим","хотіти спати","бути голодним"]},
            {"q":"Яка форма TENER для 'ти'?","a":"tienes","wrong":["tengo","tiene","tenemos","tienen","tener"]},
            {"q":"Що означає 'tener miedo'?","a":"боятися / бояться","wrong":["поспішати","хотіти пити","бути голодним","хотіти спати","бути правим"]},
            {"q":"Яка форма TENER для 'я'?","a":"tengo","wrong":["tienes","tiene","tenemos","tienen","tener"]},
            {"q":"Я хочу пити = ?","a":"Tengo sed","wrong":["Tengo hambre","Tengo sueño","Tengo miedo","Tengo prisa","Tengo razón"]},
            {"q":"Що означає 'tener razón'?","a":"бути правим / быть правым","wrong":["поспішати","боятися","хотіти пити","бути голодним","хотіти спати"]},
            {"q":"У мене є кішка = ?","a":"Tengo un gato","wrong":["Soy un gato","Estoy un gato","Tiene un gato","Tienes un gato","Hay un gato"]},
        ]
    },
    {
        "id":9,"title":"👤 Урок 9: Займенники / Местоимения",
        "theory":(
            "━━━━━━━━━━━━━━━━━━━━━━\n📖 *Урок 9: Займенники / Местоимения*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "• *yo* — я / я\n• *tú* — ти / ты\n"
            "• *él* — він / он\n• *ella* — вона / она\n"
            "• *usted* — Ви / Вы (формально)\n"
            "• *nosotros* — ми / мы\n• *vosotros* — ви / вы (Іспанія)\n"
            "• *ellos* — вони (ч.р.) / они (м.р.)\n• *ellas* — вони (ж.р.) / они (ж.р.)\n"
            "• *ustedes* — ви / вы (Латинська Америка)\n\n"
            "💡 Займенники часто опускають / Местоимения часто опускают:\n"
            "• *Hablo español* = Я говорю іспанською"
        ),
        "all_questions":[
            {"q":"Як буде 'ми'?","a":"nosotros","wrong":["vosotros","ellos","ustedes","ellas","usted"]},
            {"q":"Що означає 'ella'?","a":"вона / она","wrong":["він","ми","ви","вони","я"]},
            {"q":"Яке 'ви' у Латинській Америці?","a":"ustedes","wrong":["vosotros","usted","ellos","nosotros","tú"]},
            {"q":"Як буде 'вони' (жіночий рід)?","a":"ellas","wrong":["ellos","ustedes","nosotras","vosotras","ella"]},
            {"q":"Що означає 'usted'?","a":"Ви (формально) / Вы (формально)","wrong":["ти","він","вона","ми","вони"]},
            {"q":"Як буде 'він'?","a":"él","wrong":["ella","usted","tú","yo","ellos"]},
            {"q":"Що означає 'vosotros'?","a":"ви (неформально, Іспанія)","wrong":["вони","ми","він","ви (формально)","я"]},
            {"q":"Як буде 'вони' (чоловічий рід)?","a":"ellos","wrong":["ellas","nosotros","ustedes","vosotros","usted"]},
            {"q":"Що означає 'yo'?","a":"я / я","wrong":["ти","він","вона","ми","вони"]},
            {"q":"Яке 'ви' неформальне в Іспанії?","a":"vosotros","wrong":["ustedes","usted","ellos","nosotros","tú"]},
            {"q":"Як буде 'ти'?","a":"tú","wrong":["yo","él","usted","nosotros","vosotros"]},
            {"q":"Займенники в іспанській часто...?","a":"опускають / опускают","wrong":["подвоюють","пишуть першими","змінюють форму","не існують","повторюють"]},
        ]
    },
    {
        "id":10,"title":"📚 Урок 10: Дієслова -AR",
        "theory":(
            "━━━━━━━━━━━━━━━━━━━━━━\n📖 *Урок 10: Дієслова -AR*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "hablar (говорити / говорить):\n"
            "yo habl*o* | tú habl*as* | él habl*a*\n"
            "nosotros habl*amos* | vosotros habl*áis* | ellos habl*an*\n\n"
            "*Дієслова -AR / Глаголы -AR:*\n"
            "• *trabajar* — працювати / работать\n"
            "• *estudiar* — вчитися / учиться\n"
            "• *caminar* — ходити / ходить\n"
            "• *comprar* — купувати / покупать\n"
            "• *escuchar* — слухати / слушать\n\n"
            "💡 *Trabajo mucho* — Я багато працюю / Я много работаю"
        ),
        "all_questions":[
            {"q":"Яке закінчення 'hablar' для 'yo'?","a":"hablo","wrong":["hablas","habla","hablamos","habláis","hablan"]},
            {"q":"Як сказати 'Ми вчимося'?","a":"Estudiamos","wrong":["Estudian","Estudia","Estudias","Estudio","Estudiais"]},
            {"q":"Яке закінчення -AR для 'ellos'?","a":"-an","wrong":["-o","-as","-a","-amos","-áis"]},
            {"q":"Як сказати 'Він купує'?","a":"Compra","wrong":["Compro","Compras","Compramos","Compran","Compráis"]},
            {"q":"'Trabajar' означає?","a":"працювати / работать","wrong":["говорити","вчитися","ходити","купувати","слухати"]},
            {"q":"Яке закінчення -AR для 'tú'?","a":"-as","wrong":["-o","-a","-amos","-áis","-an"]},
            {"q":"Як сказати 'Я слухаю'?","a":"Escucho","wrong":["Escuchas","Escucha","Escuchamos","Escuchan","Escuchamos"]},
            {"q":"'Caminar' означає?","a":"ходити / ходить","wrong":["бігти","їхати","летіти","плисти","стрибати"]},
            {"q":"Яке закінчення -AR для 'nosotros'?","a":"-amos","wrong":["-an","-as","-a","-áis","-o"]},
            {"q":"Як сказати 'Ти говориш'?","a":"Hablas","wrong":["Hablo","Habla","Hablamos","Habláis","Hablan"]},
            {"q":"'Comprar' означає?","a":"купувати / покупать","wrong":["продавати","дарувати","брати","мати","носити"]},
            {"q":"Яке закінчення -AR для 'vosotros'?","a":"-áis","wrong":["-amos","-an","-as","-a","-o"]},
        ]
    },
    {
        "id":11,"title":"📗 Урок 11: Дієслова -ER і -IR",
        "theory":(
            "━━━━━━━━━━━━━━━━━━━━━━\n📖 *Урок 11: Дієслова -ER і -IR*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "*-ER* (comer — їсти / есть):\n"
            "yo com*o* | tú com*es* | él com*e*\n"
            "nosotros com*emos* | ellos com*en*\n\n"
            "*-IR* (vivir — жити / жить):\n"
            "yo viv*o* | tú viv*es* | él viv*e*\n"
            "nosotros viv*imos* | ellos viv*en*\n\n"
            "• *beber* — пити / пить\n• *leer* — читати / читать\n"
            "• *escribir* — писати / писать\n\n"
            "💡 *Vivo en Polonia* — Я живу в Польщі / Я живу в Польше"
        ),
        "all_questions":[
            {"q":"Яке закінчення -ER для 'tú'?","a":"-es","wrong":["-o","-e","-emos","-en","-as"]},
            {"q":"Як сказати 'Я живу в Польщі'?","a":"Vivo en Polonia","wrong":["Vives en Polonia","Vive en Polonia","Vivimos en Polonia","Vivir en Polonia","Vivía en Polonia"]},
            {"q":"'Leer' означає?","a":"читати / читать","wrong":["писати","пити","їсти","відкривати","говорити"]},
            {"q":"Яке закінчення -IR для 'nosotros'?","a":"-imos","wrong":["-amos","-emos","-en","-is","-an"]},
            {"q":"Як сказати 'Вони п'ють'?","a":"Beben","wrong":["Bebe","Bebes","Bebemos","Bebo","Bebéis"]},
            {"q":"Яке закінчення -ER для 'ellos'?","a":"-en","wrong":["-es","-e","-emos","-éis","-o"]},
            {"q":"'Escribir' означає?","a":"писати / писать","wrong":["читати","говорити","слухати","бачити","думати"]},
            {"q":"Як сказати 'Ти їси'?","a":"Comes","wrong":["Como","Come","Comemos","Coméis","Comen"]},
            {"q":"'Abrir' означає?","a":"відкривати / открывать","wrong":["закривати","брати","давати","бачити","чути"]},
            {"q":"Як сказати 'Ми читаємо'?","a":"Leemos","wrong":["Leen","Lee","Lees","Leo","Leéis"]},
            {"q":"Яке закінчення -ER для 'yo'?","a":"-o","wrong":["-es","-e","-emos","-éis","-en"]},
            {"q":"Яке закінчення -IR для 'ellos'?","a":"-en","wrong":["-es","-e","-imos","-ís","-o"]},
        ]
    },
    {
        "id":12,"title":"🔊 Урок 12: Фонетика",
        "theory":(
            "━━━━━━━━━━━━━━━━━━━━━━\n📖 *Урок 12: Фонетика*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🔤 *ñ* = [нь] — España, mañana\n"
            "🔤 *ll* = [й] — llamar, llover\n"
            "🔤 *rr* = вібруючий [р] — perro, carro\n"
            "🔤 *h* = мовчить / молчит — hola, hacer\n"
            "🔤 *j* = [х] — jardín, jugar\n"
            "🔤 *c+e/i* = [с/θ] — ciudad\n"
            "🔤 *g+e/i* = [х] — gente\n"
            "🔤 *qu* = [к] — queso, querer\n\n"
            "💡 *mañana* = завтра/ранок / завтра/утро\n"
            "💡 *perro* = собака / собака"
        ),
        "all_questions":[
            {"q":"Як читається 'h'?","a":"Мовчить / Молчит","wrong":["як [х]","як [г]","як [h]","як [ф]","як [в]"]},
            {"q":"Як читається 'ñ'?","a":"[нь]","wrong":["[н]","[м]","[ж]","[й]","[х]"]},
            {"q":"Що означає 'mañana'?","a":"завтра / ранок","wrong":["вечір","сьогодні","місяць","рік","тиждень"]},
            {"q":"Як читається 'j'?","a":"[х]","wrong":["[дж]","[ж]","[й]","[г]","мовчить"]},
            {"q":"'ll' читається як?","a":"[й]","wrong":["[л]","[лл]","[в]","[х]","[н]"]},
            {"q":"Як читається 'qu'?","a":"[к]","wrong":["[кв]","[к+у]","[х]","[г]","[ч]"]},
            {"q":"Що означає 'España'?","a":"Іспанія / Испания","wrong":["Франція","Португалія","Мексика","Аргентина","Бразилія"]},
            {"q":"Як читається 'rr'?","a":"вібруючий [р]","wrong":["[р, звичайний]","[рр]","мовчить","[л]","[в]"]},
            {"q":"'perro' означає?","a":"собака / собака","wrong":["кіт","кінь","птах","риба","корова"]},
            {"q":"Як читається 'g' перед 'e' і 'i'?","a":"[х]","wrong":["[г]","[ж]","[й]","[дж]","мовчить"]},
            {"q":"Скільки голосних в іспанській?","a":"5","wrong":["4","6","7","3","8"]},
            {"q":"Буква 'h' в слові 'hola'...","a":"не читається","wrong":["читається як [х]","читається як [г]","читається як [h]","подвоює наступний звук","пом'якшує попередній"]},
        ]
    },
]

# ══════════════════════════════════════════════════════════
# СЛОВНИК ПО ТЕМАХ З ПРИКЛАДАМИ
# ══════════════════════════════════════════════════════════
VOCAB_THEMES = [
    {
        "id":"numbers","title":"🔢 Числа 1–100","level":"A1",
        "words":[
            {"es":"uno","ua":"один","ru":"один","ex":"Tengo *uno* hermano. — У мене один брат."},
            {"es":"dos","ua":"два","ru":"два","ex":"Son *dos* horas. — Це дві години."},
            {"es":"tres","ua":"три","ru":"три","ex":"Necesito *tres* manzanas. — Мені треба три яблука."},
            {"es":"diez","ua":"десять","ru":"десять","ex":"Cuesta *diez* euros. — Коштує десять євро."},
            {"es":"veinte","ua":"двадцять","ru":"двадцять","ex":"Tengo *veinte* años. — Мені двадцять років."},
            {"es":"treinta","ua":"тридцять","ru":"тридцать","ex":"Son *treinta* minutos. — Це тридцять хвилин."},
            {"es":"cuarenta","ua":"сорок","ru":"сорок","ex":"Hay *cuarenta* personas. — Тут сорок людей."},
            {"es":"cincuenta","ua":"п'ятдесят","ru":"пятьдесят","ex":"Cuesta *cincuenta* zlotys. — Коштує п'ятдесят злотих."},
            {"es":"cien","ua":"сто","ru":"сто","ex":"Hay *cien* páginas. — Тут сто сторінок."},
            {"es":"primero","ua":"перший","ru":"первый","ex":"Soy el *primero* en la clase. — Я перший у класі."},
        ],
        "quiz":[
            {"q":"Як буде '40'?","a":"cuarenta","wrong":["treinta","cincuenta","sesenta","veinte","setenta"]},
            {"q":"Що означає 'cien'?","a":"сто","wrong":["десять","двадцять","п'ятдесят","дев'яносто","вісімдесят"]},
            {"q":"Як буде '30'?","a":"treinta","wrong":["veinte","cuarenta","cincuenta","sesenta","cien"]},
            {"q":"Що означає 'cincuenta'?","a":"п'ятдесят","wrong":["сорок","шістдесят","сімдесят","тридцять","вісімдесят"]},
            {"q":"Як буде 'перший'?","a":"primero","wrong":["segundo","tercero","último","cuarto","quinto"]},
            {"q":"Що означає 'treinta'?","a":"тридцять","wrong":["двадцять","сорок","п'ятдесят","шістдесят","сто"]},
            {"q":"Як буде '20'?","a":"veinte","wrong":["diez","treinta","cuarenta","quince","doce"]},
            {"q":"Що означає 'cuarenta'?","a":"сорок","wrong":["тридцять","п'ятдесят","двадцять","шістдесят","сімдесят"]},
            {"q":"У реченні 'Tengo veinte años' — скільки років?","a":"20","wrong":["10","30","40","50","25"]},
            {"q":"Як буде '50'?","a":"cincuenta","wrong":["cuarenta","sesenta","setenta","treinta","veinte"]},
        ]
    },
    {
        "id":"body","title":"🧍 Тіло людини / Тело человека","level":"A1",
        "words":[
            {"es":"la cabeza","ua":"голова","ru":"голова","ex":"Me duele la *cabeza*. — У мене болить голова."},
            {"es":"el ojo","ua":"око","ru":"глаз","ex":"Tiene los *ojos* azules. — У нього блакитні очі."},
            {"es":"la nariz","ua":"ніс","ru":"нос","ex":"Tengo la *nariz* fría. — У мене холодний ніс."},
            {"es":"la boca","ua":"рот","ru":"рот","ex":"Abre la *boca*. — Відкрий рот."},
            {"es":"el oído","ua":"вухо","ru":"ухо","ex":"Me duele el *oído*. — У мене болить вухо."},
            {"es":"el cuello","ua":"шия","ru":"шея","ex":"Lleva un collar en el *cuello*. — Вона носить намисто на шиї."},
            {"es":"el hombro","ua":"плече","ru":"плечо","ex":"Me duele el *hombro*. — У мене болить плече."},
            {"es":"el brazo","ua":"рука (від плеча)","ru":"рука (от плеча)","ex":"Levanta el *brazo*. — Підніми руку."},
            {"es":"la mano","ua":"рука (кисть)","ru":"рука (кисть)","ex":"Dame la *mano*. — Дай мені руку."},
            {"es":"el dedo","ua":"палець","ru":"палец","ex":"Me corté el *dedo*. — Я порізав палець."},
            {"es":"el pecho","ua":"груди","ru":"грудь","ex":"Me duele el *pecho*. — У мене болить груди."},
            {"es":"el estómago","ua":"шлунок","ru":"желудок","ex":"Me duele el *estómago*. — У мене болить шлунок."},
            {"es":"la pierna","ua":"нога","ru":"нога","ex":"Me duele la *pierna*. — У мене болить нога."},
            {"es":"el pie","ua":"стопа","ru":"стопа","ex":"Tengo el *pie* frío. — У мене холодна стопа."},
            {"es":"el corazón","ua":"серце","ru":"сердце","ex":"El *corazón* late rápido. — Серце б'ється швидко."},
        ],
        "quiz":[
            {"q":"Як буде 'голова'?","a":"la cabeza","wrong":["el ojo","la nariz","la boca","el cuello","el hombro"]},
            {"q":"Що означає 'el ojo'?","a":"око / глаз","wrong":["ніс","рот","вухо","щока","лоб"]},
            {"q":"Як буде 'рука (кисть)'?","a":"la mano","wrong":["el brazo","el dedo","el hombro","el pie","la pierna"]},
            {"q":"Що означає 'la pierna'?","a":"нога / нога","wrong":["рука","стопа","палець","плече","шия"]},
            {"q":"Як буде 'серце'?","a":"el corazón","wrong":["el estómago","el pecho","la cabeza","el hombro","el cuello"]},
            {"q":"Що означає 'la boca'?","a":"рот / рот","wrong":["ніс","вухо","очей","щока","зуб"]},
            {"q":"Як буде 'палець'?","a":"el dedo","wrong":["la mano","el pie","el brazo","la pierna","el hombro"]},
            {"q":"Що означає 'el hombro'?","a":"плече / плечо","wrong":["рука","шия","груди","спина","лікоть"]},
            {"q":"У реченні 'Me duele la cabeza' що болить?","a":"голова","wrong":["нога","рука","живіт","спина","шия"]},
            {"q":"Що означає 'el estómago'?","a":"шлунок / желудок","wrong":["серце","груди","нога","голова","спина"]},
        ]
    },
    {
        "id":"animals","title":"🐾 Тварини / Животные","level":"A1",
        "words":[
            {"es":"el perro","ua":"собака","ru":"собака","ex":"Mi *perro* se llama Max. — Мого собаку звати Макс."},
            {"es":"el gato","ua":"кіт","ru":"кот","ex":"El *gato* duerme mucho. — Кіт багато спить."},
            {"es":"el pájaro","ua":"птах","ru":"птица","ex":"El *pájaro* canta bien. — Птах добре співає."},
            {"es":"el caballo","ua":"кінь","ru":"лошадь","ex":"El *caballo* corre rápido. — Кінь швидко бігає."},
            {"es":"la vaca","ua":"корова","ru":"корова","ex":"La *vaca* da leche. — Корова дає молоко."},
            {"es":"el cerdo","ua":"свиня","ru":"свинья","ex":"El *cerdo* come mucho. — Свиня багато їсть."},
            {"es":"el pollo","ua":"курка","ru":"курица","ex":"El *pollo* pone huevos. — Курка несе яйця."},
            {"es":"el pez","ua":"риба","ru":"рыба","ex":"El *pez* nada en el agua. — Риба плаває у воді."},
            {"es":"el conejo","ua":"кролик","ru":"кролик","ex":"El *conejo* come zanahorias. — Кролик їсть моркву."},
            {"es":"el oso","ua":"ведмідь","ru":"медведь","ex":"El *oso* hiberna en invierno. — Ведмідь зимує взимку."},
            {"es":"el león","ua":"лев","ru":"лев","ex":"El *león* es el rey de la selva. — Лев — цар джунглів."},
            {"es":"el elefante","ua":"слон","ru":"слон","ex":"El *elefante* tiene una trompa larga. — Слон має довгий хобот."},
        ],
        "quiz":[
            {"q":"Як буде 'собака'?","a":"el perro","wrong":["el gato","el pájaro","el conejo","el oso","el cerdo"]},
            {"q":"Що означає 'el gato'?","a":"кіт / кот","wrong":["собака","птах","кролик","ведмідь","лев"]},
            {"q":"Як буде 'кінь'?","a":"el caballo","wrong":["la vaca","el cerdo","el oso","el elefante","el león"]},
            {"q":"Що означає 'el pez'?","a":"риба / рыба","wrong":["птах","кролик","кіт","собака","свиня"]},
            {"q":"Як буде 'ведмідь'?","a":"el oso","wrong":["el león","el elefante","el caballo","el cerdo","la vaca"]},
            {"q":"Що означає 'la vaca'?","a":"корова / корова","wrong":["свиня","кінь","вівця","козел","курка"]},
            {"q":"Як буде 'кролик'?","a":"el conejo","wrong":["el pájaro","el pez","el gato","el cerdo","el oso"]},
            {"q":"Що означає 'el león'?","a":"лев / лев","wrong":["тигр","ведмідь","слон","вовк","лисиця"]},
            {"q":"У реченні 'El perro se llama Max' — хто це?","a":"собака","wrong":["кіт","кінь","птах","кролик","ведмідь"]},
            {"q":"Що означає 'el elefante'?","a":"слон / слон","wrong":["жираф","лев","носоріг","гіпопотам","зебра"]},
        ]
    },
    {
        "id":"house","title":"🏠 Дім і меблі / Дом и мебель","level":"A2",
        "words":[
            {"es":"la casa","ua":"будинок","ru":"дом","ex":"Vivo en una *casa* grande. — Я живу у великому будинку."},
            {"es":"el apartamento","ua":"квартира","ru":"квартира","ex":"Tengo un *apartamento* en el centro. — У мене квартира в центрі."},
            {"es":"la cocina","ua":"кухня","ru":"кухня","ex":"Cocino en la *cocina*. — Я готую на кухні."},
            {"es":"el baño","ua":"ванна кімната","ru":"ванная","ex":"El *baño* está limpio. — Ванна кімната чиста."},
            {"es":"el dormitorio","ua":"спальня","ru":"спальня","ex":"Mi *dormitorio* es pequeño. — Моя спальня маленька."},
            {"es":"el salón","ua":"вітальня","ru":"гостиная","ex":"Vemos TV en el *salón*. — Ми дивимось ТБ у вітальні."},
            {"es":"la cama","ua":"ліжко","ru":"кровать","ex":"La *cama* es muy cómoda. — Ліжко дуже зручне."},
            {"es":"la mesa","ua":"стіл","ru":"стол","ex":"Comemos en la *mesa*. — Ми їмо за столом."},
            {"es":"la silla","ua":"стілець","ru":"стул","ex":"Siéntate en la *silla*. — Сядь на стілець."},
            {"es":"el sofá","ua":"диван","ru":"диван","ex":"Descanso en el *sofá*. — Я відпочиваю на дивані."},
            {"es":"la ventana","ua":"вікно","ru":"окно","ex":"Abre la *ventana*, por favor. — Відкрий вікно, будь ласка."},
            {"es":"la puerta","ua":"двері","ru":"дверь","ex":"Cierra la *puerta*. — Закрий двері."},
        ],
        "quiz":[
            {"q":"Як буде 'кухня'?","a":"la cocina","wrong":["el baño","el dormitorio","el salón","la cocina","la puerta"]},
            {"q":"Що означає 'el dormitorio'?","a":"спальня / спальня","wrong":["кухня","ванна","вітальня","коридор","балкон"]},
            {"q":"Як буде 'стіл'?","a":"la mesa","wrong":["la silla","el sofá","la cama","la ventana","la puerta"]},
            {"q":"Що означає 'la ventana'?","a":"вікно / окно","wrong":["двері","стіна","підлога","стеля","балкон"]},
            {"q":"Як буде 'диван'?","a":"el sofá","wrong":["la silla","la cama","la mesa","el armario","la ventana"]},
            {"q":"Що означає 'la puerta'?","a":"двері / дверь","wrong":["вікно","стіна","підлога","стеля","поріг"]},
            {"q":"Як буде 'ліжко'?","a":"la cama","wrong":["el sofá","la silla","la mesa","el dormitorio","la ventana"]},
            {"q":"Що означає 'el baño'?","a":"ванна кімната / ванная","wrong":["спальня","кухня","вітальня","туалет","коридор"]},
            {"q":"У реченні 'Vivo en una casa grande' — де живе людина?","a":"у великому будинку","wrong":["у маленькій квартирі","у готелі","на дачі","у гуртожитку","у кімнаті"]},
            {"q":"Що означає 'el salón'?","a":"вітальня / гостиная","wrong":["спальня","кухня","ванна","коридор","балкон"]},
        ]
    },
    {
        "id":"city","title":"🏙 Місто і транспорт / Город и транспорт","level":"A2",
        "words":[
            {"es":"la calle","ua":"вулиця","ru":"улица","ex":"Vivo en esta *calle*. — Я живу на цій вулиці."},
            {"es":"la tienda","ua":"магазин","ru":"магазин","ex":"Voy a la *tienda*. — Я іду в магазин."},
            {"es":"el supermercado","ua":"супермаркет","ru":"супермаркет","ex":"Compro en el *supermercado*. — Я купую в супермаркеті."},
            {"es":"el banco","ua":"банк","ru":"банк","ex":"Necesito ir al *banco*. — Мені треба піти в банк."},
            {"es":"el hospital","ua":"лікарня","ru":"больница","ex":"El *hospital* está cerca. — Лікарня поруч."},
            {"es":"la farmacia","ua":"аптека","ru":"аптека","ex":"Compro medicinas en la *farmacia*. — Я купую ліки в аптеці."},
            {"es":"el autobús","ua":"автобус","ru":"автобус","ex":"Voy al trabajo en *autobús*. — Я їду на роботу на автобусі."},
            {"es":"el metro","ua":"метро","ru":"метро","ex":"El *metro* es rápido. — Метро швидке."},
            {"es":"el tren","ua":"поїзд","ru":"поезд","ex":"El *tren* sale a las ocho. — Поїзд відходить о восьмій."},
            {"es":"el coche","ua":"машина","ru":"машина","ex":"Tengo un *coche* nuevo. — У мене нова машина."},
            {"es":"la bicicleta","ua":"велосипед","ru":"велосипед","ex":"Voy en *bicicleta* al trabajo. — Я їду на велосипеді на роботу."},
            {"es":"el aeropuerto","ua":"аеропорт","ru":"аэропорт","ex":"El *aeropuerto* está lejos. — Аеропорт далеко."},
        ],
        "quiz":[
            {"q":"Як буде 'автобус'?","a":"el autobús","wrong":["el metro","el tren","el coche","la bicicleta","el taxi"]},
            {"q":"Що означає 'la farmacia'?","a":"аптека / аптека","wrong":["лікарня","банк","магазин","пошта","кафе"]},
            {"q":"Як буде 'аеропорт'?","a":"el aeropuerto","wrong":["la estación","el puerto","el metro","la calle","el hotel"]},
            {"q":"Що означає 'el supermercado'?","a":"супермаркет / супермаркет","wrong":["ринок","банк","аптека","ресторан","магазин одягу"]},
            {"q":"Як буде 'велосипед'?","a":"la bicicleta","wrong":["el coche","el autobús","el metro","el tren","la moto"]},
            {"q":"Що означає 'el banco'?","a":"банк / банк","wrong":["аптека","лікарня","магазин","пошта","офіс"]},
            {"q":"Як буде 'вулиця'?","a":"la calle","wrong":["la plaza","el parque","la avenida","el camino","la ruta"]},
            {"q":"Що означає 'el tren'?","a":"поїзд / поезд","wrong":["автобус","метро","машина","літак","корабель"]},
            {"q":"У реченні 'Voy al trabajo en autobús' — як людина їде?","a":"на автобусі","wrong":["на метро","на машині","пішки","на велосипеді","на поїзді"]},
            {"q":"Що означає 'el hospital'?","a":"лікарня / больница","wrong":["аптека","клініка","банк","школа","офіс"]},
        ]
    },
    {
        "id":"weather","title":"🌤 Погода / Погода","level":"A2",
        "words":[
            {"es":"el sol","ua":"сонце","ru":"солнце","ex":"Hoy hace mucho *sol*. — Сьогодні дуже сонячно."},
            {"es":"la lluvia","ua":"дощ","ru":"дождь","ex":"Hay mucha *lluvia* hoy. — Сьогодні багато дощу."},
            {"es":"la nieve","ua":"сніг","ru":"снег","ex":"Me gusta la *nieve*. — Мені подобається сніг."},
            {"es":"el viento","ua":"вітер","ru":"ветер","ex":"Hace mucho *viento*. — Дуже вітряно."},
            {"es":"la nube","ua":"хмара","ru":"облако","ex":"Hay muchas *nubes* hoy. — Сьогодні багато хмар."},
            {"es":"la tormenta","ua":"гроза","ru":"гроза","ex":"Esta noche habrá *tormenta*. — Вночі буде гроза."},
            {"es":"el calor","ua":"спека","ru":"жара","ex":"En verano hay mucho *calor*. — Влітку дуже жарко."},
            {"es":"el frío","ua":"холод","ru":"холод","ex":"Tengo mucho *frío*. — Мені дуже холодно."},
            {"es":"¿Qué tiempo hace?","ua":"Яка погода?","ru":"Какая погода?","ex":"*¿Qué tiempo hace* hoy? — Яка сьогодні погода?"},
            {"es":"Hace calor","ua":"Жарко","ru":"Жарко","ex":"*Hace calor* en verano. — Влітку жарко."},
            {"es":"Hace frío","ua":"Холодно","ru":"Холодно","ex":"*Hace frío* en invierno. — Взимку холодно."},
            {"es":"Llueve","ua":"Іде дощ","ru":"Идёт дождь","ex":"*Llueve* mucho en otoño. — Восени часто іде дощ."},
        ],
        "quiz":[
            {"q":"Як буде 'сніг'?","a":"la nieve","wrong":["la lluvia","el viento","la nube","el sol","la tormenta"]},
            {"q":"Що означає 'el viento'?","a":"вітер / ветер","wrong":["дощ","сніг","сонце","хмара","гроза"]},
            {"q":"Як сказати 'Жарко'?","a":"Hace calor","wrong":["Hace frío","Llueve","Nieva","Hace viento","Hace sol"]},
            {"q":"Що означає 'Llueve'?","a":"Іде дощ / Идёт дождь","wrong":["Сніжить","Вітряно","Сонячно","Хмарно","Гроза"]},
            {"q":"Як запитати 'Яка погода?'","a":"¿Qué tiempo hace?","wrong":["¿Cómo estás?","¿Qué hora es?","¿Dónde estás?","¿Cuántos años tienes?","¿Cómo te llamas?"]},
            {"q":"Що означає 'la tormenta'?","a":"гроза / гроза","wrong":["дощ","сніг","вітер","хмара","туман"]},
            {"q":"Як буде 'сонце'?","a":"el sol","wrong":["la luna","la estrella","la nube","el cielo","el arcoíris"]},
            {"q":"Що означає 'Hace frío'?","a":"Холодно / Холодно","wrong":["Жарко","Вітряно","Сонячно","Дощить","Сніжить"]},
            {"q":"У реченні 'En verano hay mucho calor' — коли жарко?","a":"влітку","wrong":["взимку","навесні","восени","завжди","ніколи"]},
            {"q":"Що означає 'la lluvia'?","a":"дощ / дождь","wrong":["сніг","вітер","гроза","туман","хмара"]},
        ]
    },
    {
        "id":"emotions","title":"😊 Емоції / Эмоции","level":"B1",
        "words":[
            {"es":"feliz","ua":"щасливий","ru":"счастливый","ex":"Estoy muy *feliz* hoy. — Я дуже щасливий сьогодні."},
            {"es":"triste","ua":"сумний","ru":"грустный","ex":"Estoy *triste* porque llueve. — Мені сумно, бо іде дощ."},
            {"es":"enojado","ua":"злий","ru":"злой","ex":"Estoy *enojado* contigo. — Я злий на тебе."},
            {"es":"asustado","ua":"наляканий","ru":"испуганный","ex":"El niño está *asustado*. — Дитина налякана."},
            {"es":"sorprendido","ua":"здивований","ru":"удивлённый","ex":"Estoy *sorprendido* por la noticia. — Я здивований новиною."},
            {"es":"cansado","ua":"втомлений","ru":"усталый","ex":"Estoy muy *cansado* hoy. — Я дуже втомлений сьогодні."},
            {"es":"aburrido","ua":"нудьгуючий","ru":"скучающий","ex":"Estoy *aburrido* en casa. — Мені нудно вдома."},
            {"es":"nervioso","ua":"нервовий","ru":"нервный","ex":"Estoy *nervioso* antes del examen. — Я нервую перед іспитом."},
            {"es":"emocionado","ua":"схвильований","ru":"взволнованный","ex":"Estoy muy *emocionado* por el viaje. — Я дуже схвильований подорожжю."},
            {"es":"tranquilo","ua":"спокійний","ru":"спокойный","ex":"Estoy *tranquilo* ahora. — Я зараз спокійний."},
            {"es":"orgulloso","ua":"гордий","ru":"гордый","ex":"Estoy *orgulloso* de ti. — Я пишаюся тобою."},
            {"es":"avergonzado","ua":"засоромлений","ru":"пристыжённый","ex":"Estoy *avergonzado* de mi error. — Мені соромно за мою помилку."},
        ],
        "quiz":[
            {"q":"Як буде 'щасливий'?","a":"feliz","wrong":["triste","enojado","cansado","nervioso","aburrido"]},
            {"q":"Що означає 'triste'?","a":"сумний / грустный","wrong":["злий","втомлений","нервовий","здивований","спокійний"]},
            {"q":"Як буде 'втомлений'?","a":"cansado","wrong":["aburrido","nervioso","feliz","triste","tranquilo"]},
            {"q":"Що означає 'nervioso'?","a":"нервовий / нервный","wrong":["спокійний","злий","сумний","щасливий","гордий"]},
            {"q":"Як буде 'спокійний'?","a":"tranquilo","wrong":["nervioso","enojado","asustado","emocionado","orgulloso"]},
            {"q":"Що означає 'sorprendido'?","a":"здивований / удивлённый","wrong":["наляканий","злий","сумний","нудьгуючий","схвильований"]},
            {"q":"Як буде 'гордий'?","a":"orgulloso","wrong":["feliz","emocionado","tranquilo","sorprendido","avergonzado"]},
            {"q":"Що означає 'aburrido'?","a":"нудьгуючий / скучающий","wrong":["втомлений","сумний","злий","нервовий","наляканий"]},
            {"q":"У реченні 'Estoy nervioso antes del examen' — коли людина нервує?","a":"перед іспитом","wrong":["після іспиту","під час іспиту","на уроці","вдома","вранці"]},
            {"q":"Що означає 'emocionado'?","a":"схвильований / взволнованный","wrong":["злий","наляканий","нудьгуючий","спокійний","сумний"]},
        ]
    },
    {
        "id":"professions","title":"💼 Професії / Профессии","level":"A2",
        "words":[
            {"es":"el médico","ua":"лікар","ru":"врач","ex":"El *médico* me ayudó mucho. — Лікар мені дуже допоміг."},
            {"es":"el profesor","ua":"вчитель","ru":"учитель","ex":"Mi *profesor* es muy bueno. — Мій вчитель дуже хороший."},
            {"es":"el ingeniero","ua":"інженер","ru":"инженер","ex":"Trabajo como *ingeniero*. — Я працюю інженером."},
            {"es":"el abogado","ua":"адвокат","ru":"адвокат","ex":"Necesito hablar con un *abogado*. — Мені треба поговорити з адвокатом."},
            {"es":"el cocinero","ua":"кухар","ru":"повар","ex":"El *cocinero* prepara la comida. — Кухар готує їжу."},
            {"es":"el conductor","ua":"водій","ru":"водитель","ex":"El *conductor* maneja bien. — Водій добре керує."},
            {"es":"el policía","ua":"поліцейський","ru":"полицейский","ex":"El *policía* me ayudó. — Поліцейський мені допоміг."},
            {"es":"el enfermero","ua":"медсестра/брат","ru":"медсестра/брат","ex":"El *enfermero* es muy amable. — Медбрат дуже ввічливий."},
            {"es":"el periodista","ua":"журналіст","ru":"журналист","ex":"El *periodista* escribe artículos. — Журналіст пише статті."},
            {"es":"el arquitecto","ua":"архітектор","ru":"архитектор","ex":"El *arquitecto* diseña edificios. — Архітектор проектує будівлі."},
            {"es":"el bombero","ua":"пожежник","ru":"пожарный","ex":"Los *bomberos* apagan el fuego. — Пожежники гасять вогонь."},
            {"es":"el dentista","ua":"стоматолог","ru":"стоматолог","ex":"Voy al *dentista* mañana. — Я йду до стоматолога завтра."},
        ],
        "quiz":[
            {"q":"Як буде 'лікар'?","a":"el médico","wrong":["el enfermero","el dentista","el abogado","el profesor","el cocinero"]},
            {"q":"Що означає 'el profesor'?","a":"вчитель / учитель","wrong":["лікар","інженер","адвокат","кухар","водій"]},
            {"q":"Як буде 'пожежник'?","a":"el bombero","wrong":["el policía","el médico","el conductor","el arquitecto","el periodista"]},
            {"q":"Що означає 'el cocinero'?","a":"кухар / повар","wrong":["водій","архітектор","журналіст","інженер","лікар"]},
            {"q":"Як буде 'адвокат'?","a":"el abogado","wrong":["el médico","el juez","el periodista","el arquitecto","el ingeniero"]},
            {"q":"Що означає 'el dentista'?","a":"стоматолог / стоматолог","wrong":["лікар","медбрат","хірург","фармацевт","терапевт"]},
            {"q":"Як буде 'журналіст'?","a":"el periodista","wrong":["el escritor","el fotógrafo","el abogado","el arquitecto","el ingeniero"]},
            {"q":"Що означає 'el conductor'?","a":"водій / водитель","wrong":["пілот","капітан","машиніст","кур'єр","таксист"]},
            {"q":"У реченні 'Voy al dentista mañana' — куди йде людина?","a":"до стоматолога","wrong":["до лікаря","до аптеки","до лікарні","до школи","до банку"]},
            {"q":"Що означає 'el arquitecto'?","a":"архітектор / архитектор","wrong":["інженер","будівельник","дизайнер","художник","скульптор"]},
        ]
    },
]

FLASHCARDS = [
    {"es":"hola","ua":"привіт","ru":"привет"},
    {"es":"gracias","ua":"дякую","ru":"спасибо"},
    {"es":"por favor","ua":"будь ласка","ru":"пожалуйста"},
    {"es":"sí","ua":"так","ru":"да"},
    {"es":"no","ua":"ні","ru":"нет"},
    {"es":"perdón","ua":"вибачте","ru":"извините"},
    {"es":"de nada","ua":"нема за що","ru":"пожалуйста"},
    {"es":"rojo","ua":"червоний","ru":"красный"},
    {"es":"azul","ua":"синій","ru":"синий"},
    {"es":"verde","ua":"зелений","ru":"зелёный"},
    {"es":"negro","ua":"чорний","ru":"чёрный"},
    {"es":"blanco","ua":"білий","ru":"белый"},
    {"es":"el pan","ua":"хліб","ru":"хлеб"},
    {"es":"el agua","ua":"вода","ru":"вода"},
    {"es":"el café","ua":"кава","ru":"кофе"},
    {"es":"el pollo","ua":"курка","ru":"курица"},
    {"es":"la madre","ua":"мати","ru":"мать"},
    {"es":"el padre","ua":"батько","ru":"отец"},
    {"es":"el hermano","ua":"брат","ru":"брат"},
    {"es":"hablar","ua":"говорити","ru":"говорить"},
    {"es":"comer","ua":"їсти","ru":"есть"},
    {"es":"vivir","ua":"жити","ru":"жить"},
    {"es":"trabajar","ua":"працювати","ru":"работать"},
    {"es":"estudiar","ua":"вчитися","ru":"учиться"},
    {"es":"tener","ua":"мати","ru":"иметь"},
    {"es":"ser","ua":"бути (постійно)","ru":"быть (постоянно)"},
    {"es":"estar","ua":"бути (тимчасово)","ru":"быть (временно)"},
    {"es":"yo","ua":"я","ru":"я"},
    {"es":"tú","ua":"ти","ru":"ты"},
    {"es":"nosotros","ua":"ми","ru":"мы"},
    {"es":"la casa","ua":"будинок","ru":"дом"},
    {"es":"la ciudad","ua":"місто","ru":"город"},
    {"es":"el trabajo","ua":"робота","ru":"работа"},
    {"es":"la tienda","ua":"магазин","ru":"магазин"},
    {"es":"el perro","ua":"собака","ru":"собака"},
    {"es":"el gato","ua":"кіт","ru":"кот"},
    {"es":"feliz","ua":"щасливий","ru":"счастливый"},
    {"es":"cansado","ua":"втомлений","ru":"усталый"},
    {"es":"el médico","ua":"лікар","ru":"врач"},
    {"es":"el autobús","ua":"автобус","ru":"автобус"},
]

# ══════════════════════════════════════════════════════════
# БАЗА ДАНИХ
# ══════════════════════════════════════════════════════════
users_db = {}

def get_user(uid):
    k = str(uid)
    if k not in users_db:
        users_db[k] = {
            "lang": "ua",
            "xp": 0, "streak": 0, "last_date": None,
            "completed_lessons": [], "known_cards": [],
            "flash_idx": 0, "notify_hour": 9, "notify_enabled": True,
            "quiz_lesson": None, "quiz_questions": [], "quiz_idx": 0, "quiz_correct": 0,
            "vocab_quiz": None, "vocab_quiz_q": [], "vocab_quiz_idx": 0, "vocab_quiz_correct": 0,
            "game_mode": None, "game_cards": [], "game_idx": 0, "game_correct": 0,
            "waiting_input": None,
        }
    return users_db[k]

def add_xp(uid, amount):
    u = get_user(uid)
    u["xp"] += amount
    today = date.today().isoformat()
    if u["last_date"] != today:
        u["streak"] += 1
        u["last_date"] = today

def get_level(xp):
    levels = [
        (0,"🥚 Початківець/Новичок",100),
        (100,"🐣 Новачок/Начинающий",300),
        (300,"📚 Студент/Студент",600),
        (600,"🎓 Учень/Ученик",1000),
        (1000,"⭐ Знавець/Знаток",1500),
        (1500,"🌟 Майстер/Мастер",2500),
        (2500,"🏆 Експерт/Эксперт",9999),
    ]
    for min_xp, name, max_xp in levels:
        if xp < max_xp:
            return name, min_xp, max_xp
    return levels[-1][1], 2500, 9999

def get_word_translation(word, lang):
    return word.get("ru" if lang == "ru" else "ua", word.get("ua", ""))

# ══════════════════════════════════════════════════════════
# КЛАВІАТУРИ
# ══════════════════════════════════════════════════════════
def main_kb(uid):
    lang = users_db.get(str(uid), {}).get("lang", "ua")
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(UI[lang]["lessons"], callback_data="menu_lessons"),
         InlineKeyboardButton(UI[lang]["flashcards"], callback_data="menu_flash")],
        [InlineKeyboardButton(UI[lang]["quiz"], callback_data="menu_quiz"),
         InlineKeyboardButton(UI[lang]["game"], callback_data="menu_game")],
        [InlineKeyboardButton(UI[lang]["vocab"], callback_data="menu_vocab"),
         InlineKeyboardButton(UI[lang]["progress"], callback_data="menu_progress")],
        [InlineKeyboardButton(UI[lang]["notify"], callback_data="menu_notify"),
         InlineKeyboardButton(UI[lang]["lang"], callback_data="toggle_lang")],
    ])

def back_kb(uid):
    return InlineKeyboardMarkup([[InlineKeyboardButton(t(uid,"main_menu"), callback_data="menu_main")]])

# ══════════════════════════════════════════════════════════
# HANDLERS
# ══════════════════════════════════════════════════════════
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    get_user(user.id)
    lang_flag = "🇺🇦"
    await update.message.reply_text(
        f"🇪🇸 *¡Hola, {user.first_name}!* {lang_flag}\n\n"
        f"{t(user.id, 'welcome')}\n\n"
        f"📖 {t(user.id,'lessons')} — теорія з нуля\n"
        f"🃏 {t(user.id,'flashcards')} — слова\n"
        f"🧠 {t(user.id,'quiz')} — 10 рандомних питань\n"
        f"🎮 {t(user.id,'game')} — як у Duolingo\n"
        f"📚 {t(user.id,'vocab')} — слова по темах з реченнями\n"
        f"🔔 {t(user.id,'notify')} — щоденні нагадування\n\n"
        f"{t(user.id,'choose')}",
        parse_mode="Markdown", reply_markup=main_kb(user.id)
    )

async def handle_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    uid = q.from_user.id
    u = get_user(uid)

    # ── МОВА ──────────────────────────────────────────────
    if data == "toggle_lang":
        u["lang"] = "ru" if u["lang"] == "ua" else "ua"
        flag = "🇺🇦" if u["lang"] == "ua" else "🇷🇺"
        await q.edit_message_text(
            f"{flag} Мову змінено / Язык изменён\n\n{t(uid,'choose')}",
            reply_markup=main_kb(uid)
        )

    # ── МЕНЮ ──────────────────────────────────────────────
    elif data == "menu_main":
        await q.edit_message_text(
            f"🇪🇸 *{'Головне меню' if u['lang']=='ua' else 'Главное меню'}*",
            parse_mode="Markdown", reply_markup=main_kb(uid)
        )

    # ── УРОКИ ─────────────────────────────────────────────
    elif data == "menu_lessons":
        rows = []
        for l in LESSONS:
            done = l["id"] in u["completed_lessons"]
            mark = "✅" if done else "▸"
            rows.append([InlineKeyboardButton(f"{mark} {l['title']}", callback_data=f"lesson_{l['id']}")])
        rows.append([InlineKeyboardButton(t(uid,"main_menu"), callback_data="menu_main")])
        await q.edit_message_text(t(uid,"lessons_title"), parse_mode="Markdown",
                                   reply_markup=InlineKeyboardMarkup(rows))

    elif data.startswith("lesson_"):
        lid = int(data.split("_")[1])
        lesson = next(l for l in LESSONS if l["id"] == lid)
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"🧠 {'Квіз (10 питань)' if u['lang']=='ua' else 'Квиз (10 вопросов)'}", callback_data=f"quiz_lesson_{lid}")],
            [InlineKeyboardButton(t(uid,"back"), callback_data="menu_lessons")],
        ])
        await q.edit_message_text(lesson["theory"], parse_mode="Markdown", reply_markup=kb)

    # ── ФЛЕШКАРТИ ─────────────────────────────────────────
    elif data == "menu_flash":
        await show_flashcard(q, uid)

    elif data == "flash_show":
        await show_flashcard(q, uid, reveal=True)

    elif data == "flash_know":
        card = FLASHCARDS[u["flash_idx"] % len(FLASHCARDS)]
        if card["es"] not in u["known_cards"]:
            u["known_cards"].append(card["es"])
            add_xp(uid, 5)
        u["flash_idx"] = (u["flash_idx"] + 1) % len(FLASHCARDS)
        await show_flashcard(q, uid)

    elif data == "flash_next":
        u["flash_idx"] = (u["flash_idx"] + 1) % len(FLASHCARDS)
        await show_flashcard(q, uid)

    elif data == "flash_random":
        u["flash_idx"] = random.randint(0, len(FLASHCARDS) - 1)
        await show_flashcard(q, uid)

    # ── КВІЗ ──────────────────────────────────────────────
    elif data == "menu_quiz":
        rows = [[InlineKeyboardButton(l["title"], callback_data=f"quiz_lesson_{l['id']}")] for l in LESSONS]
        rows.append([InlineKeyboardButton(t(uid,"quiz_random"), callback_data="quiz_random")])
        rows.append([InlineKeyboardButton(t(uid,"main_menu"), callback_data="menu_main")])
        await q.edit_message_text(t(uid,"quiz_title"), parse_mode="Markdown",
                                   reply_markup=InlineKeyboardMarkup(rows))

    elif data.startswith("quiz_lesson_") or data == "quiz_random":
        if data == "quiz_random":
            lesson = random.choice(LESSONS)
        else:
            lid = int(data.split("_")[2])
            lesson = next(l for l in LESSONS if l["id"] == lid)
        all_q = lesson["all_questions"].copy()
        random.shuffle(all_q)
        u["quiz_lesson"] = lesson
        u["quiz_questions"] = all_q[:10]
        u["quiz_idx"] = 0
        u["quiz_correct"] = 0
        await show_quiz(q, uid)

    elif data == "quiz_next":
        await show_quiz(q, uid)

    elif data.startswith("qans_"):
        await handle_quiz_answer(q, uid, data[5:])

    # ── СЛОВНИК ───────────────────────────────────────────
    elif data == "menu_vocab":
        rows = []
        for theme in VOCAB_THEMES:
            rows.append([InlineKeyboardButton(
                f"{theme['title']} [{theme['level']}]",
                callback_data=f"vocab_{theme['id']}"
            )])
        rows.append([InlineKeyboardButton(t(uid,"main_menu"), callback_data="menu_main")])
        await q.edit_message_text(t(uid,"vocab_title"), parse_mode="Markdown",
                                   reply_markup=InlineKeyboardMarkup(rows))

    elif data.startswith("vocab_") and not data.startswith("vocab_quiz_"):
        theme_id = data[6:]
        theme = next(th for th in VOCAB_THEMES if th["id"] == theme_id)
        lang = u["lang"]

        text = f"📖 *{theme['title']}*\n\n"
        for w in theme["words"]:
            trans = w.get("ru" if lang == "ru" else "ua", "")
            text += f"🇪🇸 *{w['es']}* — {trans}\n"
            text += f"💬 _{w['ex']}_\n\n"

        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(t(uid,"quiz_words"), callback_data=f"vocab_quiz_{theme_id}")],
            [InlineKeyboardButton(t(uid,"back"), callback_data="menu_vocab")],
        ])
        # Розбиваємо на частини якщо довго
        if len(text) > 4000:
            text = text[:3900] + "\n\n_...і ще більше слів у квізі!_"
        await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

    elif data.startswith("vocab_quiz_"):
        theme_id = data[11:]
        theme = next(th for th in VOCAB_THEMES if th["id"] == theme_id)
        all_q = theme["quiz"].copy()
        random.shuffle(all_q)
        u["vocab_quiz"] = theme
        u["vocab_quiz_q"] = all_q[:10]
        u["vocab_quiz_idx"] = 0
        u["vocab_quiz_correct"] = 0
        await show_vocab_quiz(q, uid)

    elif data == "vocab_quiz_next":
        await show_vocab_quiz(q, uid)

    elif data.startswith("vans_"):
        await handle_vocab_answer(q, uid, data[5:])

    # ── ПРОГРЕС ───────────────────────────────────────────
    elif data == "menu_progress":
        xp = u["xp"]
        level, min_xp, max_xp = get_level(xp)
        progress = xp - min_xp
        total = max_xp - min_xp
        filled = int(progress / total * 10) if total > 0 else 10
        bar = "█" * filled + "░" * (10 - filled)
        nd = len(u["completed_lessons"])
        text = (
            f"{t(uid,'progress_title')}\n\n"
            f"{t(uid,'level')}: *{level}*\n"
            f"⭐ XP: *{xp}*\n[{bar}] {progress}/{total}\n\n"
            f"{t(uid,'streak')}: *{u['streak']} {t(uid,'days')}*\n"
            f"{t(uid,'lessons_done')}: *{nd}/{len(LESSONS)}*\n"
            f"{t(uid,'words_done')}: *{len(u['known_cards'])}/{len(FLASHCARDS)}*\n\n"
        )
        if nd == 0:
            text += t(uid, "all_lessons")
        elif nd < len(LESSONS):
            text += t(uid, "some_lessons", n=len(LESSONS)-nd)
        else:
            text += t(uid, "all_done")
        await q.edit_message_text(text, parse_mode="Markdown", reply_markup=back_kb(uid))

    # ── НАГАДУВАННЯ ───────────────────────────────────────
    elif data == "menu_notify":
        status = t(uid,"notify_status_on") if u["notify_enabled"] else t(uid,"notify_status_off")
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(t(uid,"notify_off") if u["notify_enabled"] else t(uid,"notify_on"),
                                  callback_data="notify_toggle")],
            [InlineKeyboardButton(t(uid,"notify_time"), callback_data="notify_time")],
            [InlineKeyboardButton(t(uid,"main_menu"), callback_data="menu_main")],
        ])
        await q.edit_message_text(
            f"{t(uid,'notify_title')}\n\n{status}\n⏰ {u['notify_hour']:02d}:00",
            parse_mode="Markdown", reply_markup=kb
        )

    elif data == "notify_toggle":
        u["notify_enabled"] = not u["notify_enabled"]
        status = t(uid,"notify_status_on") if u["notify_enabled"] else t(uid,"notify_status_off")
        await q.edit_message_text(f"✅ {status}", reply_markup=back_kb(uid))

    elif data == "notify_time":
        hours = [[InlineKeyboardButton(f"{h:02d}:00", callback_data=f"notifyset_{h}") for h in range(i, min(i+4,23))]
                 for i in range(7, 23, 4)]
        hours.append([InlineKeyboardButton(t(uid,"back"), callback_data="menu_notify")])
        await q.edit_message_text("⏰", reply_markup=InlineKeyboardMarkup(hours))

    elif data.startswith("notifyset_"):
        hour = int(data.split("_")[1])
        u["notify_hour"] = hour
        await q.edit_message_text(f"✅ {hour:02d}:00", reply_markup=back_kb(uid))

    # ── ІГРОВИЙ РЕЖИМ ─────────────────────────────────────
    elif data == "menu_game":
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(t(uid,"game_mc"), callback_data="game_mc")],
            [InlineKeyboardButton(t(uid,"game_write"), callback_data="game_write")],
            [InlineKeyboardButton(t(uid,"main_menu"), callback_data="menu_main")],
        ])
        await q.edit_message_text(t(uid,"game_title"), parse_mode="Markdown", reply_markup=kb)

    elif data in ("game_mc", "game_write"):
        cards = FLASHCARDS.copy()
        random.shuffle(cards)
        u["game_mode"] = data
        u["game_cards"] = cards[:15]
        u["game_idx"] = 0
        u["game_correct"] = 0
        await show_game(q, uid)

    elif data.startswith("gans_"):
        await handle_game_answer(q, uid, data[5:])

    elif data == "game_next":
        await show_game(q, uid)


async def show_flashcard(q, uid, reveal=False):
    u = get_user(uid)
    idx = u["flash_idx"] % len(FLASHCARDS)
    card = FLASHCARDS[idx]
    lang = u["lang"]
    trans = card.get("ru" if lang == "ru" else "ua", "")
    known = len(u["known_cards"])

    if not reveal:
        text = (f"🃏 *{idx+1}/{len(FLASHCARDS)}*\n\n"
                f"🇪🇸 *{card['es']}*\n\n{t(uid,'flash_know')}")
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(t(uid,"flash_show"), callback_data="flash_show")],
            [InlineKeyboardButton(t(uid,"flash_next"), callback_data="flash_next"),
             InlineKeyboardButton(t(uid,"flash_random"), callback_data="flash_random")],
            [InlineKeyboardButton(t(uid,"main_menu"), callback_data="menu_main")],
        ])
    else:
        text = (f"🃏 *{idx+1}/{len(FLASHCARDS)}*\n\n"
                f"🇪🇸 *{card['es']}*\n"
                f"{'🇺🇦' if lang=='ua' else '🇷🇺'} *{trans}*\n\n"
                f"✅ {known}/{len(FLASHCARDS)}")
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(t(uid,"flash_knew"), callback_data="flash_know"),
             InlineKeyboardButton(t(uid,"flash_next"), callback_data="flash_next")],
            [InlineKeyboardButton(t(uid,"main_menu"), callback_data="menu_main")],
        ])
    await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)


async def show_quiz(q, uid):
    u = get_user(uid)
    questions = u["quiz_questions"]
    qi = u["quiz_idx"]

    if qi >= len(questions):
        correct = u["quiz_correct"]
        total = len(questions)
        xp = correct * 15
        add_xp(uid, xp)
        lesson = u["quiz_lesson"]
        if lesson["id"] not in u["completed_lessons"]:
            u["completed_lessons"].append(lesson["id"])
        pct = int(correct / total * 100)
        emoji = "🏆" if pct == 100 else "👍" if pct >= 60 else "📚"
        phrase = "¡Perfecto!" if pct==100 else "¡Bien!" if pct>=60 else "Practíca más!"
        await q.edit_message_text(
            t(uid,"quiz_done",c=correct,t=total,p=pct,e=f"{emoji} {phrase}",xp=xp),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(uid,"try_again"), callback_data=f"quiz_lesson_{lesson['id']}")],
                [InlineKeyboardButton(t(uid,"main_menu"), callback_data="menu_main")],
            ])
        )
        return

    q_data = questions[qi]
    wrong = random.sample(q_data["wrong"], min(3, len(q_data["wrong"])))
    options = wrong + [q_data["a"]]
    random.shuffle(options)
    kb = InlineKeyboardMarkup([[InlineKeyboardButton(opt, callback_data=f"qans_{opt}")] for opt in options])
    await q.edit_message_text(
        t(uid,"question",i=qi+1,total=len(questions),q=q_data["q"]),
        parse_mode="Markdown", reply_markup=kb
    )


async def handle_quiz_answer(q, uid, answer):
    u = get_user(uid)
    q_data = u["quiz_questions"][u["quiz_idx"]]
    correct = answer == q_data["a"]
    if correct:
        u["quiz_correct"] += 1
        text = t(uid,"correct",a=q_data["a"])
    else:
        text = t(uid,"wrong",ans=answer,a=q_data["a"])
    u["quiz_idx"] += 1
    await q.edit_message_text(text, parse_mode="Markdown",
                               reply_markup=InlineKeyboardMarkup([[
                                   InlineKeyboardButton(t(uid,"next"), callback_data="quiz_next")
                               ]]))


async def show_vocab_quiz(q, uid):
    u = get_user(uid)
    questions = u["vocab_quiz_q"]
    qi = u["vocab_quiz_idx"]

    if qi >= len(questions):
        correct = u["vocab_quiz_correct"]
        total = len(questions)
        xp = correct * 15
        add_xp(uid, xp)
        pct = int(correct / total * 100)
        emoji = "🏆" if pct == 100 else "👍" if pct >= 60 else "📚"
        phrase = "¡Perfecto!" if pct==100 else "¡Bien!" if pct>=60 else "Practíca más!"
        await q.edit_message_text(
            t(uid,"quiz_done",c=correct,t=total,p=pct,e=f"{emoji} {phrase}",xp=xp),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(uid,"try_again"), callback_data=f"vocab_quiz_{u['vocab_quiz']['id']}")],
                [InlineKeyboardButton(t(uid,"back"), callback_data="menu_vocab")],
            ])
        )
        return

    q_data = questions[qi]
    wrong = random.sample(q_data["wrong"], min(3, len(q_data["wrong"])))
    options = wrong + [q_data["a"]]
    random.shuffle(options)
    kb = InlineKeyboardMarkup([[InlineKeyboardButton(opt, callback_data=f"vans_{opt}")] for opt in options])
    await q.edit_message_text(
        t(uid,"question",i=qi+1,total=len(questions),q=q_data["q"]),
        parse_mode="Markdown", reply_markup=kb
    )


async def handle_vocab_answer(q, uid, answer):
    u = get_user(uid)
    q_data = u["vocab_quiz_q"][u["vocab_quiz_idx"]]
    correct = answer == q_data["a"]
    if correct:
        u["vocab_quiz_correct"] += 1
        text = t(uid,"correct",a=q_data["a"])
    else:
        text = t(uid,"wrong",ans=answer,a=q_data["a"])
    u["vocab_quiz_idx"] += 1
    await q.edit_message_text(text, parse_mode="Markdown",
                               reply_markup=InlineKeyboardMarkup([[
                                   InlineKeyboardButton(t(uid,"next"), callback_data="vocab_quiz_next")
                               ]]))


async def show_game(q, uid):
    u = get_user(uid)
    cards = u["game_cards"]
    gi = u["game_idx"]
    lang = u["lang"]

    if gi >= len(cards):
        correct = u["game_correct"]
        total = len(cards)
        xp = correct * 10
        add_xp(uid, xp)
        pct = int(correct / total * 100)
        await q.edit_message_text(
            t(uid,"game_done",c=correct,t=total,p=pct,xp=xp),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t(uid,"again"), callback_data=u["game_mode"])],
                [InlineKeyboardButton(t(uid,"main_menu"), callback_data="menu_main")],
            ])
        )
        return

    card = cards[gi]
    mode = u["game_mode"]

    if mode == "game_mc":
        all_trans = [c.get("ru" if lang=="ru" else "ua","") for c in FLASHCARDS
                     if c.get("ru" if lang=="ru" else "ua","") != card.get("ru" if lang=="ru" else "ua","")]
        wrong3 = random.sample(all_trans, 3)
        correct_trans = card.get("ru" if lang=="ru" else "ua","")
        options = wrong3 + [correct_trans]
        random.shuffle(options)
        kb = InlineKeyboardMarkup([[InlineKeyboardButton(opt, callback_data=f"gans_{opt}")] for opt in options])
        await q.edit_message_text(
            f"🎮 *{gi+1}/{len(cards)}*\n\n🇪🇸 *{card['es']}*\n\n{t(uid,'translate_q')}",
            parse_mode="Markdown", reply_markup=kb
        )
    else:
        trans = card.get("ru" if lang=="ru" else "ua","")
        u["waiting_input"] = {"type":"game_write","answer":card["es"],"trans":trans}
        await q.edit_message_text(
            f"✍️ *{gi+1}/{len(cards)}*\n\n{'🇺🇦' if lang=='ua' else '🇷🇺'} *{trans}*\n\n{t(uid,'write_q')}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(t(uid,"skip"), callback_data="gans_SKIP")
            ]])
        )


async def handle_game_answer(q, uid, answer):
    u = get_user(uid)
    lang = u["lang"]
    card = u["game_cards"][u["game_idx"]]
    correct_ans = card.get("ru" if lang=="ru" else "ua","") if u["game_mode"]=="game_mc" else card["es"]
    correct = answer == correct_ans
    if answer == "SKIP":
        text = f"{t(uid,'skipped')}\n✅ {t(uid,'correct_ans')}: *{correct_ans}*"
    elif correct:
        u["game_correct"] += 1
        text = t(uid,"correct",a=correct_ans)
    else:
        text = t(uid,"wrong",ans=answer,a=correct_ans)
    u["game_idx"] += 1
    u["waiting_input"] = None
    await q.edit_message_text(text, parse_mode="Markdown",
                               reply_markup=InlineKeyboardMarkup([[
                                   InlineKeyboardButton(t(uid,"next"), callback_data="game_next")
                               ]]))


async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    u = get_user(uid)
    text = update.message.text.strip()
    wi = u.get("waiting_input")

    if wi and wi["type"] == "game_write":
        correct = text.lower().strip() == wi["answer"].lower().strip()
        if correct:
            u["game_correct"] += 1
            reply = t(uid,"correct",a=wi["answer"])
        else:
            reply = t(uid,"wrong",ans=text,a=wi["answer"])
        u["game_idx"] += 1
        u["waiting_input"] = None
        await update.message.reply_text(reply, parse_mode="Markdown",
                                         reply_markup=InlineKeyboardMarkup([[
                                             InlineKeyboardButton(t(uid,"next"), callback_data="game_next")
                                         ]]))
    else:
        await update.message.reply_text(t(uid,"menu"), reply_markup=main_kb(uid))


REMINDERS = {
    "ua": [
        "🇪🇸 *¡Buenos días!* Час вчити іспанську! 💪",
        "🌟 Не забудь про урок сьогодні! 🔥",
        "📚 Слово дня: *mañana* = завтра/ранок 🇪🇸",
        "🎯 *¡Ánimo!* Твій квіз чекає! 💃",
        "⭐ Не переривай серію — вчи іспанську! 🇪🇸",
    ],
    "ru": [
        "🇪🇸 *¡Buenos días!* Время учить испанский! 💪",
        "🌟 Не забудь про урок сегодня! 🔥",
        "📚 Слово дня: *mañana* = завтра/утро 🇪🇸",
        "🎯 *¡Ánimo!* Твой квиз ждёт! 💃",
        "⭐ Не прерывай серию — учи испанский! 🇪🇸",
    ]
}

async def send_daily_reminders(app):
    while True:
        from datetime import datetime
        now = datetime.now()
        for uid, u in list(users_db.items()):
            if u["notify_enabled"] and now.hour == u["notify_hour"] and now.minute == 0:
                try:
                    lang = u.get("lang", "ua")
                    msg = random.choice(REMINDERS[lang])
                    await app.bot.send_message(
                        chat_id=int(uid), text=msg,
                        parse_mode="Markdown", reply_markup=main_kb(int(uid))
                    )
                except Exception:
                    pass
        await asyncio.sleep(60)


if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    loop = asyncio.get_event_loop()
    loop.create_task(send_daily_reminders(app))
    print("🤖 Бот v4.0 запущено!")
    app.run_polling(drop_pending_updates=True)
