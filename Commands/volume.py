# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core     import db, ROOT_ID
from pyrogram import Client, filters

@Client.on_message(filters.command("volume") & ~filters.private)
async def volume_bot(client, message):
    if message.from_user.id != ROOT_ID:
        await message.reply("__**root** değilmişsin kekkooo__", quote=True)
        return

    global db
    usage = "**Kullanım:**\n/volume [1-200]"
    chat_id = message.chat.id

    if chat_id not in db:
        return await message.reply_text("Sesli Sohbet Başlatılmadı..")

    if "call" not in db[chat_id]:
        return await message.reply_text("Sesli Sohbet Başlatılmadı..")

    vc = db[chat_id]["call"]
    if len(message.command) != 2:
        return await message.reply_text(usage, quote=False)

    volume = int(message.text.split(None, 1)[1])

    if (volume < 1) or (volume > 200):
        return await message.reply_text(usage, quote=False)

    try:
        await vc.set_my_volume(volume=volume)
    except ValueError:
        return await message.reply_text(usage, quote=False)

    await message.reply_text(f"**Ses Ayarı {volume}**", quote=False)