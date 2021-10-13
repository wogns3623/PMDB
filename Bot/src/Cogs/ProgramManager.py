import sys
import os
import errno

import asyncio
import discord
from discord.ext import commands

from config import get_config
from Utils.logs import *
from Utils.SizedQueue import *

config = get_config("named_pipe")
BUF_SIZE = config["buffer_size"]
LOG_SIZE = config["log_size"]
INP_PIPE_DIR = os.path.join(config["path"], config["input_pipe_name"])
OUT_PIPE_DIR = os.path.join(config["path"], config["output_pipe_name"])


class ProgramManager:
    def __init__(self, log_size: int, input_pipe_dir: str, output_pipe_dir: str):
        self.log_cache = SizedQueue(log_size)
        self.open_pipe(input_pipe_dir, output_pipe_dir)
        self.log_regex_list = []

    def open_pipe(self, input_pipe_dir: str, output_pipe_dir: str):
        # somehow it work like os.O_RDWR mode
        self.input_pipe = open(input_pipe_dir, "w+b", buffering=0)
        self.output_pipe = open(output_pipe_dir, "r+b", buffering=0)

    def close_pipe(self):
        self.input_pipe.close()
        self.output_pipe.close()

    def write_command(self, command: str) -> bool:
        log(f"Send command to server:\n{command}, {len(command)}")
        n = self.input_pipe.write(command.encode())
        if n != len(command):
            errlog(f"Fail to send command to server {n}, {len(command)}")
            return False
        return True

    # TODO: complete function
    def read_log(self):
        """
        read log from attacher periodically
        """
        pass
        # while res := self.output_pipe.readline(BUF_SIZE).decode("utf-8"):
        #     if self.log_cache.full():
        #         self.log_cache.pop()
        #     self.log_cache.put(res)

    def load_regex_list(self, regex_table: str) -> bool:
        """load regex to evaluate important log

        Args:
            regex_table (str): regex list

        Returns:
            bool: if load success, return true
        """
        pass


class ProgramManagerCog(ProgramManager, commands.Cog):
    def __init__(
        self,
        bot: commands.Bot,
        log_size: int,
        input_pipe_dir: str,
        output_pipe_dir: str,
    ):
        self.bot = bot
        ProgramManager.__init__(log_size, input_pipe_dir, output_pipe_dir)

    def cog_unload(self):
        self.close_pipe()

    @commands.command(name="console", help="direct console input")
    async def console(self, ctx: commands.Context, *, command: str):
        if not self.write_command(command):
            response = "서버에 명령을 전송하는 도중 오류가 발생했습니다."
        else:
            response = "서버에 명령을 전송했습니다."

        await ctx.send(response)

    @commands.command(
        name="log",
        help=f"direct console output\nRead N lines from console\n Default 1 line, Maximun {LOG_SIZE} line",
    )
    async def send_log(self, ctx: commands.Context, *, n: int = 1):
        # TODO: self.log_cache를 쓰도록 변경하기
        for i in range(n):
            res = self.output_pipe.readline(BUF_SIZE).decode("utf-8")
            log(f"Send message to guild:\n{res}")
            await ctx.send(res)


def setup(bot: commands.Bot):
    try:
        os.mkfifo(INP_PIPE_DIR)
    except OSError as oe:
        if oe.errno != errno.EEXIST:
            errlog(f"mkfifo fail, {oe.errno}")
            raise commands.ExtensionFailed(f"mkfifo fail because {oe.errno}")
    try:
        os.mkfifo(OUT_PIPE_DIR)
    except OSError as oe:
        if oe.errno != errno.EEXIST:
            errlog(f"mkfifo fail, {oe.errno}")
            raise commands.ExtensionFailed(f"mkfifo fail because {oe.errno}")

    bot.add_cog(ProgramManagerCog(bot, LOG_SIZE, INP_PIPE_DIR, OUT_PIPE_DIR))
    return
