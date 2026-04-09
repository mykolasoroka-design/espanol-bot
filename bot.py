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

LESSONS = [
    {
        "id": 1, "title": "🔤 Урок 1: Привітання",
        "theory": (
            "━━━━━━━━━━━━━━━━━━━━━━\n📖 *УРОК 1: Привітання*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🌅 *Hola* — Привіт\n🌄 *Buenos días* — Доброго ранку\n"
            "☀️ *Buenas tardes* — Добрий день\n🌙 *Buenas noches* — Добрий вечір\n"
            "👋 *¿Cómo estás?* — Як справи?\n😊 *Bien, gracias* — Добре, дякую\n"
            "🤝 *Mucho gusto* — Приємно познайомитись\n💬 *Hasta luego* — До зустрічі\n"
            "👋 *Adiós* — До побачення\n🙏 *Por favor* — Будь ласка\n"
            "💙 *Gracias* — Дякую\n😅 *Lo siento* — Вибачте\n\n"
            "💡 *tú* = неформальне 'ти'\n💡 *usted* = формальне 'Ви'"
        ),
        "all_questions": [
            {"q":"Як сказати 'Привіт'?","a":"Hola","wrong":["Adiós","Gracias","Buenos días","Buenas noches","Lo siento"]},
            {"q":"Що означає 'Buenos días'?","a":"Доброго ранку","wrong":["Добрий вечір","Добрий день","До побачення","Як справи?","Дякую"]},
            {"q":"Як спитати 'Як справи?'","a":"¿Cómo estás?","wrong":["¿Qué hora es?","¿Cómo te llamas?","¿Dónde estás?","¿Cuántos años tienes?","Hasta luego"]},
            {"q":"Що означає 'Mucho gusto'?","a":"Приємно познайомитись","wrong":["Дякую","Добре","До побачення","Вибачте","Будь ласка"]},
            {"q":"Як сказати 'До зустрічі'?","a":"Hasta luego","wrong":["Adiós","Hola","Gracias","Por favor","De nada"]},
            {"q":"Що означає 'Buenas noches'?","a":"Добрий вечір/ніч","wrong":["Доброго ранку","Добрий день","Привіт","До побачення","Як справи?"]},
            {"q":"Як сказати 'Дякую'?","a":"Gracias","wrong":["Por favor","De nada","Lo siento","Hola","Adiós"]},
            {"q":"Що означає 'Lo siento'?","a":"Вибачте/Шкода","wrong":["Дякую","Будь ласка","Привіт","Добре","Як справи?"]},
            {"q":"Як сказати 'Будь ласка'?","a":"Por favor","wrong":["Gracias","De nada","Lo siento","Mucho gusto","Hola"]},
            {"q":"Що означає 'Bien, gracias'?","a":"Добре, дякую","wrong":["Як справи?","Вибачте","До побачення","Приємно познайомитись","Будь ласка"]},
            {"q":"Яке звернення формальне?","a":"usted","wrong":["tú","yo","él","ella","nosotros"]},
            {"q":"Що означає 'Buenas tardes'?","a":"Добрий день","wrong":["Доброго ранку","Добрий вечір","Привіт","До побачення","Дякую"]},
        ]
    },
    {
        "id": 2, "title": "🔢 Урок 2: Числа 1–20",
        "theory": (
            "━━━━━━━━━━━━━━━━━━━━━━\n📖 *УРОК 2: Числа 1–20*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "1️⃣ uno  2️⃣ dos  3️⃣ tres  4️⃣ cuatro  5️⃣ cinco\n"
            "6️⃣ seis  7️⃣ siete  8️⃣ ocho  9️⃣ nueve  🔟 diez\n\n"
            "1️⃣1️⃣ once  1️⃣2️⃣ doce  1️⃣3️⃣ trece\n"
            "1️⃣4️⃣ catorce  1️⃣5️⃣ quince\n"
            "1️⃣6️⃣ dieciséis  1️⃣7️⃣ diecisiete\n"
            "1️⃣8️⃣ dieciocho  1️⃣9️⃣ diecinueve  2️⃣0️⃣ veinte\n\n"
            "💡 16-19 = dieci + (6-9)"
        ),
        "all_questions": [
            {"q":"Як буде '5' іспанською?","a":"cinco","wrong":["cuatro","seis","siete","tres","ocho"]},
            {"q":"Що означає 'diez'?","a":"10","wrong":["7","8","9","11","6"]},
            {"q":"Як буде '15' іспанською?","a":"quince","wrong":["catorce","trece","dieciséis","once","doce"]},
            {"q":"Що означає 'veinte'?","a":"20","wrong":["10","15","12","18","19"]},
            {"q":"Як буде '3' іспанською?","a":"tres","wrong":["dos","cuatro","uno","cinco","seis"]},
            {"q":"Що означає 'nueve'?","a":"9","wrong":["6","7","8","10","5"]},
            {"q":"Як буде '12' іспанською?","a":"doce","wrong":["once","trece","catorce","quince","diez"]},
            {"q":"Що означає 'ocho'?","a":"8","wrong":["6","7","9","10","5"]},
            {"q":"Як буде '17' іспанською?","a":"diecisiete","wrong":["dieciséis","dieciocho","diecinueve","veinte","quince"]},
            {"q":"Що означає 'catorce'?","a":"14","wrong":["13","15","12","16","11"]},
            {"q":"Як буде '1' іспанською?","a":"uno","wrong":["dos","tres","cuatro","cinco","seis"]},
            {"q":"Що означає 'siete'?","a":"7","wrong":["5","6","8","9","10"]},
        ]
    },
    {
        "id": 3, "title": "🎨 Урок 3: Кольори",
        "theory": (
            "━━━━━━━━━━━━━━━━━━━━━━\n📖 *УРОК 3: Кольори*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "❤️ *rojo* — червоний\n💛 *amarillo* — жовтий\n💙 *azul* — синій\n"
            "💚 *verde* — зелений\n🤍 *blanco* — білий\n🖤 *negro* — чорний\n"
            "🟠 *naranja* — помаранчевий\n🟣 *morado* — фіолетовий\n"
            "🩷 *rosa* — рожевий\n🟤 *marrón* — коричневий\n⚪ *gris* — сірий\n\n"
            "💡 Прикметники узгоджуються з іменником:\n"
            "• El coche *rojo* (м.р.) • La casa *roja* (ж.р.)"
        ),
        "all_questions": [
            {"q":"Як буде 'синій'?","a":"azul","wrong":["verde","rojo","amarillo","blanco","negro"]},
            {"q":"Що означає 'negro'?","a":"чорний","wrong":["білий","сірий","коричневий","фіолетовий","рожевий"]},
            {"q":"Як буде 'зелений'?","a":"verde","wrong":["blanco","naranja","rosa","azul","rojo"]},
            {"q":"Що означає 'amarillo'?","a":"жовтий","wrong":["помаранчевий","червоний","рожевий","коричневий","синій"]},
            {"q":"Як буде 'білий'?","a":"blanco","wrong":["negro","rojo","verde","azul","morado"]},
            {"q":"Що означає 'rosa'?","a":"рожевий","wrong":["червоний","фіолетовий","помаранчевий","коричневий","сірий"]},
            {"q":"Як буде 'коричневий'?","a":"marrón","wrong":["gris","negro","morado","naranja","rojo"]},
            {"q":"Що означає 'gris'?","a":"сірий","wrong":["коричневий","чорний","білий","фіолетовий","рожевий"]},
            {"q":"Як буде 'помаранчевий'?","a":"naranja","wrong":["rojo","amarillo","rosa","marrón","verde"]},
            {"q":"Що означає 'morado'?","a":"фіолетовий","wrong":["рожевий","синій","сірий","коричневий","чорний"]},
            {"q":"Яке закінчення у 'rojo' для жіночого роду?","a":"roja","wrong":["roje","rojos","rojas","roji","rojа"]},
            {"q":"Як буде 'червоний'?","a":"rojo","wrong":["naranja","rosa","marrón","morado","amarillo"]},
        ]
    },
    {
        "id": 4, "title": "👨‍👩‍👧 Урок 4: Родина",
        "theory": (
            "━━━━━━━━━━━━━━━━━━━━━━\n📖 *УРОК 4: Родина*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "👨 *el padre* — батько\n👩 *la madre* — мати\n"
            "👦 *el hijo* — син\n👧 *la hija* — дочка\n"
            "👴 *el abuelo* — дідусь\n👵 *la abuela* — бабуся\n"
            "👱 *el hermano* — брат\n👱‍♀️ *la hermana* — сестра\n"
            "👨‍💼 *el tío* — дядько\n👩‍💼 *la tía* — тітка\n"
            "👶 *el bebé* — немовля\n💑 *los padres* — батьки\n\n"
            "💡 *el* = чоловічий рід\n💡 *la* = жіночий рід"
        ),
        "all_questions": [
            {"q":"Як буде 'мати'?","a":"la madre","wrong":["el padre","la hija","la abuela","la hermana","la tía"]},
            {"q":"Що означає 'el hermano'?","a":"брат","wrong":["сестра","дядько","батько","дідусь","кузен"]},
            {"q":"Який артикль у 'hijo' (син)?","a":"el","wrong":["la","los","las","un","una"]},
            {"q":"Що означає 'la abuela'?","a":"бабуся","wrong":["дідусь","мати","тітка","сестра","дочка"]},
            {"q":"Як буде 'дочка'?","a":"la hija","wrong":["el hijo","la hermana","la madre","la tía","la abuela"]},
            {"q":"Що означає 'el tío'?","a":"дядько","wrong":["тітка","брат","батько","дідусь","кузен"]},
            {"q":"Як буде 'дідусь'?","a":"el abuelo","wrong":["la abuela","el padre","el tío","el hermano","el hijo"]},
            {"q":"Що означає 'los padres'?","a":"батьки","wrong":["діти","брати","дідусь і бабуся","дядьки","сестри"]},
            {"q":"Як буде 'сестра'?","a":"la hermana","wrong":["el hermano","la hija","la madre","la tía","la abuela"]},
            {"q":"Що означає 'el bebé'?","a":"немовля","wrong":["дитина","син","дочка","онук","племінник"]},
            {"q":"Як буде 'тітка'?","a":"la tía","wrong":["el tío","la hermana","la madre","la abuela","la hija"]},
            {"q":"Що означає 'el padre'?","a":"батько","wrong":["дідусь","брат","дядько","син","чоловік"]},
        ]
    },
    {
        "id": 5, "title": "🍎 Урок 5: Їжа",
        "theory": (
            "━━━━━━━━━━━━━━━━━━━━━━\n📖 *УРОК 5: Їжа*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🍞 *el pan* — хліб\n🥛 *la leche* — молоко\n🍳 *el huevo* — яйце\n"
            "🍗 *el pollo* — курка\n🐟 *el pescado* — риба\n"
            "🍚 *el arroz* — рис\n🥗 *la ensalada* — салат\n"
            "☕ *el café* — кава\n💧 *el agua* — вода\n🍷 *el vino* — вино\n"
            "🍎 *la manzana* — яблуко\n🧀 *el queso* — сир\n\n"
            "💡 *Tengo hambre* — Я голодний\n"
            "💡 *¡Buen provecho!* — Смачного!"
        ),
        "all_questions": [
            {"q":"Як буде 'хліб'?","a":"el pan","wrong":["la leche","el agua","el café","el arroz","el vino"]},
            {"q":"Що означає 'el pollo'?","a":"курка","wrong":["риба","яйце","рис","хліб","салат"]},
            {"q":"Як сказати 'Я голодний'?","a":"Tengo hambre","wrong":["Tengo sed","Tengo frío","Tengo sueño","Tengo miedo","Tengo razón"]},
            {"q":"Що означає 'el agua'?","a":"вода","wrong":["молоко","кава","вино","сік","чай"]},
            {"q":"Як буде 'кава'?","a":"el café","wrong":["el vino","la leche","el agua","el pan","el arroz"]},
            {"q":"Що означає 'la leche'?","a":"молоко","wrong":["вода","кава","сік","вино","чай"]},
            {"q":"Як буде 'риба'?","a":"el pescado","wrong":["el pollo","el arroz","el huevo","el pan","el queso"]},
            {"q":"Що означає 'el queso'?","a":"сир","wrong":["яйце","хліб","рис","курка","салат"]},
            {"q":"Як буде 'яблуко'?","a":"la manzana","wrong":["el arroz","la ensalada","el pan","el huevo","la leche"]},
            {"q":"Що означає 'la ensalada'?","a":"салат","wrong":["суп","рис","хліб","сир","курка"]},
            {"q":"Що означає '¡Buen provecho!'?","a":"Смачного!","wrong":["Будь ласка!","Дякую!","На здоров'я!","Привіт!","До побачення!"]},
            {"q":"Як буде 'яйце'?","a":"el huevo","wrong":["el pan","el queso","el arroz","el pollo","la leche"]},
        ]
    },
    {
        "id": 6, "title": "🕐 Урок 6: Час і дні тижня",
        "theory": (
            "━━━━━━━━━━━━━━━━━━━━━━\n📖 *УРОК 6: Час і дні тижня*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Пн *lunes* | Вт *martes* | Ср *miércoles*\n"
            "Чт *jueves* | Пт *viernes*\nСб *sábado* | Нд *domingo*\n\n"
            "⏰ *¿Qué hora es?* — Котра година?\n"
            "• *Es la una* — Перша година\n"
            "• *Son las dos* — Друга година\n"
            "• *Son las tres y media* — Пів на четверту\n"
            "• *Son las cinco menos cuarto* — Без чверті п'ять\n\n"
            "💡 'es' для 1-ї год, 'son' для решти!"
        ),
        "all_questions": [
            {"q":"Як буде 'понеділок'?","a":"lunes","wrong":["martes","miércoles","jueves","viernes","sábado"]},
            {"q":"Що означає '¿Qué hora es?'","a":"Котра година?","wrong":["Який день?","Яке число?","Як справи?","Де ти?","Скільки коштує?"]},
            {"q":"Як сказати 'Друга година'?","a":"Son las dos","wrong":["Es la dos","Es las dos","Son la dos","Son dos","Es dos"]},
            {"q":"Який день — 'viernes'?","a":"П'ятниця","wrong":["Четвер","Субота","Середа","Неділя","Понеділок"]},
            {"q":"Як буде 'неділя'?","a":"domingo","wrong":["sábado","viernes","lunes","martes","jueves"]},
            {"q":"Що означає 'miércoles'?","a":"Середа","wrong":["Вівторок","Четвер","П'ятниця","Субота","Понеділок"]},
            {"q":"Як сказати 'Перша година'?","a":"Es la una","wrong":["Son la una","Es las una","Son las una","Es uno","Son uno"]},
            {"q":"Що означає 'sábado'?","a":"Субота","wrong":["Неділя","П'ятниця","Четвер","Середа","Понеділок"]},
            {"q":"Як буде 'вівторок'?","a":"martes","wrong":["lunes","miércoles","jueves","viernes","domingo"]},
            {"q":"Що означає 'jueves'?","a":"Четвер","wrong":["Середа","П'ятниця","Вівторок","Субота","Понеділок"]},
            {"q":"Як сказати 'пів на четверту'?","a":"Son las tres y media","wrong":["Son las cuatro y media","Es la tres y media","Son las tres menos media","Son tres y media","Es tres y media"]},
            {"q":"Скільки днів у тижні іспанською?","a":"siete","wrong":["seis","ocho","cinco","nueve","diez"]},
        ]
    },
    {
        "id": 7, "title": "🔵 Урок 7: SER і ESTAR",
        "theory": (
            "━━━━━━━━━━━━━━━━━━━━━━\n📖 *УРОК 7: SER і ESTAR*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Обидва = 'бути', але різні!\n\n"
            "*SER* — постійні риси:\nyo *soy* | tú *eres* | él *es*\n"
            "nosotros *somos* | ellos *son*\n\n"
            "*ESTAR* — стан, місце:\nyo *estoy* | tú *estás* | él *está*\n"
            "nosotros *estamos* | ellos *están*\n\n"
            "💡 *Soy ucraniano* — Я українець (SER)\n"
            "💡 *Estoy cansado* — Я втомлений (ESTAR)\n"
            "💡 *Está en casa* — Він вдома (ESTAR)"
        ),
        "all_questions": [
            {"q":"Яка форма SER для 'я'?","a":"soy","wrong":["estoy","eres","es","somos","son"]},
            {"q":"Я втомлений = ?","a":"Estoy cansado","wrong":["Soy cansado","Es cansado","Estar cansado","Estás cansado","Somos cansados"]},
            {"q":"Яке дієслово для постійних рис?","a":"SER","wrong":["ESTAR","TENER","HACER","IR","PODER"]},
            {"q":"Яка форма ESTAR для 'він'?","a":"está","wrong":["es","estoy","estás","estamos","están"]},
            {"q":"Він вдома = ?","a":"Está en casa","wrong":["Es en casa","Estoy en casa","Son en casa","Ser en casa","Estás en casa"]},
            {"q":"Яка форма SER для 'ми'?","a":"somos","wrong":["estamos","son","eres","soy","es"]},
            {"q":"Я українець = ?","a":"Soy ucraniano","wrong":["Estoy ucraniano","Es ucraniano","Ser ucraniano","Somos ucranianos","Estás ucraniano"]},
            {"q":"Яка форма ESTAR для 'ви' (vosotros)?","a":"estáis","wrong":["estamos","están","estás","estoy","está"]},
            {"q":"Яке дієслово для місцезнаходження?","a":"ESTAR","wrong":["SER","TENER","IR","HACER","PODER"]},
            {"q":"Яка форма SER для 'вони'?","a":"son","wrong":["están","somos","eres","soy","es"]},
            {"q":"Ми в Польщі = ?","a":"Estamos en Polonia","wrong":["Somos en Polonia","Están en Polonia","Estoy en Polonia","Es en Polonia","Estar en Polonia"]},
            {"q":"Яка форма ESTAR для 'ти'?","a":"estás","wrong":["eres","estoy","está","estamos","están"]},
        ]
    },
    {
        "id": 8, "title": "🚶 Урок 8: TENER і вік",
        "theory": (
            "━━━━━━━━━━━━━━━━━━━━━━\n📖 *УРОК 8: TENER*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "yo *tengo* | tú *tienes* | él *tiene*\n"
            "nosotros *tenemos* | ellos *tienen*\n\n"
            "💡 *¿Cuántos años tienes?* — Скільки років?\n"
            "💡 *Tengo 30 años* — Мені 30 років\n\n"
            "*Вирази з TENER:*\n"
            "• *tener hambre* — бути голодним\n"
            "• *tener sed* — хотіти пити\n"
            "• *tener sueño* — хотіти спати\n"
            "• *tener miedo* — боятися\n"
            "• *tener razón* — бути правим\n"
            "• *tener prisa* — поспішати"
        ),
        "all_questions": [
            {"q":"Як сказати 'Мені 25 років'?","a":"Tengo 25 años","wrong":["Soy 25 años","Estoy 25 años","Tiene 25 años","Tienes 25 años","Tenemos 25 años"]},
            {"q":"Яка форма TENER для 'вони'?","a":"tienen","wrong":["tenemos","tiene","tengo","tienes","tener"]},
            {"q":"Що означає 'tener sueño'?","a":"хотіти спати","wrong":["боятися","хотіти пити","бути голодним","бути правим","поспішати"]},
            {"q":"Яка форма TENER для 'ми'?","a":"tenemos","wrong":["tienen","tengo","tiene","tienes","tener"]},
            {"q":"Як запитати 'Скільки тобі років?'","a":"¿Cuántos años tienes?","wrong":["¿Cómo estás?","¿Qué hora es?","¿Dónde vives?","¿Cómo te llamas?","¿Qué haces?"]},
            {"q":"Що означає 'tener prisa'?","a":"поспішати","wrong":["боятися","хотіти пити","бути правим","хотіти спати","бути голодним"]},
            {"q":"Яка форма TENER для 'ти'?","a":"tienes","wrong":["tengo","tiene","tenemos","tienen","tener"]},
            {"q":"Що означає 'tener miedo'?","a":"боятися","wrong":["поспішати","хотіти пити","бути голодним","хотіти спати","бути правим"]},
            {"q":"Яка форма TENER для 'я'?","a":"tengo","wrong":["tienes","tiene","tenemos","tienen","tener"]},
            {"q":"Що означає 'tener razón'?","a":"бути правим","wrong":["поспішати","боятися","хотіти пити","бути голодним","хотіти спати"]},
            {"q":"Я хочу пити = ?","a":"Tengo sed","wrong":["Tengo hambre","Tengo sueño","Tengo miedo","Tengo prisa","Tengo razón"]},
            {"q":"У мене є кішка = ?","a":"Tengo un gato","wrong":["Soy un gato","Estoy un gato","Tiene un gato","Tienes un gato","Hay un gato"]},
        ]
    },
    {
        "id": 9, "title": "👤 Урок 9: Займенники",
        "theory": (
            "━━━━━━━━━━━━━━━━━━━━━━\n📖 *УРОК 9: Займенники*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "*Особові займенники:*\n"
            "• *yo* — я\n• *tú* — ти (неформально)\n"
            "• *él* — він\n• *ella* — вона\n"
            "• *usted* — Ви (формально)\n"
            "• *nosotros* — ми\n• *vosotros* — ви (Іспанія)\n"
            "• *ellos* — вони (ч.р.)\n• *ellas* — вони (ж.р.)\n"
            "• *ustedes* — ви (Латинська Америка)\n\n"
            "💡 В іспанській займенники часто *опускають*:\n"
            "• *Hablo español* = Я говорю іспанською"
        ),
        "all_questions": [
            {"q":"Як буде 'ми' іспанською?","a":"nosotros","wrong":["vosotros","ellos","ustedes","ellas","usted"]},
            {"q":"Що означає 'ella'?","a":"вона","wrong":["він","ми","ви","вони","я"]},
            {"q":"Яке 'ви' у Латинській Америці?","a":"ustedes","wrong":["vosotros","usted","ellos","nosotros","tú"]},
            {"q":"Як буде 'вони' (жіночий рід)?","a":"ellas","wrong":["ellos","ustedes","nosotras","vosotras","ellas"]},
            {"q":"Що означає 'usted'?","a":"Ви (формально)","wrong":["ти","він","вона","ми","вони"]},
            {"q":"Як буде 'він' іспанською?","a":"él","wrong":["ella","usted","tú","yo","ellos"]},
            {"q":"Що означає 'vosotros'?","a":"ви (неформально, Іспанія)","wrong":["вони","ми","він","ви (формально)","я"]},
            {"q":"Як буде 'вони' (чоловічий рід)?","a":"ellos","wrong":["ellas","nosotros","ustedes","vosotros","usted"]},
            {"q":"Що означає 'yo'?","a":"я","wrong":["ти","він","вона","ми","вони"]},
            {"q":"Яке 'ви' неформальне в Іспанії?","a":"vosotros","wrong":["ustedes","usted","ellos","nosotros","tú"]},
            {"q":"Займенники в іспанській часто...?","a":"опускають","wrong":["подвоюють","пишуть першими","пишуть в кінці","змінюють форму","не існують"]},
            {"q":"Як буде 'ти' іспанською?","a":"tú","wrong":["yo","él","usted","nosotros","vosotros"]},
        ]
    },
    {
        "id": 10, "title": "📚 Урок 10: Теперішній час (-AR)",
        "theory": (
            "━━━━━━━━━━━━━━━━━━━━━━\n📖 *УРОК 10: Дієслова -AR*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Дієслова на *-AR* (hablar — говорити):\n\n"
            "yo habl*o* | tú habl*as* | él habl*a*\n"
            "nosotros habl*amos* | vosotros habl*áis* | ellos habl*an*\n\n"
            "*Інші дієслова -AR:*\n"
            "• *trabajar* — працювати\n• *estudiar* — вчитися\n"
            "• *caminar* — ходити\n• *comprar* — купувати\n"
            "• *escuchar* — слухати\n• *hablar* — говорити\n\n"
            "💡 *Trabajo mucho* — Я багато працюю\n"
            "💡 *Estudiamos español* — Ми вчимо іспанську"
        ),
        "all_questions": [
            {"q":"Яке закінчення 'hablar' для 'yo'?","a":"hablo","wrong":["hablas","habla","hablamos","habláis","hablan"]},
            {"q":"Як сказати 'Ми вчимося'?","a":"Estudiamos","wrong":["Estudian","Estudia","Estudias","Estudio","Estudiais"]},
            {"q":"Яке закінчення -AR для 'ellos'?","a":"-an","wrong":["-o","-as","-a","-amos","-áis"]},
            {"q":"Як сказати 'Він купує'?","a":"Compra","wrong":["Compro","Compras","Compramos","Compran","Compráis"]},
            {"q":"'Trabajar' означає?","a":"працювати","wrong":["говорити","вчитися","ходити","купувати","слухати"]},
            {"q":"Яке закінчення -AR для 'tú'?","a":"-as","wrong":["-o","-a","-amos","-áis","-an"]},
            {"q":"Як сказати 'Я слухаю'?","a":"Escucho","wrong":["Escuchas","Escucha","Escuchamos","Escuchan","Escuchamos"]},
            {"q":"'Caminar' означає?","a":"ходити","wrong":["бігти","їхати","летіти","плисти","стрибати"]},
            {"q":"Яке закінчення -AR для 'nosotros'?","a":"-amos","wrong":["-an","-as","-a","-áis","-o"]},
            {"q":"Як сказати 'Ти говориш'?","a":"Hablas","wrong":["Hablo","Habla","Hablamos","Habláis","Hablan"]},
            {"q":"'Comprar' означає?","a":"купувати","wrong":["продавати","дарувати","брати","мати","носити"]},
            {"q":"Яке закінчення -AR для 'vosotros'?","a":"-áis","wrong":["-amos","-an","-as","-a","-o"]},
        ]
    },
    {
        "id": 11, "title": "📗 Урок 11: Дієслова -ER і -IR",
        "theory": (
            "━━━━━━━━━━━━━━━━━━━━━━\n📖 *УРОК 11: Дієслова -ER і -IR*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "*-ER* (comer — їсти):\nyo com*o* | tú com*es* | él com*e*\n"
            "nosotros com*emos* | ellos com*en*\n\n"
            "*-IR* (vivir — жити):\nyo viv*o* | tú viv*es* | él viv*e*\n"
            "nosotros viv*imos* | ellos viv*en*\n\n"
            "*Популярні дієслова:*\n"
            "• *beber* — пити\n• *leer* — читати\n"
            "• *escribir* — писати\n• *abrir* — відкривати\n\n"
            "💡 *Como pizza* — Я їм піцу\n"
            "💡 *Vivo en Polonia* — Я живу в Польщі"
        ),
        "all_questions": [
            {"q":"Яке закінчення -ER для 'tú'?","a":"-es","wrong":["-o","-e","-emos","-en","-as"]},
            {"q":"Як сказати 'Я живу в Польщі'?","a":"Vivo en Polonia","wrong":["Vives en Polonia","Vive en Polonia","Vivimos en Polonia","Vivir en Polonia","Vivía en Polonia"]},
            {"q":"'Leer' означає?","a":"читати","wrong":["писати","пити","їсти","відкривати","говорити"]},
            {"q":"Яке закінчення -IR для 'nosotros'?","a":"-imos","wrong":["-amos","-emos","-en","-is","-an"]},
            {"q":"Як сказати 'Вони п'ють'?","a":"Beben","wrong":["Bebe","Bebes","Bebemos","Bebo","Bebéis"]},
            {"q":"Яке закінчення -ER для 'ellos'?","a":"-en","wrong":["-es","-e","-emos","-éis","-o"]},
            {"q":"'Escribir' означає?","a":"писати","wrong":["читати","говорити","слухати","бачити","думати"]},
            {"q":"Як сказати 'Ти їси'?","a":"Comes","wrong":["Como","Come","Comemos","Coméis","Comen"]},
            {"q":"Яке закінчення -IR для 'ellos'?","a":"-en","wrong":["-es","-e","-imos","-ís","-o"]},
            {"q":"'Abrir' означає?","a":"відкривати","wrong":["закривати","брати","давати","бачити","чути"]},
            {"q":"Як сказати 'Ми читаємо'?","a":"Leemos","wrong":["Leen","Lee","Lees","Leo","Leéis"]},
            {"q":"Яке закінчення -ER для 'yo'?","a":"-o","wrong":["-es","-e","-emos","-éis","-en"]},
        ]
    },
    {
        "id": 12, "title": "🔊 Урок 12: Фонетика",
        "theory": (
            "━━━━━━━━━━━━━━━━━━━━━━\n📖 *УРОК 12: Фонетика*\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "*Особливі звуки:*\n\n"
            "🔤 *ñ* = [нь] — España, mañana\n"
            "🔤 *ll* = [й] — llamar, llover\n"
            "🔤 *rr* = [р, вібрант] — perro, carro\n"
            "🔤 *h* = мовчить — hola, hacer\n"
            "🔤 *j* = [х] — jardín, jugar\n"
            "🔤 *c+e/i* = [с/θ] — ciudad, cerro\n"
            "🔤 *g+e/i* = [х] — gente, gitano\n"
            "🔤 *qu* = [к] — queso, querer\n\n"
            "💡 *mañana* = завтра/ранок\n"
            "💡 *España* = Іспанія\n"
            "💡 *perro* = собака"
        ),
        "all_questions": [
            {"q":"Як читається 'h' в іспанській?","a":"Мовчить","wrong":["як [х]","як [г]","як [h]","як [ф]","як [в]"]},
            {"q":"Як читається 'ñ'?","a":"[нь]","wrong":["[н]","[м]","[ж]","[й]","[х]"]},
            {"q":"Що означає 'mañana'?","a":"завтра / ранок","wrong":["вечір","сьогодні","місяць","рік","тиждень"]},
            {"q":"Як читається 'j' в іспанській?","a":"[х]","wrong":["[дж]","[ж]","[й]","[г]","мовчить"]},
            {"q":"'ll' читається як?","a":"[й]","wrong":["[л]","[лл]","[в]","[х]","[н]"]},
            {"q":"Як читається 'qu'?","a":"[к]","wrong":["[кв]","[к+у]","[х]","[г]","[ч]"]},
            {"q":"Що означає 'España'?","a":"Іспанія","wrong":["Франція","Португалія","Мексика","Аргентина","Бразилія"]},
            {"q":"Як читається 'rr'?","a":"[р, вібрант]","wrong":["[р, звичайний]","[рр]","мовчить","[л]","[в]"]},
            {"q":"'perro' означає?","a":"собака","wrong":["кіт","кінь","птах","риба","корова"]},
            {"q":"Як читається 'g' перед 'e' і 'i'?","a":"[х]","wrong":["[г]","[ж]","[й]","[дж]","мовчить"]},
            {"q":"Скільки голосних в іспанській?","a":"5","wrong":["4","6","7","3","8"]},
            {"q":"Наголос в іспанській позначається знаком...?","a":"´ (акут)","wrong":["` (грав)","^ (циркумфлекс)","¨ (умлаут)","~ (тильда)","¸ (седиль)"]},
        ]
    },
]

FLASHCARDS = [
    {"es":"hola","ua":"привіт","cat":"привітання"},
    {"es":"gracias","ua":"дякую","cat":"ввічливість"},
    {"es":"por favor","ua":"будь ласка","cat":"ввічливість"},
    {"es":"sí","ua":"так","cat":"базові"},
    {"es":"no","ua":"ні","cat":"базові"},
    {"es":"perdón","ua":"вибачте","cat":"ввічливість"},
    {"es":"de nada","ua":"нема за що","cat":"ввічливість"},
    {"es":"uno","ua":"один","cat":"числа"},
    {"es":"dos","ua":"два","cat":"числа"},
    {"es":"tres","ua":"три","cat":"числа"},
    {"es":"diez","ua":"десять","cat":"числа"},
    {"es":"veinte","ua":"двадцять","cat":"числа"},
    {"es":"cien","ua":"сто","cat":"числа"},
    {"es":"rojo","ua":"червоний","cat":"кольори"},
    {"es":"azul","ua":"синій","cat":"кольори"},
    {"es":"verde","ua":"зелений","cat":"кольори"},
    {"es":"negro","ua":"чорний","cat":"кольори"},
    {"es":"blanco","ua":"білий","cat":"кольори"},
    {"es":"amarillo","ua":"жовтий","cat":"кольори"},
    {"es":"el pan","ua":"хліб","cat":"їжа"},
    {"es":"el agua","ua":"вода","cat":"їжа"},
    {"es":"el café","ua":"кава","cat":"їжа"},
    {"es":"el pollo","ua":"курка","cat":"їжа"},
    {"es":"la leche","ua":"молоко","cat":"їжа"},
    {"es":"el arroz","ua":"рис","cat":"їжа"},
    {"es":"la madre","ua":"мати","cat":"родина"},
    {"es":"el padre","ua":"батько","cat":"родина"},
    {"es":"el hermano","ua":"брат","cat":"родина"},
    {"es":"la hermana","ua":"сестра","cat":"родина"},
    {"es":"hablar","ua":"говорити","cat":"дієслова"},
    {"es":"comer","ua":"їсти","cat":"дієслова"},
    {"es":"vivir","ua":"жити","cat":"дієслова"},
    {"es":"trabajar","ua":"працювати","cat":"дієслова"},
    {"es":"estudiar","ua":"вчитися","cat":"дієслова"},
    {"es":"beber","ua":"пити","cat":"дієслова"},
    {"es":"leer","ua":"читати","cat":"дієслова"},
    {"es":"escribir","ua":"писати","cat":"дієслова"},
    {"es":"tener","ua":"мати","cat":"дієслова"},
    {"es":"ser","ua":"бути (постійно)","cat":"дієслова"},
    {"es":"estar","ua":"бути (тимчасово)","cat":"дієслова"},
    {"es":"yo","ua":"я","cat":"займенники"},
    {"es":"tú","ua":"ти","cat":"займенники"},
    {"es":"él","ua":"він","cat":"займенники"},
    {"es":"ella","ua":"вона","cat":"займенники"},
    {"es":"nosotros","ua":"ми","cat":"займенники"},
    {"es":"ellos","ua":"вони","cat":"займенники"},
    {"es":"la casa","ua":"будинок","cat":"місця"},
    {"es":"la ciudad","ua":"місто","cat":"місця"},
    {"es":"el trabajo","ua":"робота","cat":"місця"},
    {"es":"la tienda","ua":"магазин","cat":"місця"},
]

users_db = {}

def get_user(uid):
    k = str(uid)
    if k not in users_db:
        users_db[k] = {
            "xp": 0, "streak": 0, "last_date": None,
            "completed_lessons": [], "known_cards": [],
            "flash_idx": 0, "notify_hour": 9, "notify_enabled": True,
            "quiz_lesson": None, "quiz_questions": [], "quiz_idx": 0, "quiz_correct": 0,
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
        (0,"🥚 Початківець",100),(100,"🐣 Новачок",300),(300,"📚 Студент",600),
        (600,"🎓 Учень",1000),(1000,"⭐ Знавець",1500),(1500,"🌟 Майстер",2500),(2500,"🏆 Експерт",9999),
    ]
    for min_xp, name, max_xp in levels:
        if xp < max_xp:
            return name, min_xp, max_xp
    return levels[-1][1], 2500, 9999

def main_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📖 Уроки", callback_data="menu_lessons"),
         InlineKeyboardButton("🃏 Флешкарти", callback_data="menu_flash")],
        [InlineKeyboardButton("🧠 Квіз", callback_data="menu_quiz"),
         InlineKeyboardButton("🎮 Гра", callback_data="menu_game")],
        [InlineKeyboardButton("📊 Прогрес", callback_data="menu_progress"),
         InlineKeyboardButton("🔔 Нагадування", callback_data="menu_notify")],
    ])

def back_kb():
    return InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Головне меню", callback_data="menu_main")]])

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    get_user(user.id)
    await update.message.reply_text(
        f"🇪🇸 *¡Hola, {user.first_name}!*\n\n"
        "Ласкаво просимо до бота для вивчення іспанської!\n\n"
        "📖 *Уроки* — теорія з нуля\n"
        "🃏 *Флешкарти* — слова\n"
        "🧠 *Квіз* — 10 рандомних питань\n"
        "🎮 *Гра* — вчи слова як у Duolingo\n"
        "🔔 *Нагадування* — щоденні пуші\n\n"
        "З чого починаємо? 👇",
        parse_mode="Markdown", reply_markup=main_kb()
    )

async def handle_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    uid = q.from_user.id
    u = get_user(uid)

    if data == "menu_main":
        await q.edit_message_text(
            "🇪🇸 *Головне меню*", parse_mode="Markdown", reply_markup=main_kb()
        )

    elif data == "menu_lessons":
        rows = []
        for l in LESSONS:
            done = l["id"] in u["completed_lessons"]
            mark = "✅" if done else "▸"
            rows.append([InlineKeyboardButton(f"{mark} {l['title']}", callback_data=f"lesson_{l['id']}")])
        rows.append([InlineKeyboardButton("◀️ Назад", callback_data="menu_main")])
        await q.edit_message_text("📖 *Уроки*\n\nОбирай урок:", parse_mode="Markdown",
                                   reply_markup=InlineKeyboardMarkup(rows))

    elif data.startswith("lesson_"):
        lid = int(data.split("_")[1])
        lesson = next(l for l in LESSONS if l["id"] == lid)
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🧠 Пройти квіз (10 питань)", callback_data=f"quiz_lesson_{lid}")],
            [InlineKeyboardButton("◀️ До уроків", callback_data="menu_lessons")],
        ])
        await q.edit_message_text(lesson["theory"], parse_mode="Markdown", reply_markup=kb)

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

    elif data == "menu_quiz":
        rows = [[InlineKeyboardButton(l["title"], callback_data=f"quiz_lesson_{l['id']}")] for l in LESSONS]
        rows.append([InlineKeyboardButton("🎲 Випадковий урок", callback_data="quiz_random")])
        rows.append([InlineKeyboardButton("◀️ Назад", callback_data="menu_main")])
        await q.edit_message_text("🧠 *Квіз*\n\nОбирай тему:", parse_mode="Markdown",
                                   reply_markup=InlineKeyboardMarkup(rows))

    elif data.startswith("quiz_lesson_") or data == "quiz_random":
        if data == "quiz_random":
            lesson = random.choice(LESSONS)
        else:
            lid = int(data.split("_")[2])
            lesson = next(l for l in LESSONS if l["id"] == lid)
        # Беремо 10 рандомних питань з перемішуванням
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

    elif data == "menu_progress":
        xp = u["xp"]
        level, min_xp, max_xp = get_level(xp)
        progress = xp - min_xp
        total = max_xp - min_xp
        filled = int(progress / total * 10) if total > 0 else 10
        bar = "█" * filled + "░" * (10 - filled)
        text = (
            f"📊 *Твій прогрес*\n\n"
            f"🏅 Рівень: *{level}*\n"
            f"⭐ XP: *{xp}*\n"
            f"[{bar}] {progress}/{total}\n\n"
            f"🔥 Серія: *{u['streak']} днів*\n"
            f"📖 Уроків: *{len(u['completed_lessons'])}/{len(LESSONS)}*\n"
            f"🃏 Слів: *{len(u['known_cards'])}/{len(FLASHCARDS)}*\n\n"
        )
        if len(u["completed_lessons"]) == 0:
            text += "💡 Починай з першого уроку!"
        elif len(u["completed_lessons"]) < len(LESSONS):
            text += f"💪 Ще {len(LESSONS) - len(u['completed_lessons'])} уроків!"
        else:
            text += "🎉 Усі уроки пройдено! ¡Fantástico!"
        await q.edit_message_text(text, parse_mode="Markdown", reply_markup=back_kb())

    elif data == "menu_notify":
        status = "🟢 Увімкнено" if u["notify_enabled"] else "🔴 Вимкнено"
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔕 Вимкнути" if u["notify_enabled"] else "🔔 Увімкнути",
                                  callback_data="notify_toggle")],
            [InlineKeyboardButton("⏰ Змінити час", callback_data="notify_time")],
            [InlineKeyboardButton("◀️ Назад", callback_data="menu_main")],
        ])
        await q.edit_message_text(
            f"🔔 *Нагадування*\n\nСтатус: {status}\nЧас: *{u['notify_hour']:02d}:00*",
            parse_mode="Markdown", reply_markup=kb
        )

    elif data == "notify_toggle":
        u["notify_enabled"] = not u["notify_enabled"]
        status = "🟢 Увімкнено" if u["notify_enabled"] else "🔴 Вимкнено"
        await q.edit_message_text(f"✅ Нагадування: *{status}*",
                                   parse_mode="Markdown", reply_markup=back_kb())

    elif data == "notify_time":
        hours = [[InlineKeyboardButton(f"{h:02d}:00", callback_data=f"notifyset_{h}") for h in range(i, min(i+4, 23))]
                 for i in range(7, 23, 4)]
        hours.append([InlineKeyboardButton("◀️ Назад", callback_data="menu_notify")])
        await q.edit_message_text("⏰ Обери час:", reply_markup=InlineKeyboardMarkup(hours))

    elif data.startswith("notifyset_"):
        hour = int(data.split("_")[1])
        u["notify_hour"] = hour
        await q.edit_message_text(f"✅ Нагадування о *{hour:02d}:00*",
                                   parse_mode="Markdown", reply_markup=back_kb())

    elif data == "menu_game":
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎯 Вгадай переклад", callback_data="game_mc")],
            [InlineKeyboardButton("✍️ Напиши слово", callback_data="game_write")],
            [InlineKeyboardButton("◀️ Назад", callback_data="menu_main")],
        ])
        await q.edit_message_text("🎮 *Ігровий режим*\n\nОбери тип:", parse_mode="Markdown", reply_markup=kb)

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
    known = len(u["known_cards"])
    if not reveal:
        text = (f"🃏 *Флешкарта {idx+1}/{len(FLASHCARDS)}*\n_{card['cat']}_\n\n"
                f"🇪🇸 *{card['es']}*\n\nЗнаєш переклад?")
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("👁 Показати", callback_data="flash_show")],
            [InlineKeyboardButton("➡️ Далі", callback_data="flash_next"),
             InlineKeyboardButton("🎲 Випадкова", callback_data="flash_random")],
            [InlineKeyboardButton("◀️ Меню", callback_data="menu_main")],
        ])
    else:
        text = (f"🃏 *Флешкарта {idx+1}/{len(FLASHCARDS)}*\n_{card['cat']}_\n\n"
                f"🇪🇸 *{card['es']}*\n🇺🇦 *{card['ua']}*\n\n✅ Вивчено: {known}/{len(FLASHCARDS)}")
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Знаю!", callback_data="flash_know"),
             InlineKeyboardButton("🔄 Далі", callback_data="flash_next")],
            [InlineKeyboardButton("◀️ Меню", callback_data="menu_main")],
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
        await q.edit_message_text(
            f"✅ *Квіз завершено!*\n\n"
            f"Правильно: *{correct}/{total}* ({pct}%)\n"
            f"{emoji} {'¡Perfecto!' if pct==100 else '¡Bien!' if pct>=60 else 'Practíca más!'}\n\n"
            f"⭐ +{xp} XP отримано!",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Ще раз (нові питання!)", callback_data=f"quiz_lesson_{lesson['id']}")],
                [InlineKeyboardButton("◀️ Меню", callback_data="menu_main")],
            ])
        )
        return

    q_data = questions[qi]
    # Рандомно вибираємо 3 неправильних + правильна = 4 варіанти
    wrong = random.sample(q_data["wrong"], min(3, len(q_data["wrong"])))
    options = wrong + [q_data["a"]]
    random.shuffle(options)

    kb = InlineKeyboardMarkup([[InlineKeyboardButton(opt, callback_data=f"qans_{opt}")] for opt in options])
    await q.edit_message_text(
        f"🧠 *Питання {qi+1}/{len(questions)}*\n\n{q_data['q']}",
        parse_mode="Markdown", reply_markup=kb
    )


async def handle_quiz_answer(q, uid, answer):
    u = get_user(uid)
    questions = u["quiz_questions"]
    qi = u["quiz_idx"]
    q_data = questions[qi]
    correct = answer == q_data["a"]
    if correct:
        u["quiz_correct"] += 1
        text = f"✅ *Правильно!* ¡Correcto!\n\n✔️ *{q_data['a']}*"
    else:
        text = f"❌ *Неправильно.*\nТи обрав: _{answer}_\n✅ Правильно: *{q_data['a']}*"
    u["quiz_idx"] += 1
    await q.edit_message_text(text, parse_mode="Markdown",
                               reply_markup=InlineKeyboardMarkup([[
                                   InlineKeyboardButton("➡️ Далі", callback_data="quiz_next")
                               ]]))


async def show_game(q, uid):
    u = get_user(uid)
    cards = u["game_cards"]
    gi = u["game_idx"]

    if gi >= len(cards):
        correct = u["game_correct"]
        total = len(cards)
        xp = correct * 10
        add_xp(uid, xp)
        pct = int(correct / total * 100)
        await q.edit_message_text(
            f"🎮 *Гру завершено!*\n\nПравильно: *{correct}/{total}* ({pct}%)\n⭐ +{xp} XP\n\n"
            f"{'🏆 ¡Excelente!' if pct==100 else '👍 ¡Bien!' if pct>=60 else '💪 Practíca más!'}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Ще раз", callback_data=u["game_mode"])],
                [InlineKeyboardButton("◀️ Меню", callback_data="menu_main")],
            ])
        )
        return

    card = cards[gi]
    mode = u["game_mode"]

    if mode == "game_mc":
        all_ua = [c["ua"] for c in FLASHCARDS if c["ua"] != card["ua"]]
        wrong3 = random.sample(all_ua, 3)
        options = wrong3 + [card["ua"]]
        random.shuffle(options)
        kb = InlineKeyboardMarkup([[InlineKeyboardButton(opt, callback_data=f"gans_{opt}")] for opt in options])
        await q.edit_message_text(
            f"🎮 *Гра {gi+1}/{len(cards)}*\n\n🇪🇸 *{card['es']}*\n\nЯк перекласти?",
            parse_mode="Markdown", reply_markup=kb
        )
    else:
        u["waiting_input"] = {"type": "game_write", "answer": card["es"], "ua": card["ua"]}
        await q.edit_message_text(
            f"✍️ *Гра {gi+1}/{len(cards)}*\n\n🇺🇦 *{card['ua']}*\n\nНапиши іспанською:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⏭ Пропустити", callback_data="gans_SKIP")
            ]])
        )


async def handle_game_answer(q, uid, answer):
    u = get_user(uid)
    card = u["game_cards"][u["game_idx"]]
    correct_ans = card["ua"] if u["game_mode"] == "game_mc" else card["es"]
    correct = answer == correct_ans
    if answer == "SKIP":
        text = f"⏭ *Пропущено*\n✅ Правильно: *{correct_ans}*"
    elif correct:
        u["game_correct"] += 1
        text = "✅ *Правильно!* ¡Correcto!"
    else:
        text = f"❌ *Неправильно.*\n✅ Правильно: *{correct_ans}*"
    u["game_idx"] += 1
    u["waiting_input"] = None
    await q.edit_message_text(text, parse_mode="Markdown",
                               reply_markup=InlineKeyboardMarkup([[
                                   InlineKeyboardButton("➡️ Далі", callback_data="game_next")
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
            reply = f"✅ *Правильно!*\n_{wi['ua']}_ = *{wi['answer']}*"
        else:
            reply = f"❌ *Неправильно.*\nТи написав: _{text}_\n✅ Правильно: *{wi['answer']}*"
        u["game_idx"] += 1
        u["waiting_input"] = None
        await update.message.reply_text(reply, parse_mode="Markdown",
                                         reply_markup=InlineKeyboardMarkup([[
                                             InlineKeyboardButton("➡️ Далі", callback_data="game_next")
                                         ]]))
    else:
        await update.message.reply_text("Головне меню 👇", reply_markup=main_kb())


REMINDERS = [
    "🇪🇸 *¡Buenos días!* Час вчити іспанську! 💪",
    "🌟 *¡Hola!* Не забудь про урок сьогодні! 🔥",
    "📚 Слово дня: *mañana* = завтра/ранок 🇪🇸",
    "🎯 *¡Ánimo!* Твій квіз чекає! 💃",
    "⭐ Не переривай серію — вчи іспанську! 🇪🇸",
]

async def send_daily_reminders(app):
    while True:
        from datetime import datetime
        now = datetime.now()
        for uid, u in list(users_db.items()):
            if u["notify_enabled"] and now.hour == u["notify_hour"] and now.minute == 0:
                try:
                    await app.bot.send_message(
                        chat_id=int(uid), text=random.choice(REMINDERS),
                        parse_mode="Markdown", reply_markup=main_kb()
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

    print("🤖 Бот v3.0 запущено!")
    app.run_polling(drop_pending_updates=True)
