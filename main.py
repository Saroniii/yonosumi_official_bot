# coding: UTF-8
import discord
from discord.ext import commands
import os

TOKEN = os.environ['TOKEN']

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.loaded = False
        self.ready_check = False
        self.notema = None
        self.waf = None
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print("------")
        print(f"導入サーバー数：{len(self.guilds)}")
        print(f"合計ユーザー数：{len({a.id for a in self.users if not a.bot})}")
        print(f"合計ボット数：{len({a.id for a in self.users if a.bot})}")
        print('------')
        reloaded = discord.Game("起動中です・・・")
        await bot.change_presence(status=discord.Status.idle, activity=reloaded)
        print(f'import')
        if not self.loaded:
            import pathlib
            cur = pathlib.Path('.')
            for p in cur.glob('module/*.py'):
                try:
                    print(f'module.{p.stem}', end="　")
                    self.load_extension(f'module.{p.stem}')
                    print(f'success')
                except commands.errors.NoEntryPointError:
                    print(f'module.{p.stem}')
            else:
                self.loaded = True
        print('------')
        membercount = len(bot.users)
        game = discord.Game(f"世の隅の{membercount}人と一緒にいるよ！")
        await bot.change_presence(status=discord.Status.online,activity=game)

bot = MyBot(command_prefix=["y/","y1"])

bot.run(TOKEN)
