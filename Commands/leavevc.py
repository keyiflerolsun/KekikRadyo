# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core     import db, ROOT_ID
from pyrogram import Client, filters

@Client.on_message(filters.command("leavevc") & ~filters.private)
async def leavevc(client, message):
    if message.from_user.id != ROOT_ID:
        await message.reply("__**root** değilmişsin kekkooo__", quote=True)
        return

    global db
    chat_id = message.chat.id
    if chat_id in db and "call" in db[chat_id]:
        vc = db[chat_id]["call"]
        del db[chat_id]["call"]
        await vc.leave_current_group_call()
        await vc.stop()

    await message.reply_text("**Sesli Sohbetten Ayrıldı**", quote=False)