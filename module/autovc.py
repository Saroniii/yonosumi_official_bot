import discord
from discord.ext import commands
from yonosumi_utils import voice

class Cog(commands.Cog):

    def __init__(self, bot):
        self.bot=bot
        self.voice = voice()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member :discord.Member, before :discord.VoiceState, after :discord.VoiceState):
        
        if self.voice.is_active(member.voice.channel, count_bots = False) and self.voice.is_generate_voice_channel(member.voice.channel):
            author_channel :discord.VoiceChannel = member.voice.channel
            voicechannel: discord.VoiceChannel = await author_channel.category.create_voice_channel(
                name=f"{member.name}の溜まり場"
                )
            textchannel: discord.TextChannel = await author_channel.category.create_text_channel(
                name=f"{member.name}の溜まり場",
                topic=self.voice.generate_auto_voice_topic(
                    voice=voicechannel,
                    member=member
                    )
                )
            await member.move_to(voicechannel, reason = "VCの自動生成が完了したため")
            base_embed = discord.Embed(
                title = f"{member.name}の溜まり場へようこそ！",
                description = f"ここでは、該当するリアクションを押すことで様々な設定を行うことが出来ます。\n\n✏：チャンネル名の変更\n\n🔒：利用可能人数の制限\n\n⚠：NSFWの有無"
            )
            
            msg: discord.Message = await textchannel.send(embed=base_embed)
            
            reaction_list = ["✏", "🔒", "⚠"]

            for emoji in reaction_list:
                await msg.add_reaction(emoji)


def setup(bot):
    bot.add_cog(Cog(bot))