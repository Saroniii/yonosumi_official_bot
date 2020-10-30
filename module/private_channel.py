import discord
from discord.ext import commands


class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        chid = 757410395299381340
        if chid == payload.channel_id and not payload.member.bot and str(payload.emoji) == "<:danbooorudaisuki:572190221370654741>":
            channel: discord.TextChannel = self.bot.get_channel(chid)
            guild: discord.Guild = channel.guild
            msg: discord.Message = await channel.fetch_message(payload.message_id)
            new_channel = await guild.create_text_channel(name=f"{payload.member.name}の防音室", category=channel.category)
            await new_channel.set_permissions(payload.member, manage_channels=True, read_messages=True, send_messages=True)
            await new_channel.send(f"{payload.member.mention}->防音室を作成しました！")
            await msg.remove_reaction(payload.emoji, payload.member)
        else:
            return


def setup(bot):
    bot.add_cog(Cog(bot))
