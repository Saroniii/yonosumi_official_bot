from typing import Callable, List
import aiosqlite3
import os
import discord
import dropbox

class Database:

    def __init__(self):
        self.database_name = "yonosumi.db" #データベース名のセット
        self.block_table_name = "block" #ブロックしているユーザーのテーブル名
        pass

    async def set_blocklist(self, has_database: bool) -> dict:
        """
        ユーザーのブロックリストを取得し、返します。
        """
        if has_database is False:
            return False
        
        connect: aiosqlite3.Connection = await aiosqlite3.connect(self.database_name)
        cursor: aiosqlite3.Cursor = await connect.cursor()

        blocklist = {}

        for row in await cursor.execute(f"SELECT * FROM {self.block_table_name}"):
            #row[0]->対象のユーザーID
            #row[1]->そのユーザーがブロックしているユーザーIDのリスト
            blocklist[row[0]] = self.convert_str_to_int_list_data(row[1])

        await connect.close()
        
        return blocklist
    
    def has_database(self, database_name =None):
        """
        指定したデータベースが存在するか確認します。
        """
        if not database_name:
            database_name = self.database_name
        
        if os.path.isfile(database_name):
            return True

        return False
    
    def convert_str_to_int_list_data(self, sentence :str):
        """
        文字列を数値型のリストに変換します。
        """
        return [int(i) for i in sentence.split(",")]

    async def execute_sql(self, sql: str, has_database, database ="yonosumi.db"):
        """
        SQLを実行します。
        """
        if has_database == False:
            return
        conn: aiosqlite3.Connection = await aiosqlite3.connect(database)
        c: aiosqlite3.Cursor = await conn.cursor()
        await c.execute(sql)
        await c.close()
        await conn.close()

    async def convert_int_list_to_member_list(self, guild: discord.Guild, member_id_list: List[int]) -> List[discord.Member]:
        """
        数値型のリストをメンバーのリストに変換します。
        """
        member_list = []
        for member_id in member_id_list:
            try:
                member = await guild.fetch_member(member_id)
                member_list.append(member)
            except:
                pass

        return member_list

class DropBox(Database):

    def __init__(self):
        self.dbx_token = os.environ["dropbox_token"]
        self.dbx = dropbox.Dropbox(self.dbx_token)
        self.database_name = "yonosumi.db" #データベース名のセット
        self.block_table_name = "block" #ブロックしているユーザーのテーブル名
        self.PATH_LOCAL = self.database_name
        self.PATH_DBX = f"/{self.database_name}"

    def download_database(self, database_name =None):
        """
        DropBox上からデータベースを取得します。
        """
        if not database_name:
            database_name = self.database_name

        dbx = self.dbx
        dbx.files_download_to_file(self.PATH_LOCAL, self.PATH_DBX)

    def upload_database(self, has_database: bool, database_name =None):
        """
        DropBox上にデータベースをアップロードします。
        """
        if has_database is False:
            return

        if not database_name:
            database_name = self.database_name
        
        dbx :dropbox = self.dbx
        with open(self.PATH_LOCAL, "rb") as f:
            dbx.files_upload(
                f.read(),
                self.PATH_DBX,
                mode=dropbox.files.WriteMode.overwrite
            )