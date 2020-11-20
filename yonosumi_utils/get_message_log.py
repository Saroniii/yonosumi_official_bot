import discord
from discord.ext import commands

class GetMessageLog:

    async def get_message_log(self, channel: discord.TextChannel, limit =None):
        """
        メッセージログを取得します。
        """
        log = ""
        async for message in channel.history(limit=limit):
            
            log += f"{message.author}({message.author.id}):{message.content}\n"

            if message.attachments:
                attachment_count = len(message.attachments)

                for i in range(attachment_count):
                    log += f"↪{message.attachments[i].url}\n"
                
        return log

    def return_text_file(self, filename: str, sentence: str):
        """
        テキストファイルに書き込みます。
        """
        with open(filename, mode='w') as f:
            f.write(sentence)
            
                
