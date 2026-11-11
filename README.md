# Telegram AI Bot

Telegram-e live message-er reply AI diye automatic dey.

## Setup
1. Telegram-e @BotFather -> /newbot -> token nao.
2. Gemini API key nao (free): https://aistudio.google.com
3. Run:
   ```
   pip install -r requirements.txt
   cp .env.example .env   # .env te token ar key boshao
   python bot.py
   ```
4. Telegram-e bot ke message pathao. `/reset` dile memory clear hobe.

## 24/7 chalate
Railway / Render / VPS e deploy koro, `python bot.py` start command, ar
environment variables e token ar key dao.

## GitHub e upload
```
git init
git add .
git commit -m "telegram ai bot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/telegram-ai-bot.git
git push -u origin main
```
`.env` file kokhono push korbe na (.gitignore e ache).

## Render (Web Service) settings
- Runtime: Python
- Build command: `pip install -r requirements.txt`
- Start command: `python bot.py`
- Environment: `TELEGRAM_BOT_TOKEN`, `GEMINI_API_KEY` (Render dashboard e nijе boshao)
- Free plan e kichukkhon traffic na ashle service ghumiye jete pare.
  UptimeRobot diye service URL e proti 5 minute e ping korle jege thakbe.
