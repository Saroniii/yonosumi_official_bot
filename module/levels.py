import discord
from discord.ext import commands
from yonosumi_utils import Level


class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.level = Level()


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        await self.level.get_level_role(
            message=message,
            bot=self.bot,
            check=self.level.check_meet_level_requirement(message)
        )


def setup(bot):
    bot.add_cog(Cog(bot))