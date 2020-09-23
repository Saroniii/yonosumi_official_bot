import discord
from discord.ext import commands,tasks
status_flag = False

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.changestatus.start()


    @commands.command()
    async def setstatus(self, ctx, onlinetype, *, playing =None):
        if [i for i in ctx.bot.get_guild(642358764145737747).get_member(ctx.author.id).roles if i.id == 643755423035293696]:
            playing = discord.Game(playing)
            global status_flag 
            if onlinetype == "online":
                await self.bot.change_presence(status=discord.Status.online, activity=playing)
                status_flag = True
            elif onlinetype == "idle":
                await self.bot.change_presence(status=discord.Status.idle, activity=playing)
                status_flag = True
            elif onlinetype in ["dnd","dead"]:
                await self.bot.change_presence(status=discord.Status.dnd, activity=playing)
                status_flag = True
            elif onlinetype == "invisible":
                await self.bot.change_presence(status=discord.Status.invisible, activity=playing)
                status_flag = True
            elif onlinetype == "reset":
                membercount = len(self.bot.users)
                game = discord.Game(f"世の隅の{membercount}人と一緒にいるよ！")
                await self.bot.change_presence(status=discord.Status.online,activity=game)
                await ctx.send(f"{ctx.author.mention}->ステータスをリセットしました！")
                status_flag = False
                return
            else:
                await ctx.send(f"{ctx.author.mention}->引数``onlinetype``の値が不正です！")
                return
            await ctx.send(f"{ctx.author.mention}->ステータスを更新しました！")
        else:
            await ctx.send(f"{ctx.author.mention}->権限がありません！")

    @tasks.loop(minutes=1)
    async def changestatus(self):
        global status_flag
        if status_flag == False:
            await self.bot.wait_until_ready()
            membercount = len(self.bot.users)
            game = discord.Game(f"世の隅の{membercount}人と一緒にいるよ！")
            await self.bot.change_presence(status=discord.Status.online,activity=game)
        else:
            pass


def setup(bot):
    bot.add_cog(Cog(bot))