
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor

BOT_TOKEN = "7667691336:AAHYJO_Vaf5RRuF-aJraY1yYZa_Ya2jK1yg"
GEMINI_API_KEY = "AIzaSyC4JhbXXVpb0HfMJlsZHjJqT77DXtJooS0"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

def ask_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta3/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    headers = { "Content-Type": "application/json" }
    data = {
        "contents": [{ "parts": [{ "text": prompt }] }]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except:
            return "حدث خطأ في تحليل رد الذكاء الاصطناعي."
    else:
        return f"حدث خطأ: {response.text}"

@dp.message_handler()
async def handle_message(message: Message):
    user_input = message.text
    await message.chat.do("typing")
    prompt = f"أجب بصيغة شخصية اسمها حكيم، ذكية، مهذبة، وتتكلم بالفصحى:\n\n{user_input}"
    ai_reply = ask_gemini(prompt)
    await message.reply(ai_reply)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
