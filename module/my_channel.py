import yonosumi_utils
from yonosumi_utils.embed import yonosumiEmbed
import yonosumi_utils.my_channel as my_channel
import discord
from discord.ext import commands
import asyncio

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.room = {
            'bot_role':560675500557860871,
            'guild':560663701028339713,
            'member_role':560668622222000128,
        }

    @commands.command()
    async def setname(self, ctx :commands.Context, *, after_name :str):
        if my_channel.is_nedoko(ctx.channel):
            data = {}
            for perm in ctx.channel.permissions_for(ctx.author):
                data[perm[0]] = perm[1]
            if data['manage_channels'] == True:
                await ctx.channel.edit(name=after_name)
                await ctx.send(f"{ctx.author.mention}->このチャンネル名を``{after_name}``に変更しました！")
            else:
                await ctx.message.delete()
        else:
            await ctx.send(f"{ctx.author.mention}->この機能は、寝床内で使用できます！")

    @commands.command()
    async def settopic(self, ctx, *, topic):
        if my_channel.is_nedoko(ctx.channel):
            data = {}
            for perm in ctx.channel.permissions_for(ctx.author):
                data[perm[0]] = perm[1]
            if data['manage_channels'] == True:
                if topic == "None":
                    await ctx.channel.edit(topic=None)
                    await ctx.send(f"{ctx.author.mention}->このチャンネルのチャンネルトピックを削除しました！")
                else:
                    await ctx.channel.edit(topic=topic)
                    await ctx.send(f"{ctx.author.mention}->このチャンネルのチャンネルトピックを以下の文章に変更しました！\n```\n{topic}\n```")
            else:
                await ctx.message.delete()
        else:
            await ctx.send(f"{ctx.author.mention}->この機能は、寝床内で使用できます！")

    @commands.command()
    async def settrusted(self, ctx, check, member :discord.Member):
        if my_channel.is_nedoko(ctx.channel):
            if check in ["add","+","a"]:
                data = {}
                for perm in ctx.channel.permissions_for(ctx.author):
                    data[perm[0]] = perm[1]
                if data["manage_channels"] == True:
                    wait_message = await ctx.send(f"{ctx.author.mention}->",embed=discord.Embed(title=f"⚠{member}を#{ctx.channel}の信頼人に追加しようとしています！⚠",description=f"信頼人を付与すると、``{member}``は以下のことが可能になります：\n```○メッセージの管理(ピン留めや削除)\n○このホームが非公開にされている場合の閲覧可能権限```\n**__信頼できる人、もしくはサブアカウントなどに付与するようにして下さい！__**\n\n``{member}``に信頼人を付与する場合は✅を、付与しない場合は❌を押して下さい。"))
                    for emoji in ["✅","❌"]:
                        await wait_message.add_reaction(emoji)
                    def check(reaction,user):
                        return user == ctx.author and str(reaction.emoji) in ['✅','❌']
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
                    except asyncio.TimeoutError:
                        await wait_message.clear_reactions()
                        await wait_message.edit(content=f"{ctx.author.mention}->指定した時間までに反応がなかったため、付与を行いませんでした！",embed=None)
                    else:
                        if reaction.emoji == "✅":
                            await ctx.channel.set_permissions(member,manage_messages=True,read_messages=True)
                            await wait_message.clear_reactions()
                            try:
                                await member.send(f"あなたは、``{ctx.author}``から{ctx.channel.mention}の信頼人に追加されました！")
                            except:
                                pass
                            await wait_message.edit(content=f"{ctx.author.mention}->``{member}``を信頼人に追加しました！",embed=None)
                        else:
                            await wait_message.clear_reactions()
                            await wait_message.edit(content=f"{member}を信頼人に追加することをキャンセルしました！",embed=None)
            elif check in ["del","delete","remove","d","r","-"]:
                data = {}
                for perm in ctx.channel.permissions_for(ctx.author):
                    data[perm[0]] = perm[1]
                if data["manage_channels"] == True:
                    trust = {}
                    for perm in ctx.channel.permissions_for(member):
                        trust[perm[0]] = perm[1]
                    if trust["manage_messages"] == False:
                        await ctx.send(f"{ctx.author.mention}->``{member}``は信頼人ではありません！")
                        return
                    else:
                        wait_message = await ctx.send(f"{ctx.author.mention}->",embed=discord.Embed(title=f"⚠{member}を#{ctx.channel}の信頼人から削除しようとしています！⚠",description=f"``{member}``から信頼人を削除する場合は✅を、削除しない場合は❌を押して下さい。"))
                        for emoji in ["✅","❌"]:
                            await wait_message.add_reaction(emoji)
                        def check(reaction,user):
                            return user == ctx.author and str(reaction.emoji) in ['✅','❌']
                        try:
                            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
                        except asyncio.TimeoutError:
                            await wait_message.clear_reactions()
                            await wait_message.edit(content=f"{ctx.author.mention}->指定した時間までに反応がなかったため、削除を行いませんでした！",embed=None)
                        else:
                            if reaction.emoji == "✅":
                                await ctx.channel.set_permissions(member,manage_messages=None,read_messages=None)
                                await wait_message.clear_reactions()
                                await wait_message.edit(content=f"{ctx.author.mention}->``{member}``を信頼人から削除しました！",embed=None)
                            else:
                                await wait_message.clear_reactions()
                                await wait_message.edit(content=f"{member}を信頼人から削除することをキャンセルしました！",embed=None)
                else:
                    await ctx.message.delete()
            else:
                await ctx.send(f"{ctx.author.mention}->使用方法は``s/settrusted <add/del> <追加したいユーザー>``です！\n※``add``は追加を、``del``は削除を示しています。")                    
        else:
            await ctx.send(f"{ctx.author.mention}->この機能は、寝床内で使用できます！")

    @commands.command()
    async def setlock(self, ctx :commands.Context, check :str):
        if my_channel.is_nedoko(ctx.channel):
            data = {}
            for perm in ctx.channel.permissions_for(ctx.author):
                data[perm[0]] = perm[1]
            if data['manage_channels'] == True:
                role = ctx.guild.get_role(570641230661156870)
                if check == "True":
                    await ctx.channel.set_permissions(role,read_messages=False)
                    await ctx.send(f"{ctx.author.mention}->このチャンネルを``ロック``しました！このチャンネルは現在、信頼人とスタッフにのみ見えています！")
                elif check == "False":
                    await ctx.channel.set_permissions(role,read_messages=True)
                    await ctx.send(f"{ctx.author.mention}->このチャンネルを``アンロック``しました！このチャンネルは現在、全ての個人チャンネル利用者に見えています！")
                else:
                    await ctx.send(f"{ctx.author.mention}->チャンネルをロックするためには、``s/setlock <True/False>`` と入力して下さい！\n※``True``が``有効化``、``False``が``無効化``になります。")
            else:
                await ctx.message.delete()
        else:
            await ctx.send(f"{ctx.author.mention}->この機能は、寝床内で使用できます！")

    @commands.command()
    async def block(self, ctx, user :discord.Member):
        if my_channel.is_nedoko(ctx.channel):
            if ctx.channel.permissions_for(ctx.author).manage_channels == True:
                await ctx.channel.set_permissions(user,read_messages=False)
                await ctx.send(f"{ctx.author.mention}->``{user}``から``{ctx.channel}``を見えなくしました！")
            else:
                await ctx.send(f"{ctx.author.mention}->あなたは、``{ctx.channel}``の所有者ではありません！")
        else:
            return

    @commands.command()
    async def unblock(self, ctx, user :discord.Member):
        if my_channel.is_nedoko(ctx.channel):
            if ctx.channel.permissions_for(ctx.author).manage_channels == True:
                await ctx.channel.set_permissions(user,read_messages=None)
                await ctx.send(f"{ctx.author.mention}->``{user}``から``{ctx.channel}``を見えるようにしました！")
            else:
                await ctx.send(f"{ctx.author.mention}->あなたは、``{ctx.channel}``の所有者ではありません！")
        else:
            return

def setup(bot):
    bot.add_cog(Cog(bot))
