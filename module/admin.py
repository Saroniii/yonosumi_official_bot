import discord
from typing import Union
from discord.ext import commands
from yonosumi_utils import YonosumiStaff

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot


    @commands.command()
    async def clone_channel(self, ctx, channel: Union[discord.CategoryChannel, discord.TextChannel, discord.VoiceChannel]):
        if (await YonosumiStaff.is_admin(self.bot, ctx)):
            await channel.clone(reason="cloneコマンドを使用したため")


def setup(bot):
    bot.add_cog(Cog(bot))