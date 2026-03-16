from vkbottle.bot import Bot, Message

TOKEN = "vk1.a.d1di-U35S6MsVen997mHz5Bdhjs6reaOuq3n5Ham8Fz6hzJxJHoRBwNXEtR5_FICAefWNt1jua52v_IOMCCB6gqMHsZ1xxG6gEPyeNNy4Awg3Njf95yvYEXKiJxPdiNOlbrhhj1OR2MflC4zwRkWpxHvzULn9Ynk8RBvPlevDMs36yHupojQttXHsA6iCzpnQVzK8xLR22s0h1Cd0rFHBg"

bot = Bot(TOKEN)

@bot.on.message(text = "/start")

async def start_handler(message:Message):
    await message.answer("Я бот")

@bot.on.message(text = "Прив")

async def hi_handler(message:Message):
    user_id = message.from_id
    await message.answer(f"q {user_id}")

@bot.on.message()
async def any_message(message:Message):
    user_id = message.from_id
    text = message.text
    if text:
        await message.answer(f"{text}, {user_id}")

if __name__ == "__main__":
    print("Bot works")
    bot.run_forever()