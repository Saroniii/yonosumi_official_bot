import discord
from discord.ext import commands
from yonosumi_utils import Anonymous as tokumei


class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.tokumei = tokumei()


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if not type(message.channel) == discord.DMChannel or message.author.bot:
            return

        dialog = await self.tokumei.setup_anonymous(
            channel=message.channel,
            message=message,
        )

        reaction = await self.tokumei.wait_answer(
                channel=message.channel,
                message=dialog,
                bot=self.bot
            )

        channel_id = await self.tokumei.do_task(
            message=message,
            reaction=reaction
        )

        await self.tokumei.send_anonymous(
            channel_id=channel_id,
            bot=self.bot,
            message=message
        )

        return await message.channel.send('メッセージを匿名で送信しました！')



def setup(bot):
    bot.add_cog(Cog(bot))