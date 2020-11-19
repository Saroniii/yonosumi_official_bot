import discord
from discord.ext import commands
from discord.raw_models import RawReactionActionEvent
from yonosumi_utils import DeleteMessage as delete_message


class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.delete_message = delete_message()


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        await self.delete_message.add_trash_emoji(message)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        
        if payload.member.bot:
            return

        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        await self.delete_message.delete_bot_message(message, str(payload.emoji))


def setup(bot):
    bot.add_cog(Cog(bot))