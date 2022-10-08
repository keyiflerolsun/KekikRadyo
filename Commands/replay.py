# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core     import db
from pyrogram import Client, filters
from config   import YETKILI

@Client.on_message(filters.command("replay") & ~filters.private)
async def replay_vc(client, message):
    if message.from_user.id not in YETKILI:
        await message.reply("__admin değilmişsin kekkooo__", quote=True)
        return

    global db
    chat_id = message.chat.id
    if chat_id not in db:
        return await message.reply_text("**Sesli Sohbet Başlatılmadı..**")

    if "call" not in db[chat_id]:
        return await message.reply_text("**Sesli Sohbet Başlatılmadı..**")

    vc = db[chat_id]["call"]
    await vc.set_is_mute(True)
    await vc.set_is_mute(False)

    if "replayed" not in db[chat_id]:
        db[chat_id]["replayed"] = False

    db[chat_id]["replayed"] = True
    await message.reply_text("**Müzik Tekrarlanıyor..**", quote=False)