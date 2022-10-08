# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core   import app, db
from config import TG_MAX_MB
from Lib    import change_vc_title, transcode, pause_skip_watcher

from asyncio   import get_running_loop
from functools import partial
from os.path   import exists
from os        import remove

# Telegram
async def telegram(_, __, message):
    global db
    chat_id = message.chat.id

    if chat_id not in db:
        db[chat_id] = {}

    if not message.reply_to_message:
        return await message.reply_text("**Bir sese yanıt verin.**", quote=False)

    if not message.reply_to_message.audio:
        return await message.reply_text("**Yalnızca Ses Dosyaları (Belge Değil) Desteklenir.**", quote=False)

    if int(message.reply_to_message.audio.file_size) >= TG_MAX_MB * 1_048_576: # This is Byte
        return await message.reply_text(f"**Bruh! Yalnızca {TG_MAX_MB} MB içindeki şarkılar.**", quote=False)

    duration = message.reply_to_message.audio.duration

    if not duration:
        return await message.reply_text("**Yalnızca Süresi Belirli Şarkılar Desteklenir.**", quote=False)

    title     = message.reply_to_message.audio.title
    performer = message.reply_to_message.audio.performer

    db[chat_id]["currently"] = {
        "artist": performer,
        "song": title,
        "query": None,
    }

    mesaj = await message.reply_text("**İndiriliyor..**", quote=False)
    song  = await message.reply_to_message.download()

    await mesaj.edit("**Kod Dönüştürülüyor..**")
    try:
        title = message.reply_to_message.audio.title or message.reply_to_message.audio.performer

        await change_vc_title(title, chat_id)
    except Exception:
        await app.send_message(chat_id, text="[HATA]: VC BAŞLIĞI DÜZENLENMEDİ, BENİ YÖNETİCİ YAPIN.")

    loop = get_running_loop()
    await loop.run_in_executor(None, partial(transcode, song, chat_id))

    await mesaj.edit(f"**Çalıyor** **{message.reply_to_message.link}.**")
    await pause_skip_watcher(mesaj, duration, chat_id)

    if exists(song):
        remove(song)