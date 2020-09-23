import discord
from saica_utils.embed import SaicaEmbed

class SaicaMsg:
    
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