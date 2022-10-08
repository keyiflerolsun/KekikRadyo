# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core     import app, db, session, baslangic, konsol, cikis_yap, hata_yakala
from asyncio  import new_event_loop
from os       import listdir, remove

def basla():
    baslangic()
    app.run()

    konsol.log("[yellow][~] Girilen Dosyaların Silinmesi Bekleniyor...")
    for file in listdir():
        if file.endswith(".raw") or file.endswith(".mp3") or file.endswith(".png") :
            remove(file)

    async def close_session(session):
        await session.close()

    m_loop = new_event_loop()
    m_loop.run_until_complete(close_session(session))
    db.clear()
    app.stop()
    m_loop.close()

if __name__ == "__main__":
    try:
        basla()
        cikis_yap(False)
    except Exception as hata:
        hata_yakala(hata)