from datetime import datetime
import os
import discord
from discord.ext import commands,tasks
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

bot = commands.Bot("!")



@tasks.loop(hours=24)
async def called_once_a_day():
    message_channel = bot.get_channel(int(CHANNEL_ID))
    print(f"Got channel {message_channel}")
    if datetime.now().weekday() <= 4:
        await message_channel.send("@everyone Please Complete your Daily Stand-up by 8pm. BEEP BOOP Here is the Link: https://drive.google.com/drive/folders/1yWNESub8Ya61OzLj0Wzkrg1MsVWaoqSy BEEP BOOP ")

@called_once_a_day.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")

called_once_a_day.start()
#Put this at the bottom of your .py file
try:
    bot.run(DISCORD_TOKEN)
except discord.errors.LoginFailure as e:
    print("Login unsuccessful.")
    print(DISCORD_TOKEN)


