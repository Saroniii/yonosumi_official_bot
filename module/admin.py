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
            cloned_channel = await channel.clone(reason="cloneコマンドを使用したため")
            await ctx.send(f"{ctx.author.mention}->{channel.mention}を複製しました！({cloned_channel.mention})")

    @commands.command()
    async def create_nedoko(self, ctx: commands.Context, owner: discord.Member):
        if (await YonosumiStaff.is_admin(self.bot, ctx)):
            
            making_nedoko_category_id = 800189192637513759
            making_nedoko: discord.CategoryChannel = self.bot.get_channel(making_nedoko_category_id)

            nedoko: discord.TextChannel = await making_nedoko.create_text_channel(name=f"{owner.name}の寝床")
            await nedoko.set_permissions(owner, read_messages=True, manage_channels=True, manage_messages=True)

            await ctx.send(content=f"{ctx.author.mention}->`{owner}`の寝床を作成しました。({nedoko.mention})")

def setup(bot):
    bot.add_cog(Cog(bot))