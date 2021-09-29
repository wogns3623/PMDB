import sys
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv


from Utils import log, errlog

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
# TOKEN = os.getenv('TEST_TOKEN')

app = commands.Bot(command_prefix="!")

for filename in os.listdir("Cogs"):
    if filename.endswith(".py"):
        app.load_extension(f"Cogs.{filename[:-3]}")


@app.event
async def on_ready():
    log(f"{app.user} has connected to Discord!")
    log(f"{app.user.name}\n{app.user.id}\n=============")
    await app.change_presence(
        status=discord.Status.online, activity=discord.Game("서버 관리")
    )


@app.command(
    name="reload",
    help='Reload certain extension.\nUsing !reload {extension} to reload {extension}.\ntype nothing or "all" will reload all extensions',
    usage="!reload {extension}\n!reload all\n!reload",
)
async def reload_commands(ctx, extension=None):
    if extension is None or extension == "all":
        await ctx.send(":white_check_mark: Reloading all extensions...")
        for filename in os.listdir("Cogs"):
            if filename.endswith(".py"):
                app.unload_extension(f"Cogs.{filename[:-3]}")
                app.load_extension(f"Cogs.{filename[:-3]}")
                await ctx.send(":white_check_mark: Reload all extensions!")
    else:
        await ctx.send(f":white_check_mark: Reloading {extension}...")
        app.unload_extension(f"Cogs.{extension}")
        app.load_extension(f"Cogs.{extension}")
        await ctx.send(f":white_check_mark: Reload {extension}!")


@app.command(name="react", help="이모지 달기")
async def react_to_emoji(ctx, emoji):
    log(emoji)
    await ctx.message.add_reaction(emoji)


@app.command(name="stop", help="봇 멈추기")
async def stopBot(ctx):
    quit()


app.run(TOKEN)
