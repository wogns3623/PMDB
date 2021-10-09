import sys
import os
import asyncio
import pip

import discord
from discord.ext import commands
from dotenv import load_dotenv


from Utils.Logs import *

load_dotenv("../")
TOKEN = os.getenv("DISCORD_TOKEN")

app = commands.Bot(command_prefix="!")

for filename in os.listdir("Cogs"):
    if filename.endswith(".py"):
        app.load_extension(f"Cogs.{filename[:-3]}")


@app.event
async def on_ready():
    log(f"{app.user} has connected to Discord!")
    log(f"{app.user.name}\n{app.user.id}\n=============")
    await app.change_presence(
        status=discord.Status.online, activity=discord.Game("dev")
    )


@app.command(
    name="load",
    help='load certain extension.\nUsing !load {extension} to load {extension}.\ntype nothing or "all" will load all extensions',
    usage="!load {extension}\n!load all\n!load",
)
async def load_commands(ctx: commands.Context, extension: str = None):
    if extension is None or extension == "all":
        await ctx.send("loading all extensions...")
        for filename in os.listdir("Cogs"):
            if filename.endswith(".py"):
                app.load_extension(f"Cogs.{filename[:-3]}")
        await ctx.send(":white_check_mark: load all extensions!")
    else:
        await ctx.send(f"loading {extension}...")
        app.load_extension(f"Cogs.{extension}")
        await ctx.send(f":white_check_mark: load {extension}!")


@app.command(
    name="unload",
    help='unload certain extension.\nUsing !unload {extension} to unload {extension}.\ntype nothing or "all" will unload all extensions',
    usage="!unload {extension}\n!unload all\n!unload",
)
async def unload_commands(ctx: commands.Context, extension: str = None):
    if extension is None or extension == "all":
        await ctx.send("Unloading all extensions...")
        for filename in os.listdir("Cogs"):
            if filename.endswith(".py"):
                app.unload_extension(f"Cogs.{filename[:-3]}")
        await ctx.send(":white_check_mark: Unload all extensions!")
    else:
        await ctx.send(f"Unloading {extension}...")
        app.unload_extension(f"Cogs.{extension}")
        await ctx.send(f":white_check_mark: Unload {extension}!")


@app.command(
    name="reload",
    help='Reload certain extension.\nUsing !reload {extension} to reload {extension}.\ntype nothing or "all" will reload all extensions',
    usage="!reload {extension}\n!reload all\n!reload",
)
async def reload_commands(ctx: commands.Context, extension: str = None):
    if extension is None or extension == "all":
        await ctx.send("Reloading all extensions...")
        for filename in os.listdir("Cogs"):
            if filename.endswith(".py"):
                app.reload_extension(f"Cogs.{filename[:-3]}")
        await ctx.send(":white_check_mark: Reload all extensions!")
    else:
        await ctx.send(f"Reloading {extension}...")
        app.reload_extension(f"Cogs.{extension}")
        await ctx.send(f":white_check_mark: Reload {extension}!")


@app.command(name="react", help="이모지 달기")
async def react_to_emoji(ctx: commands.Context, emoji: str):
    log(emoji)
    await ctx.message.add_reaction(emoji)


app.run(TOKEN)
