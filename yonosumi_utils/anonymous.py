import asyncio
from typing import Union

import discord
from discord.ext import commands

anonymous_channels = {
    'counseling': (583991230493491200, '❓'),
    'nedoko': (598178762957520896, '📦'),
    'cancel': (0, '❌')
}


class Anonymous:

    def __init__(self):
        self.anonymous_channels = anonymous_channels
        self.button_emojis = ["❓", "📦", "❌"]

    async def setup_anonymous(self, channel: discord.DMChannel, message: discord.Message) -> discord.Message:
        """
        匿名メッセージを送信するためのセットアップをします。
        """

        embed = discord.Embed(
            title="どうなさいましたか？",
            description="""
            ❓：上のメッセージを<#583991230493491200>に送信したいです。\n
            📦：上のメッセージを<#598178762957520896>に送信したいです。\n
            ❌：間違えました！気にしないで下さい！
            """
        )

        message: discord.Message = await channel.send(embed=embed)
        await self.add_buttons(message)
        return message

    async def add_buttons(self, message: discord.Message) -> None:
        """
        ボタンとなるリアクションを追加します。
        """
        for button in self.button_emojis:
            await message.add_reaction(button)

    async def wait_answer(self, channel: discord.DMChannel, message: discord.Message, bot: commands.Bot) -> Union[str, None]:
        """
        リアクションの解答を待ちます。
        """
        def check(reaction, user):
            return user == channel.recipient and str(reaction) in self.button_emojis

        try:
            reaction_value = await bot.wait_for('add_reaction', check=check, timeout=60.0)
            await message.remove_reaction(str(reaction_value), channel.recipient)

        except asyncio.TimeoutError:
            await message.edit(
                content=f"入力待機時間を超過しました！",
                embed=None
            )
            return None

        return str(reaction_value)

    async def do_task(self, message: discord.Message, reaction: Union[str, None]) -> Union[int, None]:
        """
        入力待機で得たデータを処理します。
        """
        if reaction is None:
            return None

        if reaction == "❓":
            return self.anonymous_channels['counseling'][0]

        elif reaction == "📦":
            return self.anonymous_channels['nedoko'][0]

        elif reaction == "❌":
            await message.edit(
                content=f"送信をキャンセルしました！",
                embed=None
            )
            return 0

    async def send_anonymous(self, channel_id: Union[int, None], bot: commands.Bot, message: discord.Message) -> Union[None, bool]:

        if channel_id is None and not 0:
            return None

        anonymous_channel: discord.TextChannel = bot.get_channel(channel_id)

        anonymous_embed = discord.Embed(
            title="匿名さんからメッセージが届きました。",
            description=message.content,
            timestamp=message.created_at
        )
        anonymous_embed.set_footer(text="送信日時")

        await anonymous_channel.send(embed=anonymous_embed)
