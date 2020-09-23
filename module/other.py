import discord
from discord.ext import commands, tasks

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command()
    async def genbotinvite(self, ctx, user :discord.User):
        bot = False
        if user.bot:
            bot = True
        if bot == False:
            await ctx.send(f"{ctx.author.mention}->``{user.name}``はBotではありません！")
        else:
            await ctx.send(f"{ctx.author.mention}->``{user.name}``の招待リンクはこちら\nhttps://discordapp.com/oauth2/authorize?client_id={str(user.id)}&permissions=2146958847&scope=bot")


def setup(bot):
    bot.add_cog(Cog(bot))
