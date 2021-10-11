import sys
import os
import errno

import asyncio
import discord
from discord.ext import commands

from Utils.Logs import *
from Utils.SizedQueue import *

BUF_SIZE = 4096
LOG_SIZE = 100
INP_PIPE_DIR = "/tmp/smdb_ipipe"
OUT_PIPE_DIR = "/tmp/smdb_opipe"


class ProgramManager(commands.Cog):
    def __init__(self, bot: commands.Bot, inputPipeDir, outputPipeDir):
        self.bot = bot
        self.logCache = SizedQueue(LOG_SIZE)

        self.inputPipe = os.open(inputPipeDir, os.O_RDWR)
        self.outputPipe = os.open(outputPipeDir, os.O_RDWR)

    def cog_unload(self):
        self.inputPipe.close()
        self.outputPipe.close()

    # TODO: complete function
    async def read_log(self):
        while res := await self.outputPipe.readline(BUF_SIZE):
            if self.logCache.full():
                self.logCache.pop()
            self.logCache.put(res)

    @commands.command(name="console", help="direct console input")
    async def write_command(self, ctx: commands.Context, *, command: str):
        log(f"Send command to server:\n{command}")
        if (n := self.inputPipe.write(f"/{command}")) != len(command) + 1:
            response = "서버에 명령을 전송하는 도중 오류가 발생했습니다."
            errlog(f"Fail to send command to server {n}, {len(command) + 1}")
        response = "서버에 명령을 전송했습니다."

        await ctx.send(response)

    @commands.command(
        name="log",
        help=f"direct console output\nRead N lines from console\n Default 1 line, Maximun {LOG_SIZE} line",
    )
    async def send_log(self, ctx: commands.Context, *, n: int = 1):
        for i in range(n):
            res = self.outputPipe.readline(BUF_SIZE)
            log(f"Send message to guild:\n{res}")
            await ctx.send(res)


def setup(bot: commands.Bot):
    try:
        os.mkfifo(INP_PIPE_DIR)
        os.mkfifo(OUT_PIPE_DIR)
    except OSError as oe:
        if oe.errno != errno.EEXIST:
            errlog(f"mkfifo fail, {oe.errno}")
            raise commands.ExtensionFailed(f"mkfifo fail because {oe.errno}")

    bot.add_cog(ProgramManager(bot, INP_PIPE_DIR, OUT_PIPE_DIR))
    return
