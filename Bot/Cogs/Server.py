import discord
import os
import errno
from discord.ext import commands

INP_PIPE_DIR = "/home/smdb/ipipe"
OUT_PIPE_DIR = "/home/smdb/opipe"

BUF_SIZE = 1024


class Server(commands.Cog):
  def __init__(self, app):
    self.app = app

  @commands.command(name="reboot", help="x분 후에 서버 재부팅")
  async def reboot_server(self, ctx, time: int):
    response = f"Server will reboot in {time} minute."
    await ctx.send(response)

  @commands.command(name="console", help="direct console input")
  async def console(self, ctx, *, command):
    if not os.path.exists(INP_PIPE_DIR):
      try:
        os.mkfifo(INP_PIPE_DIR)
      except OSError as oe: 
        if oe.errno != errno.EEXIST:
          print(f"[Bot/Error] mkfifo fail, errno is {oe.errno}")
          await ctx.send("오류가 발생했습니다")
          return

    with open(INP_PIPE_DIR, "w") as fifo:
      if fifo.write(f"/{command}") != len(command) + 1:
        response = "서버에 명령을 전송하는 도중 오류가 발생했습니다."
      response = "서버에 명령을 전송했습니다."

      await ctx.send(response)

  @commands.command(name="log", help="direct console output\nRead N lines from console\n Default 1 line")
  async def console(self, ctx, *, n=1):
    if not os.path.exists(OUT_PIPE_DIR):
      try:
        os.mkfifo(OUT_PIPE_DIR)
      except OSError as oe: 
        if oe.errno != errno.EEXIST:
          print(f"[Bot/Error] mkfifo fail, errno is {oe.errno}")
          await ctx.send("오류가 발생했습니다")
          return

    with open(OUT_PIPE_DIR, "r") as fifo:
      for i in range(n):
        res = fifo.readline(BUF_SIZE)
        await ctx.send(res)


def setup(app):
  app.add_cog(Server(app))
