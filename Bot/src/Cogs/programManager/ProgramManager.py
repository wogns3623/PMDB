import sys
import os
import errno

import asyncio
import discord
from discord.ext import commands

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Utils import log, errlog, SizedQueue

BUF_SIZE = 4096
LOG_SIZE = 100
INP_PIPE_DIR = "/tmp/smdb_ipipe"
OUT_PIPE_DIR = "/tmp/smdb_opipe"


class ProgramManager(commands.Cog):
    def __init__(self, app):
        self.app = app
        self.logCache = SizedQueue(LOG_SIZE)

        self.inputPipe = open(INP_PIPE_DIR, "w")
        self.outputPipe = open(OUT_PIPE_DIR, "r")

    def cog_unload(self):
        self.inputPipe.close()
        self.outputPipe.close()

    # TODO: complete function
    async def get_log(self):
        while res := await self.outputPipe.readline(BUF_SIZE):
            if self.logCache.full():
                self.logCache.pop()
            self.logCache.put(res)
        pass

    @commands.command(name="console", help="direct console input")
    async def console(self, ctx, *, command):
        log(f"Send command to server:\n{command}")
        if (n := self.inputPipe.write(f"/{command}")) != len(command) + 1:
            response = "서버에 명령을 전송하는 도중 오류가 발생했습니다."
            errlog(f"Fail to send command to server {n}, {len(command) + 1}")
        response = "서버에 명령을 전송했습니다."

        await ctx.send(response)

    @commands.command(
        name="log",
        help="direct console output\nRead N lines from console\n Default 1 line, Maximun 100 line",
    )
    async def send_log(self, ctx, *, n=1):
        for i in range(n):
            res = self.outputPipe.readline(BUF_SIZE)
            log(f"Send message to guild:\n{res}")
            await ctx.send(res)


def setup(app):
    try:
        os.mkfifo(INP_PIPE_DIR)
        os.mkfifo(OUT_PIPE_DIR)
    except OSError as oe:
        if oe.errno != errno.EEXIST:
            errlog(f"mkfifo fail, {oe.errno}")
            raise commands.ExtensionFailed(f"mkfifo fail because {oe.errno}")

    app.add_cog(ProgramManager(app))
    return