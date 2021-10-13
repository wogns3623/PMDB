import os
import yaml
import discord
from discord.ext import commands

from Utils.logs import *
from Utils.config import get_config


PROJECT_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
SOURCE_DIR = os.path.join(PROJECT_DIR, "src")
os.environ["PROJECT_DIR"] = PROJECT_DIR
os.environ["SOURCE_DIR"] = SOURCE_DIR

config = get_config("bot")


def get_cog_names():
    return [
        c[:-3]
        for c in os.listdir(os.path.join(SOURCE_DIR, "Cogs"))
        if c.endswith(".py")
    ]


bot = commands.Bot(command_prefix="!")

for filename in get_cog_names():
    bot.load_extension(f"Cogs.{filename}")


@bot.event
async def on_ready():
    log(f"{bot.user} has connected to Discord!")
    log(
        f"{bot.user.name}, {bot.user.id}\n================================================"
    )
    await bot.change_presence(
        status=discord.Status.online, activity=discord.Game("dev")
    )


@bot.slash_command(
    guild_ids=config["guild_ids"],
    name="load",
    help='load certain extension.\nUsing !load {extension} to load {extension}.\ntype nothing or "all" will load all extensions',
    usage="!load {extension}\n!load all\n!load",
)
async def load_commands(ctx: commands.Context, extension: str = None):
    if extension is None or extension == "all":
        await ctx.send("loading all extensions...")
        for filename in get_cog_names():
            bot.load_extension(f"Cogs.{filename}")
        await ctx.send(":white_check_mark: load all extensions!")
    else:
        await ctx.send(f"loading {extension}...")
        bot.load_extension(f"Cogs.{extension}")
        await ctx.send(f":white_check_mark: load {extension}!")


@bot.slash_command(
    guild_ids=config["guild_ids"],
    name="unload",
    help='unload certain extension.\nUsing !unload {extension} to unload {extension}.\ntype nothing or "all" will unload all extensions',
    usage="!unload {extension}\n!unload all\n!unload",
)
async def unload_commands(ctx: commands.Context, extension: str = None):
    if extension is None or extension == "all":
        await ctx.send("Unloading all extensions...")
        for filename in get_cog_names():
            bot.unload_extension(f"Cogs.{filename}")
        await ctx.send(":white_check_mark: Unload all extensions!")
    else:
        await ctx.send(f"Unloading {extension}...")
        bot.unload_extension(f"Cogs.{extension}")
        await ctx.send(f":white_check_mark: Unload {extension}!")


@bot.slash_command(
    guild_ids=config["guild_ids"],
    name="reload",
    help='Reload certain extension.\nUsing !reload {extension} to reload {extension}.\ntype nothing or "all" will reload all extensions',
    usage="!reload {extension}\n!reload all\n!reload",
)
async def reload_commands(ctx: commands.Context, extension: str = None):
    if extension is None or extension == "all":
        await ctx.send("Reloading all extensions...")
        for filename in get_cog_names():
            bot.reload_extension(f"Cogs.{filename}")
        await ctx.send(":white_check_mark: Reload all extensions!")
    else:
        await ctx.send(f"Reloading {extension}...")
        bot.reload_extension(f"Cogs.{extension}")
        await ctx.send(f":white_check_mark: Reload {extension}!")


@bot.command(name="react", help="이모지 달기")
async def react_to_emoji(ctx: commands.Context, emoji: str):
    log(emoji)
    await ctx.message.add_reaction(emoji)


if __name__ == "__main__":
    bot.run(config["token"])
