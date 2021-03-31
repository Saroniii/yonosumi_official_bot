import discord
from discord.ext import commands
import asyncio


class Cog(commands.Cog):

    def __init__(self):
        self.bot = bot
        self.bot.shiritori_ch_id = 826776534526197770

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.channel.id == shiritori_ch_id:
            return

        msg: discord.Message

        async for msg in message.channel.history(limit=25):

            if msg.content == message.content and not msg == message and message.content or msg.content is None:

                await message.delete()
                content = f"{message.author.mention}->{message.content}は25メッセージ以内に既に使われています！"

                embed = discord.Embed(
                    title="検知した同様のワード",
                    description=f"{msg.content}\n\n[対象の投稿に飛ぶ]({msg.jump_url})",
                ).set_footer(text=f"このメッセージは15秒後に削除されます")

                msg = await message.channel.send(content, embed=embed)
                await asyncio.sleep(15)
                await msg.delete()
                return

        await message.add_reaction("✅")