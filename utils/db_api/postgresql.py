
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool


import config

#класс для всех функций, связанных с базой данных
class Database:
    #с помощью pool происходит подключение к серверу. через него передаются данные
    def __init__(self, pool):
        self.pool: Pool = pool

    """host=config.IP"""

    #create заносит в pool аргументы для создания подключения к серверу
    @classmethod
    async def create(cls):
        pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            database=config.DB_NAME,
            host=config.DB_HOST

        )
        return cls(pool)

    #execute выполняет запросы к бд
    async def execute(self, command, *args,
                      #собрать ВСЕ данные, выгруженные в бд (и строки и столбцы)
                      fetch: bool = False,
                      # собрать только ОДНО значение из бд
                      fetchval: bool = False,
                      # собрать одну строчку из бд
                      fetchrow: bool = False,
                      # не собирать данные,а просто что-то выполнить
                      execute: bool = False):
        async with self.pool.acquire() as connection:
            connection: Connection

            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)

            logger(result)

            return result
    #создание таблицы юзеров
    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT NOT NULL UNIQUE,
        full_name VARCHAR(255) NULL
        );
        """
        await self.execute(sql, execute=True)

    #создание таблицы чатов с админом
    async def create_table_topics(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Topics (
        id SERIAL PRIMARY KEY,
        topic_id BIGINT NOT NULL,
        telegram_id BIGINT NOT NULL,
        question_type VARCHAR(255) NULL,
        theme VARCHAR(255) NULL
        );
        """

        await self.execute(sql, execute=True)



    #аргументы, по которым происходит выгрузка из бд (защита от ошибок и sql-инъекций)
    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)
        ])
        return sql, tuple(parameters.values())

    #добавление нового юзера в бд
    async def add_user(self, telegram_id,full_name):
        sql = "INSERT INTO Users (telegram_id, full_name) VALUES($1,$2)"
        return await self.execute(sql,telegram_id,full_name, fetchrow=True)

    #добавление нового топика
    async def add_topic(self,topic_id,telegram_id,question_type, theme):
        sql = "INSERT INTO Topics (topic_id, telegram_id, question_type, theme) VALUES($1,$2,$3,$4)"
        return await self.execute(sql, topic_id, telegram_id, question_type, theme, fetchrow=True)

    # получение айди нового топика
    async def select_topic_id(self, **kwargs):
        sql = "SELECT topic_id FROM Topics WHERE "
        sql,parameters = self.format_args(sql,parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    # получение айди юзера

    async def select_user_id(self, **kwargs):
        sql = "SELECT telegram_id FROM Topics WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    #добавление или обновление ФИО юзера
    async def update_fullname(self,fullname,telegram_id ):
        sql="UPDATE Users SET fullname=$1 WHERE telegram_id=$2"
        return await self.execute(sql,fullname,telegram_id)

    #выгрузка всех данных юзера
    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    # выгрузка данных одного юзера
    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

   #посчитать количество юзеров
    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)


    #удаление юзера из бд
    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    # удаление топика из бд
    async def delete_topic(self, topic_id):
        sql = "DELETE FROM Topics WHERE topic_id=$1"
        return await self.execute(sql, topic_id, fetchrow=True)

    #удаление таблицы юзеров
    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

def logger(statement):
    print(f"""
    -----------------------------------------------------------------

    Executing:
    {statement}

    -----------------------------------------------------------------
    """)