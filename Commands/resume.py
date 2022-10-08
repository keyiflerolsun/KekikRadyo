# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core     import db, ROOT_ID
from pyrogram import Client, filters

@Client.on_message(filters.command("resume") & ~filters.private)
async def resume_song(client, message):
    if message.from_user.id != ROOT_ID:
        await message.reply("__**root** değilmişsin kekkooo__", quote=True)
        return

    global db
    chat_id = message.chat.id
    if chat_id not in db:
        return await message.reply_text("**Sesli Sohbet Başlatılmadı..**")

    if "call" not in db[chat_id]:
        return await message.reply_text("**Sesli Sohbet Başlatılmadı..**")

    if "paused" in db[chat_id] and db[chat_id]["paused"] == False:
        return await message.reply_text("**Zaten Oynuyor**")

    db[chat_id]["paused"] = False

    vc = db[chat_id]["call"]
    await vc.resume_playout()

    await message.reply_text("**Sürdürüldü, Müziği Duraklatmak İçin `/pause` Gönderin.**", quote=False)