import discord
from discord.ext import commands
from yonosumi_utils import GetMessageLog as log, YonosumiMsg as msg, YonosumiStaff as staff
import yonosumi_utils


class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = log()
        self.msg = msg()
        self.staff = staff()


    @commands.command()
    async def get_message_log(self, ctx :commands.Bot, limit =None):
        
        if yonosumi_utils.is_nedoko(ctx.channel):
            if not yonosumi_utils.check_owner(ctx.author, ctx.channel) or not self.staff.is_admin(self.bot, ctx):
                return await ctx.send(f"{ctx.author.mention}->このコマンドは寝床所有者のみ使用できます！")
        
        else:
            if not self.staff.is_admin(self.bot, ctx):
                return await ctx.send(f"{ctx.author.mention}->このコマンドは寝床所有者のみ使用できます！")

        waiting = await self.msg.waiting(ctx)
        log = await self.log.get_message_log(channel=ctx.channel, limit=limit)
        filename = f"{ctx.channel.name}.txt"
        self.log.return_text_file(filename=filename, sentence=log)
        await waiting.delete()
        await ctx.send(f"{ctx.author.mention}->``{filename}``の出力が完了しました！",file=discord.File(filename))


def setup(bot):
    bot.add_cog(Cog(bot))