from datetime import datetime,time,timedelta
import os
import discord
from discord.ext import commands,tasks
from dotenv import load_dotenv
import asyncio

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

bot = commands.Bot(command_prefix="$")
WHEN = time(23, 30, 0)  # 6:00 PM


async def called_once_a_day():  # Fired every day
    await bot.wait_until_ready()  # Make sure your guild cache is ready so the channel can be found via get_channel
    channel = bot.get_channel(int(CHANNEL_ID)) # Note: It's more efficient to do bot.get_guild(guild_id).get_channel(channel_id) as there's less looping involved, but just get_channel still works fine
    if datetime.utcnow().weekday()<=4:
        await channel.send("@everyone Please Complete your Daily Stand-up by 8pm. BEEP BOOP Here is the Link: https://drive.google.com/drive/folders/1yWNESub8Ya61OzLj0Wzkrg1MsVWaoqSy BEEP BOOP ")

async def background_task():
    now = datetime.utcnow() #check if you can change this to eastern!!!!!!!!!!!!!SWAG
   
    if now.time() > WHEN:  # Make sure loop doesn't start after {WHEN} as then it will send immediately the first time as negative seconds will make the sleep yield instantly
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        print("if state")
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start 
    while True:
        now = datetime.utcnow() # You can do now() or a specific timezone if that matters, but I'll leave it with utcnow
        target_time = datetime.combine(now.date(), WHEN)  # 6:00 PM today (In UTC)
        seconds_until_target = (target_time - now).total_seconds()
        print(seconds_until_target)
        await asyncio.sleep(seconds_until_target)  # Sleep until we hit the target time
        await called_once_a_day()  # Call the helper function that sends the message
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start a new iteration


if __name__ == "__main__":
    bot.loop.create_task(background_task())
    bot.run(DISCORD_TOKEN)

# @tasks.loop(hours=24)
# async def called_once_a_day():
#     message_channel = bot.get_channel(int(CHANNEL_ID))
#     print(f"Got channel {message_channel}")
#     if datetime.now().weekday() <= 4:
#         await message_channel.send("@everyone Please Complete your Daily Stand-up by 8pm. BEEP BOOP Here is the Link: https://drive.google.com/drive/folders/1yWNESub8Ya61OzLj0Wzkrg1MsVWaoqSy BEEP BOOP ")

# @called_once_a_day.before_loop
# async def before():
#     await bot.wait_until_ready()
#     print("Finished waiting")

# called_once_a_day.start()
# #Put this at the bottom of your .py file
# try:
#     bot.run(DISCORD_TOKEN)
# except discord.errors.LoginFailure as e:
#     print("Login unsuccessful.")
#     print(DISCORD_TOKEN)


