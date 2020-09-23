import discord
from discord.ext import commands
from saica_utils.embed import SaicaEmbed

def check_owner(member :discord.Member, channel :discord.TextChannel) -> bool:
    """
    選択したメンバーが個人チャンネルの所有者か確認できます。
    """
    if channel.permissions_for(member).manage_channels == True:
        return True
    else:
        return False

async def generate_channel_info(ctx :commands.Context) -> None:
    """
    個人チャンネル情報の一覧を生成します。
    """
    category :discord.CategoryChannel = ctx.channel.category
    for channel in category.text_channels:
        channel :discord.TextChannel
        user = None
        if not channel == ctx.channel:
            for obj in channel.overwrites:
                if type(obj) == discord.Member:
                    check = channel.overwrites_for(obj).manage_channels
                    if check == True:
                        user = obj
                        break
            if user == None:
                user = f"所有者なし"
            if channel.topic == None:
                channel.topic = "トピックが設定されていません。"
            
            embed = SaicaEmbed(title=f"{channel}")
            embed.add_field(name=f"チャンネルトピック",value=channel.topic)
            embed.add_field(name=f"所有者",value=f"{user}")
            await ctx.send(embed=embed)
        
def is_room(channel :discord.TextChannel) -> bool:
    """
    指定したチャンネルがroomであるか確認します。
    """
    if channel.category.name.startswith("ーー［ROOM-") and channel.guild.id == 560663701028339713:
        return True
    else:
        return False

def is_note(channel :discord.TextChannel) -> bool:
    """
    指定したチャンネルがnoteであるか確認します。
    """
    if channel.category.name.startswith("ーー［NOTE") and channel.guild.id == 679399823698427906:
        return True
    else:
        return False

def is_nedoko(channel :discord.TextChannel) -> bool:
    """
    指定したチャンネルが寝床であるか確認します。
    """
    if channel.category.name.startswith("ホームレス居住区") and channel.guild.id == 569928145906565126:
        return True
    else:
        return False

def is_my_channel(channel :discord.TextChannel) -> bool:
    """
    指定したチャンネルが寝床、note、roomのいずれかに該当するか確認します。
    """
    if is_note(channel) or is_nedoko(channel) or is_room(channel) == True:
        return True
    else:
        return False