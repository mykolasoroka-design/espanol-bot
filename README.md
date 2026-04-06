# 🇪🇸 Бот для вивчення іспанської

## Функції
- 📖 8 уроків (привітання, числа, кольори, родина, їжа, час, ser/estar, tener)
- 🃏 Флешкарти (47 слів)
- 🧠 Квізи по кожному уроку
- 📊 Прогрес і рівні
- 📝 Словник по категоріях

## Запуск на Railway (безкоштовно)

1. Зареєструйся на https://railway.app
2. Натисни "New Project" → "Deploy from GitHub"
3. Або "New Project" → "Empty Project" → "Add Service" → "GitHub Repo"

Або просто:
1. Завантаж файли на GitHub (новий репозиторій)
2. Підключи Railway до репозиторію
3. Додай змінну середовища: BOT_TOKEN=твій_токен

## Отримати токен бота

1. Відкрий Telegram → знайди @BotFather
2. Напиши /newbot
3. Дай ім'я боту (наприклад: "Іспанська для Миколи")
4. Дай username (наприклад: @mykola_espanol_bot)
5. Скопіюй токен

## Локальний запуск

```bash
pip install -r requirements.txt
export BOT_TOKEN=твій_токен
python bot.py
```
