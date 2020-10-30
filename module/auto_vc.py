import re
import discord
from discord.ext import commands
from yonosumi_utils import voice, YonosumiMsg as msg
from asyncio import TimeoutError

import yonosumi_utils

reaction_list = ["✏", "🔒"]

class Cog(commands.Cog):

    def __init__(self, bot):
        self.bot=bot
        self.voice = voice()
        self.msg = msg()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member :discord.Member, before :discord.VoiceState, after :discord.VoiceState):
        category_id = 770140316078309416
        category: discord.CategoryChannel = self.bot.get_channel(category_id)

        if member.voice is None:
            await self.voice.clean_null_auto_text_channels(
                category,
                await self.voice.clean_null_auto_voice_channels(category)
                )

        elif self.voice.is_active(member.voice.channel, count_bots = False) and self.voice.is_generate_voice_channel(member.voice.channel):
            
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
            control_embed = discord.Embed(
                title = f"{member.name}の溜まり場へようこそ！",
                description = self.voice.control_panel_description()
            )
            
            msg: discord.Message = await textchannel.send(embed=control_embed)
            
            global reaction_list

            for emoji in reaction_list:
                await msg.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload :discord.RawReactionActionEvent):
        
        if payload.member.bot:
            return 

        channel :discord.TextChannel = self.bot.get_channel(payload.channel_id)
        voice_category_id = 770140316078309416

        if not self.voice.is_muted_text_channel(channel) or payload.member != await self.voice.get_auto_voice_owner(channel):
            return

        message :discord.Message = await channel.fetch_message(payload.message_id)

        if not self.voice.is_voice_control_panel(message):
            return
        
        global reaction_list

        if not str(payload.emoji) in reaction_list:
            return
        
        await message.remove_reaction(payload.emoji, payload.member)

        if str(payload.emoji) == "✏":
            
            msg = await self.msg.question(
                bot=self.bot,
                main_object=message,
                member=payload.member,
                title=f"{payload.member.mention}->変更したい名前を入力してください。"
            )

            if msg == False:
                return

            result = msg['result']
            question = msg['question']

            if len(result.content) > 0:
                vc_id = int(yonosumi_utils.get_topic(channel, split=True)[1])
                if vc_id is None:
                    return await question.edit(content=f"{payload.member.mention}->不明なエラーが発生しました！")
                
                vc = self.bot.get_channel(vc_id)

                await channel.edit(name=result.content)
                await vc.edit(name=result.content)
                await channel.send(f"{payload.member.mention}->チャンネル名を``{result.content}``に変更しました！")

        elif str(payload.emoji) == "🔒":
            
            msg = await self.msg.question(
                bot=self.bot,
                main_object=message,
                member=payload.member,
                title=f"{payload.member.mention}->変更したい名前を入力してください。"
            )

            if msg == False:
                return

            result = msg['result']
            question = msg['question']
            
            try:
                num = int(result.content)
            except:
                return await question.edit(content=f"{payload.member.mention}->不正な値が渡されました！")

            if not num > 100:
                vc_id = int(yonosumi_utils.get_topic(channel, split=True)[1])
                if vc_id is None:
                    return await question.edit(content=f"{payload.member.mention}->不明なエラーが発生しました！")
                vc = self.bot.get_channel(vc_id)
                await vc.edit(user_limit=num)
                await channel.send(f"{payload.member.mention}->VCの参加可能人数を``{num}人``に変更しました！")
            else:
                return await question.edit(content=f"{payload.member.mention}->100人以上は指定できません！")
        

def setup(bot):
    bot.add_cog(Cog(bot))