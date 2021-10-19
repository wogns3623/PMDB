from typing import Callable
import os

import yaml
import discord
from discord.ext import commands
from discord.app import InteractionContext

from Utils.logs import *
from config import ConfigManager, SOURCE_DIR

cm = ConfigManager()
config = cm.get_config("bot")


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


async def execute_load_like_command(
    ctx: InteractionContext, command: Callable, command_type: str, extension: str = None
):
    if extension is None or extension == "all":
        await ctx.respond(f"{command_type}ing all extensions...")
        loaded_extensions = []
        extension_names = get_cog_names()

        for filename in extension_names:
            try:
                command(f"Cogs.{filename}")
                loaded_extensions.append(filename)
                await ctx.interaction.edit_original_message(
                    content=f":white_check_mark: {command_type} {', '.join(loaded_extensions)}"
                )
            except discord.errors.ExtensionError as e:
                print(e)
                await ctx.channel.send(
                    f":negative_squared_cross_mark: Error when {command_type} extension {e}"
                )
        if len(loaded_extensions) == 0:
            await ctx.interaction.edit_original_message(
                content=f":negative_squared_cross_mark: {command_type} failed"
            )
        else:
            await ctx.interaction.edit_original_message(
                content=f":white_check_mark: {command_type} {', '.join(loaded_extensions)}!"
            )
    else:
        await ctx.respond(f"{command_type}ing {extension}...")
        try:
            command(f"Cogs.{extension}")
            await ctx.interaction.edit_original_message(
                content=f":white_check_mark: {command_type} {extension}!"
            )
        except discord.errors.ExtensionError as e:
            await ctx.interaction.edit_original_message(
                content=f":negative_squared_cross_mark: Error when {command_type} extension\n{e}"
            )


@bot.slash_command(
    guild_ids=config["guild_ids"],
    name="load",
    help='load certain extension.\nUsing /load {extension} to load {extension}.\ntype nothing or "all" will load all extensions',
    usage="/load {extension}\n/load all\n/load",
)
async def load_cog(ctx: InteractionContext, extension: str = None):
    await execute_load_like_command(ctx, bot.load_extension, "Load", extension)


@bot.slash_command(
    guild_ids=config["guild_ids"],
    name="unload",
    help='unload certain extension.\nUsing /unload {extension} to unload {extension}.\ntype nothing or "all" will unload all extensions',
    usage="/unload {extension}\n/unload all\n/unload",
)
async def unload_cog(ctx: InteractionContext, extension: str = None):
    await execute_load_like_command(ctx, bot.unload_extension, "Unload", extension)


@bot.slash_command(
    guild_ids=config["guild_ids"],
    name="reload",
    help='Reload certain extension.\nUsing /reload {extension} to reload {extension}.\ntype nothing or "all" will reload all extensions',
    usage="/reload {extension}\n/reload all\n/reload",
)
async def reload_cog(ctx: InteractionContext, extension: str = None):
    await execute_load_like_command(ctx, bot.reload_extension, "Reload", extension)


@bot.command(name="react", help="이모지 달기")
async def react_to_emoji(ctx: commands.Context, emoji: str):
    log(emoji)
    await ctx.message.add_reaction(emoji)


if __name__ == "__main__":
    bot.run(config["token"])
