import sys
import os
import errno
from contextlib import suppress
import asyncio
from typing import Optional, IO, List

import yaml
from discord.errors import ExtensionFailed
from discord.ext import commands

from discord.abc import Messageable

from config import ConfigManager, PROJECT_DIR
from Utils.logs import *
from Utils.SizedQueue import *
from Utils.LogClassifier import *

cm = ConfigManager()
config = cm.config["named_pipe"]

BUF_SIZE = config["buffer_size"]
LOG_SIZE = config["log_size"]
INP_PIPE_DIR = os.path.join(config["path"], config["input_pipe_name"])
OUT_PIPE_DIR = os.path.join(config["path"], config["output_pipe_name"])


class LogWorker:
    def __init__(
        self,
        log_size: int,
        log_channels: Optional[List[Messageable]] = None,
        readable_stream: Optional[IO] = None,
    ):
        self.log_cache = SizedQueue(log_size)
        self.classifier: LogClassifier = None
        self.channels = log_channels
        self.stream = readable_stream
        self._is_started = False
        self._task = None

    async def start(self):
        if not (self._is_started and self.channels is None and self.stream is None):
            self._is_started = True
            self._task = asyncio.ensure_future(self._run())

    async def stop(self):
        if self._is_started:
            self._is_started = False
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task

    async def _run(self):
        while res := self.stream.readline(BUF_SIZE).decode("utf-8"):
            log_type = self.classifier.classify(res)
            if not log_type is LogType.IGNORE:
                if self.log_cache.full():
                    self.log_cache.pop()
                self.log_cache.put(res)

            if log_type is LogType.IMPORTANT:
                for channel in self.channels:
                    await channel.send(log)


class ProgramManager:
    def __init__(self, log_size: int, input_pipe_dir: str, output_pipe_dir: str):
        self.open_pipe(input_pipe_dir, output_pipe_dir)
        self.log_channels: List[int] = cm.config["bot"]["log_channel"]
        self.worker = LogWorker(log_size)

    def open_pipe(self, input_pipe_dir: str, output_pipe_dir: str):
        # somehow it work like os.O_RDWR mode
        self.input_pipe = open(input_pipe_dir, "w+b", buffering=0)
        self.output_pipe = open(output_pipe_dir, "r+b", buffering=0)

    def close_pipe(self):
        self.input_pipe.close()
        self.output_pipe.close()

    def set_classifier(self, classifier_name: str) -> bool:
        """Set classifier to evaluate important log

        Args:
            classifier_name (str): classifier name

        Returns:
            bool: if load success, return true
        """
        path = os.path.join(PROJECT_DIR, f"regex/{classifier_name}.yml")
        self.classifier = LogClassifier(path)

    def write_command(self, command: str) -> bool:
        """Send command to server

        Args:
            command (str): command to send

        Returns:
            bool: if send success, return true
        """
        log(f"Send command to server:\n{command}, {len(command)}")
        n = self.input_pipe.write(command.encode())
        if n != len(command):
            errlog(f"Fail to send command to server {n}, {len(command)}")
            return False
        return True

    # TODO: complete function
    def read_log(self):
        """Read log from attacher periodically"""
        pass
        # while res := self.output_pipe.readline(BUF_SIZE).decode("utf-8"):
        #     if self.log_cache.full():
        #         self.log_cache.pop()
        #     self.log_cache.put(res)


class ProgramManagerCog(ProgramManager, commands.Cog):
    def __init__(
        self,
        bot: commands.Bot,
        log_size: int,
        input_pipe_dir: str,
        output_pipe_dir: str,
    ):
        self.bot = bot
        ProgramManager.__init__(self, log_size, input_pipe_dir, output_pipe_dir)

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
        help=f"Direct console output\nRead N lines from console\n Default 1 line, Maximun {LOG_SIZE} line",
    )
    async def send_log(self, ctx: commands.Context, *, n: int = 1):
        # TODO: self.log_cache를 쓰도록 변경하기
        for i in range(n):
            res = self.output_pipe.readline(BUF_SIZE).decode("utf-8")
            log(f"Send message to guild:\n{res}")
            await ctx.send(res)

    @commands.command(
        name="addLogChannel",
        help=f"Add this channel to log sended channel list",
    )
    async def add_log_channel(self, ctx: commands.Context, channel_id: int = None):
        if channel_id is None:
            channel_id = ctx.message.channel.id
        if not channel_id in self.log_channels:
            self.log_channels.append(channel_id)
            cm.save_config()
            await ctx.send(f"Add this channel to channel list, id: {channel_id}")
        else:
            await ctx.send(f"This channel has already been added")

    @commands.command(
        name="delLogChannel",
        help=f"Delete this channel in log sended channel list",
    )
    async def del_log_channel(self, ctx: commands.Context, channel_id: int = None):
        if channel_id is None:
            channel_id = ctx.message.channel.id
        if channel_id in self.log_channels:
            self.log_channels.remove(channel_id)
            cm.save_config()
            await ctx.send(f"Delete this channel in channel list, id: {channel_id}")
        else:
            await ctx.send(f"This channel has never been added")

    @commands.command(
        name="logChannelList",
        help=f"Show log sended channel list",
    )
    async def show_log_channel(self, ctx: commands.Context):
        await ctx.send(f"Channel list is {', '.join(self.log_channels)}")

    @commands.command(
        name="setClassifier",
        help=f"Set the classifier to classify log messages",
    )
    async def set_classifier_type(
        self,
        ctx: commands.Context,
        classifier_name: str,
    ):
        self.set_classifier(classifier_name)
        await ctx.send(f"Set classifier to {classifier_name}")


def setup(bot: commands.Bot):
    try:
        os.mkfifo(INP_PIPE_DIR)
    except OSError as oe:
        if oe.errno != errno.EEXIST:
            errlog(f"mkfifo fail, {oe.errno}")
            raise ExtensionFailed(f"mkfifo fail because {oe.errno}")
    try:
        os.mkfifo(OUT_PIPE_DIR)
    except OSError as oe:
        if oe.errno != errno.EEXIST:
            errlog(f"mkfifo fail, {oe.errno}")
            raise ExtensionFailed(f"mkfifo fail because {oe.errno}")

    bot.add_cog(ProgramManagerCog(bot, LOG_SIZE, INP_PIPE_DIR, OUT_PIPE_DIR))
    return
