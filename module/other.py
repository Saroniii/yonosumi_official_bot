import discord
from discord.ext import commands, tasks
import traceback
from googletrans import Translator
import os
import sqlite3
import requests
import time


class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error,(commands.CommandNotFound, commands.CommandOnCooldown)):
            return
        await ctx.send(error)
        s_error = traceback.format_exception(type(error), error, error.__traceback__)
        for i in range(len(s_error)):
             while len("".join(s_error[i:i+2])) < 2000-15 and len("".join(s_error[i+1:])) != 0:
                 s_error[i:i+2]=["".join(s_error[i:i+2])]
        webhook = await self.bot.fetch_webhook(676072213044133908)
        for i in range(0,len(s_error),3):
            await webhook.send(embeds=[discord.Embed(description=f"```py\n{y}```").set_footer(text=f"{i+x+1}/{len(s_error)}") for x,y in enumerate(s_error[i:i+3])])

    @commands.command(aliases=["req"])
    async def request(self, ctx, title, *, arg):
        embed = discord.Embed(title=f"{ctx.author}({ctx.author.id})",description="**リクエスト**")
        embed.add_field(name=f"{title}",value=f"{arg}")
        reqch = self.bot.get_channel(672801665413546004)
        await reqch.send(embed=embed)
        await ctx.send(f"{ctx.author.mention}->以下の内容で開発者に通知されました。要望が採用されたときや、細かい部分について確認事項がある場合、``凜花 -りんか-``または開発者からDMが届く場合があります。",embed=embed)

    @commands.command(aliases=["directmessage","pm"])
    async def dm(self, ctx, user :discord.User, *, arg):
        if [i for i in ctx.bot.get_guild(642358764145737747).get_member(ctx.author.id).roles if i.id == 643755423035293696]:
            await user.send(f"**凜花 -りんか- スタッフの``{ctx.author}``からDMが届きました。**\n```{arg}```")
            await ctx.send(f"{ctx.author.mention}->以下の内容で``{user}``にDMを送信しました。\n```{arg}```")

    @commands.command(aliases=["trans"])
    async def translate(self, ctx, lang, *, arg):
        waiting = await ctx.send(f"{ctx.author.mention}->翻訳しています...")
        trans = Translator()
        try:
            data = trans.translate(arg, dest=lang)
        except:
            await waiting.edit(content=f"{ctx.author.mention}->正常に翻訳が実行されませんでした！以下の原因の可能性があります:\n○引数``lang``を指定していない\n○引数``lang``の型が不正(日本語の場合、``ja``,英語の場合、``en``と入力してください。\n詳しくはこちら→http://bit.ly/39hhCQ1)")
            return
        embed = discord.Embed(title=f"翻訳が完了しました！",description=f"翻訳結果")
        embed.add_field(name="翻訳前:",value=f"``{arg}``")
        embed.add_field(name="翻訳後:",value=f"``{data.text}``")
        embed.set_footer(text=f"原文の言語:自動検出 / 翻訳後の言語:{lang}")
        await waiting.edit(content=f"{ctx.author.mention}->",embed=embed)

    @commands.command()
    async def restart(self, ctx):
        if [i for i in ctx.bot.get_guild(642358764145737747).get_member(ctx.author.id).roles if i.id == 643755423035293696]:
            await ctx.send(f"{ctx.author.mention}->再起動中...")
            restart = discord.Game("再起動中...")
            await self.bot.change_presence(status=discord.Status.dnd, activity=restart)
            await self.bot.start("NjcwMTI2NzEwMzM5MTQxNjMz.Xip2Ng.rSnimDzuDhIvitf8VHUUjr2hkDg")


    @commands.command()
    async def genbotinvite(self, ctx, user :discord.User):
        bot = False
        if user.bot:
            bot = True
        if bot == False:
            await ctx.send(f"{ctx.author.mention}->``{user.name}``はBotではありません！")
        else:
            await ctx.send(f"{ctx.author.mention}->``{user.name}``の招待リンクはこちら\nhttps://discordapp.com/oauth2/authorize?client_id={str(user.id)}&permissions=2146958847&scope=bot")

    @commands.command()
    async def invite(self, ctx):
        await ctx.send(f"{ctx.author.mention}->``凜花 -りんか-``の招待リンクです。\nhttps://discordapp.com/oauth2/authorize?client_id=670126710339141633&permissions=2146958847&scope=bot")

    @commands.command()
    async def featured(self, ctx, arg =None):
        if not arg:
            embed = discord.Embed(title="開発者のおすすめ",description="``凜花 -りんか-``運営陣のおすすめ")
            embed.add_field(name="結月 -ゆづき-",value="オールマイティーなBOT。使い勝手がよく、安定性もある。\n詳しい情報は``r/featured yudzuki``で確認できます。")
            embed.add_field(name="TAO",value="日本のDiscordユーザーの多くが知っているRPG系Bot。最近は多くの新機能が追加され、更に面白くなりました。\n詳しい情報は``r/featured TAO``で確認できます。")
            await ctx.send(f"{ctx.author.mention}->",embed=embed)
            return
        if arg == "yudzuki":
            embed = discord.Embed(title="結月 -ゆづき-",description="オールマイティーで使い勝手がいい高機能BOTです。\nまた純日本製で安心です。")
            embed.add_field(name="招待リンク",value="https://api.aoichaan0513.jp/invite/stable")
        elif arg == "TAO":
            embed = discord.Embed(title="TAO",description="日本のDiscord界隈を牽引している最も有名なRPG系Botです。\n結月と同じく、純日本製のBotです！")
            embed.add_field(name="招待リンク",value="[Botの招待](https://discordapp.com/oauth2/authorize?client_id=526620171658330112&permissions=2146958847&scope=bot)\n[TAO公式サーバー](https://discord.gg/7HGhtjS)")
        else:
            await ctx.send(f"{ctx.author.mention}->一致するおすすめ情報が見つかりませんでした！")
            return
        await ctx.send(f"{ctx.author.mention}->",embed=embed)

    @commands.command()
    async def support(self, ctx):
        await ctx.send(f"{ctx.author.mention}->サポートが必要ですか？凜花 -りんか- の公式サーバーに参加することで、サポート/-*を受けることができます！\nhttps://discord.gg/wcgfneh")

    @commands.command()
    async def leave(self, ctx, guild :discord.Guild):
        if [i for i in ctx.bot.get_guild(642358764145737747).get_member(ctx.author.id).roles if i.id == 643755423035293696]:
            await guild.leave()
            embed = discord.Embed(title="サーバーから抜けたよ～",description=f"``{guild.name}({guild.id})``から退出しました！")
            memberscount = len(guild.members)
            textcount = len(guild.text_channels)
            voicecount = len(guild.voice_channels)
            total = textcount + voicecount
            embed.add_field(name=f"サーバーの概要",value=f"``サーバーオーナー:{guild.owner}({guild.owner.id})``\n\n```メンバー数:{memberscount}\nテキストチャンネル:{textcount}\nボイスチャンネル:{voicecount}\n合計チャンネル数:{total}\nサーバー作成日:{guild.created_at}```")
            await ctx.send(f"{ctx.author.mention}->",embed=embed)
        

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def transcript(self, ctx, limit =None):
        waiting = await ctx.send(f"{ctx.author.mention}->チャットログを出力しています...")
        if not limit:
            limit = None  
        else:
            limit = int(limit)
        msg_count = 0
        log = f"#{ctx.channel.name}({ctx.channel.id}) logs\n"
        async for message in ctx.channel.history(limit=limit, oldest_first=True):
            msg_count = msg_count + 1
            log += f"[{msg_count}]{message.author.name}({message.author.id}):{message.content}\n"
        log += f"\n\n[総メッセージ数:{msg_count}]\n[コマンド実行者:{ctx.author}]\n\n\nこれは、凜花 -りんか-によって自動生成された#{ctx.channel.name}のチャットログです。\nこのチャットログを悪用、または意図的な改変をすることを固く禁じます。\nまた、この自動生成されたチャットログによって生じた損害に対して、凜花 -りんか- 運営チームは一切の責任を負いません。\n\n\n© 2020 Saronii & 凜花 -りんか- Operation Team. All Rights Reserved."
        path = f"{ctx.channel.name}.txt"
        with open(path,mode="w",encoding="UTF-8") as f:
            f.write(log)
        await waiting.delete()
        await ctx.send(f"{ctx.author.mention}->{ctx.channel.mention}のチャットログの出力が完了しました。",file=discord.File(f"{ctx.channel.name}.txt"))

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user :discord.User, *, reason =None):
        reasontemp = f"{ctx.author}:"
        if not reason:
            reason = "理由が未入力です"
        reasontemp += reason
        await ctx.guild.ban(user,reason=reasontemp)
        embed = discord.Embed(title="BAN成功",description=f"``BAN理由``\n```{reason}```")
        await ctx.send(f"{ctx.author.mention}->{user}をBANしました。",embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, userid, *, reason =None):
        if not reason:
            reason = "理由が未入力です"
        try:
            banuser = await ctx.guild.fetch_ban(discord.Object(userid))
            await ctx.guild.unban(banuser.user,reason=f"{ctx.author}:{reason}")
            await ctx.send(f"{ctx.author.mention}->``{banuser.user.name}``のBANを解除しました。\n``解除理由:{banuser.reason}``")
        except Exception as e:
            banuser = self.bot.get_user(userid)
            banuser = (banuser.user.name if banuser else f"<@{userid}>")
            await ctx.send(f"{ctx.author.mention}->以下のどれかの理由で、``{banuser}``のBANが解除できませんでした。\n{banuser}がBANされていない\n凜花 -りんか-にBAN権限が付与されていない")
            return

    @commands.command()
    async def ping(self, ctx):
        before = time.monotonic()
        message = await ctx.send(f"{ctx.author.mention}->計測中です...")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"{ctx.author.mention}->Pingは``{int(ping)}ms``です！")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user :discord.User, *, reason =None):
        reasontemp = f"{ctx.author}:"
        if not reason:
            reason = "理由が未入力です"
        reasontemp += reason
        await ctx.guild.kick(user,reason=reasontemp)
        embed = discord.Embed(title="キック成功",description=f"``キック理由``\n```{reason}```")
        await ctx.send(f"{ctx.author.mention}->{user}をキックしました。",embed=embed)

    @commands.command(aliases=["コロナ","corona"])
    async def covid19(self, ctx, country=None):
        url = 'https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/2/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*'
        r = requests.get(url)
        a=r.json()["features"]
        if country:
            translate = {"日本":"Japan","アメリカ":"US","イタリア":"Italy","中国":"China","フランス":"France",
                         "スペイン":"Spain","ドイツ":"Germany","イラン":"Iran"}
            for i,j in translate.items():
                country=country.replace(i,j)
            country=[country]
        else:country=["Japan", "US", "Italy", "China", "Iran", "Korea, South", "France", "Spain", "Germany", "Switzerland"]
        table={}
        embed=discord.Embed(title="特設コマンド(COVID-19)", url="https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6")
        for x in country:
            table.update({x:{}})
            for y in ["Confirmed", "Deaths", "Recovered", "Active"]:
                table[x][y[0]]=([i["attributes"][y] for i in a if i["attributes"]["Country_Region"]==x] or ["N/A"])[0]
            embed.add_field(name=f"**{x}**", value="感染：`{C:>6}`人　死亡：`{D:>5}`人　回復：`{R:>5}`人　現在：`{A:>5}`人".format(**table[x]), inline=False)
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Cog(bot))
