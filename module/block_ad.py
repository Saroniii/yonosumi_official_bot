import discord
from discord.ext import commands


class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot


    @commands.Cog.listener()
    async def on_message(self, message :discord.Message):
        ad_channel_id = 572737509923225600
        if message.author.bot or not message.channel.id == ad_channel_id:
            return print("b")

        print("a")
        
        msg :discord.Message 

        async for msg in message.channel.history(limit=25, oldest_first=True):
            print("c")
            if msg.content == message.content and not msg == message:
                print("d")
                await message.delete()
                content = f"{message.guild}の{message.channel.mention}での重複投稿を検知したため、対象の投稿を削除しました。"
                embed = discord.Embed(
                        title = "検知した過去の投稿",
                        description = f"{msg.content}\n\n[対象の投稿に飛ぶ]({msg.jump_url})",
                        timestamp = msg.created_at
                    ).set_footer(text=f"該当メッセージの投稿日")
                await message.author.send(content, embed=embed)
                logch = self.bot.get_channel(763722418182684672)
                await logch.send(content, embed=embed)
                break


def setup(bot):
    bot.add_cog(Cog(bot))