# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core import app, db, session, baslangic
from pyrogram import idle
import asyncio, os

baslangic()
app.start()
idle()

print("Girilen Dosyaların Silinmesi Bekleniyor...")
for file in os.listdir():
    if file.endswith(".raw") or file.endswith(".mp3") or file.endswith(".png") :
        os.remove(file)
print("Kapatılıyor...")

async def close_session(session):
    await session.close()

m_loop = asyncio.get_event_loop()
m_loop.run_until_complete(close_session(session))
db.clear()
app.stop()
m_loop.close()