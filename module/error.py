import re
import traceback

import discord
from discord.ext import commands


class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, (commands.CommandNotFound, commands.CommandOnCooldown)):
            return
        waiting = await ctx.send(f"{ctx.author.mention}->エラーが発生しました...原因を解析しています...")
        if isinstance(error, commands.MissingRequiredArgument):
            arg = str(error.param)
            varname = {
                'object_gos': 'サーバーオブジェクトもしくは文字列',
                'database': '操作したいデータベース',
                'object_mor': '検索したい役職もしくはメンバー',
                'announcedata': 'アナウンスする文章',
                'noteuser': 'Noteのユーザー名',
                'channelname': 'チャンネル名',
                'channel': 'チャンネル',
                'sqlcmd': 'SQLステートメント',
                'roll_data': '抽選するもの',
                '_triger': '絵文字の追加名',
                'code': 'コード',
                'userid': 'ユーザーID',
                'reason': '理由',
                'target': '処置を行う相手',
                'playername': '検索するプレイヤー',
                'artist': '歌手名',
                'song': '曲名',
                'text': '打ち込みたい文章',
                'math_value': '計算させたい式',
                'ip': '検索したいサーバーのIPアドレス',
                'settype': 'タイプ指定',
                'triger': 'メモを呼び出すためのトリガー',
                'role': '役職',
                'onlinetype': 'オンライン表示',
                'playing': 'アクティビティー',
                'check': 'タイプ指定',
                'tododata': 'ToDoの文章',
                'user': 'ユーザー',
                'invite_user': '招待したいユーザー',
                'sentence': '文章',
                'title': 'タイトル',
                'bantype': 'BANのタイプ',
                'badge_type': 'バッジのタイプ',
                'get_type': '付与するタイプ',
                'guild': 'サーバー名',
                'data_id': 'ID',
            }
            arg = re.split('[.,:]', arg)
            embed = discord.Embed(
                title="引数不足です！", description=f"引数``{arg[0]}``が足りていません！", color=discord.Colour.from_rgb(255, 0, 0))
            try:
                desc = varname[arg[0]]
                embed.add_field(name=f"💡もしかしたら...",
                                value=f"``{desc}``が不足していませんか？")
            except:
                pass
            await waiting.edit(content=f"{ctx.author.mention}->", embed=embed)
            return
        elif isinstance(error, commands.BadArgument):
            await ctx.send(dir(error))
            try:
                await ctx.send(dir(error.__context__))
            except:
                pass
            target_dir = {
                'int': '数値',
                'Member': 'メンバー',
                'user': 'ユーザー',
                'Guild': 'サーバー',
                'Emoji': '絵文字'
            }
            target = str(error.args).split()[2].replace('"', '')
            embed = discord.Embed(
                title=f'取得に失敗しました！', description=f"引数の``{target}``を取得できませんでした！", color=discord.Colour.from_rgb(255, 0, 0))
            try:
                desc = target_dir[target]
                embed.add_field(
                    name="💡もしかして...", value=f"引数の``{desc}``は実際に存在していますか？\n実際に存在しているオブジェクトでも、凜花が認識していないオブジェクトは取得できない場合があります。")
            except:
                pass
            await waiting.edit(content=f"{ctx.author.mention}->", embed=embed)
            return
        elif isinstance(error, (commands.MissingPermissions, commands.BotMissingPermissions)):
            perm = error.missing_perms[0]
            try:
                perm = self.bot.permissions_dir[perm]
            except:
                pass
            if isinstance(error, commands.MissingPermissions):
                await waiting.edit(content=f"{ctx.author.mention}->", embed=discord.Embed(title=f"権限不足です！", description=f"このコマンドを実行するには、``{perm}``が必要です！", color=discord.Colour.from_rgb(255, 0, 0)))
            else:
                await waiting.edit(content=f"{ctx.author.mention}->", embed=discord.Embed(title=f"Botの権限不足です！", description=f"このコマンドを実行するには、Botに``{perm}``を付与する必要があります！", color=discord.Colour.from_rgb(255, 0, 0)))
            return
        try:
            await waiting.edit(content=f"{ctx.author.mention}->{error}")
        except:
            await waiting.edit(content=f"{ctx.author.mention}->エラーが解析できませんでした！")
        s_error = traceback.format_exception(
            type(error), error, error.__traceback__)
        print(s_error)
        for i in range(len(s_error)):
            while len("".join(s_error[i:i+2])) < 2000-15 and len("".join(s_error[i+1:])) != 0:
                s_error[i:i+2] = ["".join(s_error[i:i+2])]
        webhook = await self.bot.fetch_webhook(800731709104324658)
        for i in range(0, len(s_error), 3):
            await webhook.send(embeds=[discord.Embed(description=f"```py\n{y}```").set_footer(text=f"{i+x+1}/{len(s_error)}") for x, y in enumerate(s_error[i:i+3])])


def setup(bot):
    bot.add_cog(Cog(bot))
