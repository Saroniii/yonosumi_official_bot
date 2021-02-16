from typing import Callable, Union

import discord
from discord.ext import commands


class Level:

    def __init__(self):
        self.mee6_id = 159985870458322944
        self.level_notify_channel_id = 572149626535411723
        self.level_roles = {
            1: 586769410346319872,
            5: 587986698449977344,
            10: 587987226638680083,
            20: 587987652062740480,
            30: 587988225138884628,
            40: 587988558531395624,
            50: 587988373243953171,
        }
        self.mee6_notify_channel_id = 771288074768482304
        self.level_list = [level for level in self.level_roles.keys()]

    async def get_level_role(self, message: discord.Message, bot: commands.Bot, check: Callable[[int], Union[int, tuple]]):
        """
        レベル役職を付与します。
        """

        if check == "NO DATA":
            return

        data = check[1]
        member = await message.guild.fetch_member(data['user_id'])
        await self.announce_level_up(member, data['level'], bot)

        if check[0] is False:
            return

        role = message.guild.get_role(check[0])
        await self.remove_old_roles(message.guild, member)
        await member.add_roles(role, reason="レベルが上がったため")

    async def announce_level_up(self, member: discord.Member, level: int, bot: commands.Bot) -> None:
        announce_template = f"お、 {member.mention} のレベル {level} に！さすが {member}。やるじゃねぇか。"
        announce_channel = bot.get_channel(self.level_notify_channel_id)
        await announce_channel.send(content=announce_template)

    async def remove_old_roles(self, guild: discord.Guild, member: discord.Member) -> None:
        for role in self.level_roles.values():
            await member.remove_roles(
                guild.get_role(role),
                reason="レベル役職の付替えのため"
            )

    def check_meet_level_requirement(self, message: discord.Message) -> Union[int, tuple]:
        """
        レベル役職を付与する条件を満たしているか確認します。
        ※満たしている場合は満たしている役職のIDを、満たしていない場合はFalseを返し、第2引数には必ずanalysis_message関数の戻り値が返ります。
        """

        data = self.analysis_message(message)

        if data == False:
            return 'NO DATA'

        if data['level'] in self.level_list:
            return self.level_roles[data['level']], data

        return False, data

    def analysis_message(self, message: discord.Message) -> Union[dict, bool]:
        """
        MEE6のメッセージを解析します。
        """
        if not self.is_level_up_message(message):
            return False

        data = message.content.splitlines()
        return {
            'user_id': int(data[0]),
            'level': int(data[1]),
        }

    def is_level_up_message(self, message: discord.Message):
        """
        指定のメッセージがMEE6によるレベルアップメッセージか確認します。
        """
        if message.author.id == self.mee6_id and message.channel.id == self.mee6_notify_channel_id:
            return True

        else:
            return False
