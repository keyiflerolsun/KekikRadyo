# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core     import db, ROOT_ID
from pyrogram import Client, filters

@Client.on_message(filters.command("skip") & ~filters.private)
async def skip_func(client, message):
    if message.from_user.id != ROOT_ID:
        await message.reply("__**root** değilmişsin kekkooo__", quote=True)
        return

    global db
    chat_id = message.chat.id
    if chat_id not in db:
        return await message.reply_text("**Sesli Sohbet Başlatılmadı..**")

    if "queue" not in db[chat_id]:
        return await message.reply_text("**Sesli Sohbet Başlatılmadı..**")

    queue = db[chat_id]["queue"]
    if queue.empty() and ("playlist" not in db[chat_id] or not db[chat_id]["playlist"]):
        return await message.reply_text("**Kuyruk Boş, Tıpkı Hayatınız Gibi.**", quote=False)

    db[chat_id]["skipped"] = True
    await message.reply_text("**Atlandı!**")