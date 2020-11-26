import discord
from discord.ext import commands


class BlockList:

    def __init__(self):
        pass

    def get_user_block_data(self, member: discord.Member, block_list: dict):
        """
        指定したユーザーのブロックデータを取得し、返します。
        データがなかった場合はNoneを返します。
        """
        
        try:
            block_data = block_list[member.id]
        except:
            block_data = None

        return block_data