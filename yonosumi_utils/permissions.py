import discord
from discord.ext import commands


class YonosumiStaff:

    @staticmethod
    async def is_admin(bot: commands.Bot, ctx: commands.Context):
        try:
            if [i for i in (await bot.get_guild(569928145906565126).fetch_member(ctx.author.id)).roles if i.id == 579558148914806796]:
                return True
            else:
                return False
        except:
            return False
