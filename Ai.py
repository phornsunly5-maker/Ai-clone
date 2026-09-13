import telebot
import requests

# ដាក់ Token និង API Key របស់អ្នកនៅទីនេះ
TELEGRAM_TOKEN = "8888082315:AAEEt0_g1AnpY3_ZZYKFGGeR2X3u5q7LgN8"
OPENROUTER_API = "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"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# សម្រាប់រក្សាទុក Model ដែល User ម្នាក់ៗបានជ្រើសរើស
user_models = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "សួស្តី! ខ្ញុំជា AI Bot។ សូមវាយបញ្ជា /model ដើម្បីជ្រើសរើស Claude Model ដែលអ្នកចង់ប្រើ។")

@bot.message_handler(commands=['model'])
def choose_model(message):
    text = "សូមជ្រើសរើស Model (វាយលេខតំណាង):\n1. Claude 3.5 Sonnet\n2. Claude 3 Haiku\n3. Claude 3 Opus"
    msg = bot.reply_to(message, text)
    bot.register_next_step_handler(msg, set_model)

def set_model(message):
    models = {
        "1": "anthropic/claude-3.5-sonnet", 
        "2": "anthropic/claude-3-haiku", 
        "3": "anthropic/claude-3-opus"
    }
    
    if message.text in models:
        user_models[message.chat.id] = models[message.text]
        bot.reply_to(message, f"✅ បានប្តូរទៅកាន់ {models[message.text]} ដោយជោគជ័យ!")
    else:
        bot.reply_to(message, "❌ សូមជ្រើសរើសតែលេខ 1, 2 ឬ 3 ប៉ុណ្ណោះ។ សូមវាយ /model ម្តងទៀត។")

@bot.message_handler(func=lambda message: True)
def chat_with_ai(message):
    # កំណត់ Claude 3.5 Sonnet ជា Model ដើមប្រសិនបើមិនទាន់បានរើស
    model = user_models.get(message.chat.id, "anthropic/claude-3.5-sonnet")
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": message.text}]
    }
    
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        if response.status_code == 200:
            reply = response.json()['choices'][0]['message']['content']
            bot.reply_to(message, reply)
        else:
            bot.reply_to(message, f"មានបញ្ហាក្នុងការភ្ជាប់ API: {response.status_code}")
    except Exception as e:
        bot.reply_to(message, "មានបញ្ហាបច្ចេកទេសសូមព្យាយាមម្តងទៀត។")

# ដំណើរការ Bot អោយដើររហូត
bot.polling()
