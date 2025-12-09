import requests
from aiogram import Bot, Dispatcher, executor, types

BOT_TOKEN = "8023296312:AAFZvasvkaPKwvmfkPHXf5Q7AmoDaJLSvNg"
DEEPSEEK_API_KEY = "sk-db5ee4e0e1db436c835b1344f2ed20c7"
API_URL = "https://api.deepseek.com/v1/chat/completions"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

def clean_text(text: str) -> str:
    text = text.replace("###", "")
    text = text.replace("*", "")
    text = text.replace("**", "")
    return text.strip()

def ask_deepseek(prompt: str):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {DEEPSEEK_API_KEY}",}
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt},],
        "max_tokens": 500,
        "temperature": 0.7,
    }
    response = requests.post(API_URL, json=payload, headers=headers, timeout=40)
    data = response.json()
    return data["choices"][0]["message"]["content"]

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f"👋 *Salom!* \nSavolingizni yuboring, imkon qadar aniq va professional tarzda javob beraman")

@dp.message_handler(content_types=['text'])
async def chat(message: types.Message):
    user_text = message.text.strip()
    wait_msg = await message.answer("⏳ Yozayapman...")
    reply = ask_deepseek(user_text)
    cleaned = clean_text(reply)
    await wait_msg.delete()
    await message.answer(cleaned)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
