import discord
from discord.ext import commands
from yonosumi_utils import GetMessageLog as log
from yonosumi_utils import YonosumiMsg as msg


class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = log()
        self.msg = msg()


    @commands.command()
    async def get_message_log(self, ctx :commands.Bot, limit =None):
        waiting = await self.msg.waiting(ctx)
        log = await self.log.get_message_log(channel=ctx.channel, limit=limit)
        filename = f"{ctx.channel.name}.txt"
        self.log.return_text_file(filename=filename, sentence=log)
        await waiting.delete()
        await ctx.send(f"{ctx.author.mention}->``{filename}``の出力が完了しました！",file=discord.File(filename))


def setup(bot):
    bot.add_cog(Cog(bot))