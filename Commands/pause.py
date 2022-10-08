# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core     import db, ROOT_ID
from pyrogram import Client, filters

@Client.on_message(filters.command("pause") & ~filters.private)
async def pause_song_func(client, message):
    if message.from_user.id != ROOT_ID:
        await message.reply("__**root** değilmişsin kekkooo__", quote=True)
        return

    global db
    chat_id = message.chat.id
    if chat_id not in db:
        return await message.reply_text("**Sesli Sohbet Başlatılmadı..**")

    if "call" not in db[chat_id]:
        return await message.reply_text("**Sesli Sohbet Başlatılmadı..**")

    if "paused" in db[chat_id] and db[chat_id]["paused"] == True:
        return await message.reply_text("**Zaten Çalmıyor..**")

    db[chat_id]["paused"] = True

    vc = db[chat_id]["call"]
    await vc.pause_playout()

    await message.reply_text("**Müziği Duraklattı, Devam Etmek için `/resume` Gönder.**", quote=False)