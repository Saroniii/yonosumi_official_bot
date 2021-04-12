import re
from asyncio import TimeoutError
from yonosumi_utils import my_channel

import discord
import yonosumi_utils
from discord.ext import commands
from yonosumi_utils import YonosumiMsg as msg
from yonosumi_utils import voice

reaction_list = ["✏", "🔒", "👀"]


class Cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.voice = voice()
        self.msg = msg()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState,
                                    after: discord.VoiceState):
        category_id = 770140316078309416
        category: discord.CategoryChannel = self.bot.get_channel(category_id)
        ignore_vcs = [831044684226625546]

        if member.voice is None:
            await self.voice.clean_null_auto_text_channels(
                category,
                await self.voice.clean_null_auto_voice_channels(category, ignore_vcs)
            )

        elif self.voice.is_active(member.voice.channel, count_bots=False) and self.voice.is_generate_voice_channel(
                member.voice.channel) and not before.channel:

            author_channel: discord.VoiceChannel = member.voice.channel
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

            await member.move_to(voicechannel, reason="VCの自動生成が完了したため")
            control_embed = discord.Embed(
                title=f"{member.name}の溜まり場へようこそ！",
                description=self.voice.control_panel_description()
            )

            msg: discord.Message = await textchannel.send(embed=control_embed)

            global reaction_list

            for emoji in reaction_list:
                await msg.add_reaction(emoji)

            await msg.pin()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):

        if payload.member.bot:
            return

        channel: discord.TextChannel = self.bot.get_channel(payload.channel_id)
        guild: discord.Guild = self.bot.get_guild(payload.guild_id)
        voice_category_id = 770140316078309416

        if not self.voice.is_muted_text_channel(channel) or payload.member != await self.voice.get_auto_voice_owner(
                channel):
            return

        message: discord.Message = await channel.fetch_message(payload.message_id)

        if not self.voice.is_voice_control_panel(message, self.bot):
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
                title=f"{payload.member.mention}->VCに入れる最大人数を指定してください。"
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

        elif str(payload.emoji) == "👀":

            if not self.voice.is_hide(payload.member.voice.channel):

                result = "非公開"

                vc: discord.VoiceChannel = self.bot.get_channel(my_channel.get_topic(channel, split=True)[1])

                for member in payload.member.voice.members:
                    await channel.set_permissions(
                        target=member,
                        view_channel=True,
                    )

                    await vc.set_permissions(
                        target=member,
                        view_channel=True,
                        connect=True
                    )

                await vc.set_permissions(
                    guild.default_role,
                    view_channel=False,
                    connect=False
                )

                await channel.set_permissions(
                    guild.default_role,
                    view_channel=False
                )

            else:

                result = "公開"

                vc: discord.VoiceChannel = self.bot.get_channel(my_channel.get_topic(channel, split=True)[1])

                await vc.set_permissions(
                    guild.default_role,
                    read_messages=True,
                    connect=True
                )

                await channel.set_permissions(
                    guild.default_role,
                    read_messages=True
                )

            await channel.send(
                content=f"{payload.member.mention}->このVCを``{result}``にしました！"
            )


def setup(bot):
    bot.add_cog(Cog(bot))
