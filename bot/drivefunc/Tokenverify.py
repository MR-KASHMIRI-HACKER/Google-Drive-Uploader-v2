
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import psycopg2

from bot import Post_url, Creds_path, LOGGER
from pyrogram import Filters


# conn = psycopg2.connect(DATABASE_URL)
conn = psycopg2.connect(Post_url)
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS USERINFO
    (
    id serial NOT NULL PRIMARY KEY UNIQUE,
    chat_id INTEGER,
    AUTH TEXT
    );'''
            )
conn.commit()


def filter_token():
    def is_token(flt, m):
        token = m.text
        token = token.split()[-1]
        TLEN = len(token)
        if TLEN == 57:
            if token[1] == "/":
                return True
            else:
                return False
        else:
            return False
    return Filters.create(is_token, "TokenFilterCreate")


# @Client.on_message(filter_token())
async def token_verify(client, message):

    token = message.text
    ID = str(message.from_user.id)
    try:
        gauth = GoogleAuth()
        gauth.Auth(token)
        gauth.SaveCredentialsFile(os.path.join(Creds_path, ID))
        a = await message.reply_text("Authorized successfully 🥳🥳")
        try:

            if os.path.isfile(os.path.join(Creds_path, ID)):
                chat_id = message.from_user.id,
                conn = psycopg2.connect(Post_url)
                cur = conn.cursor()
                file = open(os.path.join(Creds_path, str(ID)), 'r')
                Auth = file.read()
                file.close()
                cur.execute(
                    '''SELECT AUTH FROM USERINFO WHERE chat_id = %s ''', (chat_id))
                row = cur.fetchone()
                if row is None:
                    query = "INSERT INTO USERINFO (chat_id, AUTH) VALUES (%s,%s)"
                    cur.execute(query, (chat_id, Auth))
                conn.commit()
                # await a.edit("Token added to database.")
                LOGGER.info(f"{chat_id}: Token Added To database")
        except Exception as e:
            await a.edit(e)
    except Exception as e:
        print("Auth Error :", e)
        # TODO Auth error msg
        await message.reply_text(f"Auth Error: \n `{e}`\n\n #error ")


def token_make(client, message):
    chat_id = str(message.from_user.id)

    ID = str(message.from_user.id)
    if not os.path.isfile(os.path.join(Creds_path, str(ID))):
        conn = psycopg2.connect(Post_url)
        cur = conn.cursor()
        cur.execute(
            '''SELECT AUTH FROM USERINFO WHERE chat_id = %s''', (chat_id,))
        row = cur.fetchone()
        if row is not None:
            A = row[0]
            # os.mknod(os.path.join(Creds_path,str(ID)))
            f = open(os.path.join(Creds_path, str(ID)), "w")
            f.write(A)
            f.close()
            LOGGER.info(f"{chat_id} : Token File Created")
            return True
        else:
            return False