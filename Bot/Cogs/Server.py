import discord
import sys
from discord.ext import commands

class Server(commands.Cog):

  def __init__(self, app):
    self.app = app

  @commands.command(name='reboot', help='x분 후에 서버 재부팅')
  async def reboot_server(self, ctx, time: int):
    response = f"Server will reboot in {time} minute."
    await ctx.send(response)

  @commands.command(name='console', help='direct console input')
  async def console(self, ctx, *, command):
    print(f"/{command}", flush=True)
    response = f"서버에 명령을 전송했습니다."
    await ctx.send(response)


def setup(app):
  app.add_cog(Server(app))