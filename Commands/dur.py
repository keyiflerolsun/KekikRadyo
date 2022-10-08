# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core     import db, ROOT_ID
from pyrogram import Client, filters

@Client.on_message(filters.command("dur") & ~filters.private)
async def stop_vc(client, message):
    if message.from_user.id != ROOT_ID:
        await message.reply("__**root** değilmişsin kekkooo__", quote=True)
        return

    global db
    chat_id = message.chat.id
    if chat_id not in db:
        return await message.reply_text("**Sesli Sohbet Başlatılmadı..**")

    if "call" not in db[chat_id]:
        return await message.reply_text("**Sesli Sohbet Başlatılmadı..**")

    vc = db[chat_id]["call"]
    await vc.set_is_mute(True)

    if "stopped" not in db[chat_id]:
        db[chat_id]["stopped"] = False

    db[chat_id]["stopped"] = True
    await message.reply_text("**Durduruldu, Başlamak için /basla Gönder..**", quote=False)