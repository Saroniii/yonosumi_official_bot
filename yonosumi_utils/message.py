import discord
from yonosumi_utils.embed import YonosumiEmbed
from asyncio import TimeoutError
from typing import Union
from discord.ext import commands

class YonosumiMsg:
    
    @staticmethod
    async def waiting(ctx):
        return await ctx.send(f"{ctx.author.mention}->処理中です...")
    
    @staticmethod
    async def no_permission(ctx):
        return await ctx.send(f"{ctx.author.mention}->このコマンドを実行する権限がありません！")

    @staticmethod
    async def custom_waiting(ctx, *, arg :str):
        return await ctx.send(f"{ctx.author.mention}->{arg}です...")

    @staticmethod
    async def startup_process(ctx):
        return await ctx.send(f"{ctx.author.mention}->起動処理中です...再度お試しください...")

    @staticmethod
    async def question(bot :commands.Bot, main_object :Union[commands.Context, discord.Message, discord.RawReactionActionEvent], title :str) -> Union[dict, bool]:
        if type(main_object) in [discord.Message, commands.Context]:
            member = main_object.author
            def check(m):
                return m.author == member and m.channel == main_object.channel
            question = await main_object.channel.send(content = title)
            
        else:
            member = main_object.member
            channel = bot.get_channel(main_object.chsnnel_id)
            def check(m):
                return m.author == member and m.channel == channel
            question = await channel.send(content = title)

        try:
            msg = await bot.wait_for(
                'message',
                check=check,
                timeout=60.0
                )

        except TimeoutError:
            await question.edit(content=f"{member.mention}->入力待機時間内に応答がありませんでした！")
            return False
        
        return {
            'result':msg,
            'question':question
        }
