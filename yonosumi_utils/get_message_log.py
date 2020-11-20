import discord
from discord.ext import commands
from datetime import datetime

class GetMessageLog:

    async def get_message_log(self, channel: discord.TextChannel, limit =None):
        """
        メッセージログを取得します。
        """
        log = f"#{channel}のチャットログ"
        message_count = 0
        async for message in channel.history(limit=limit, oldest_first=True):
            
            log += f"{message.author}({message.author.id}):{message.content}\n"
            message_count += 1

            if message.attachments:
                attachment_count = len(message.attachments)

                for i in range(attachment_count):
                    log += f"↪{message.attachments[i].url}\n"
        
        log += f"\n総メッセージ数:{message_count}"
        time = datetime.now()
        log += f"""
        \n\nこのメッセージログは、{time}時点の#{channel.name}のログを出力させたものです。\n
        このメッセージログの捏造等を固く禁じます。\n
        ©2020 Saroniii All rights rserved.
        """
                
        return log

    def return_text_file(self, filename: str, sentence: str):
        """
        テキストファイルに書き込みます。
        """
        with open(filename, mode='w') as f:
            f.write(sentence)
            
                
