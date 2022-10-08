# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core     import db
from pyrogram import Client, filters

from config  import YETKILI
from asyncio import Queue

@Client.on_message(filters.command("kuyruk") & ~filters.private)
async def queue_list(client, message):
    if message.from_user.id not in YETKILI:
        await message.reply("__admin değilmişsin kekkooo__", quote=True)
        return

    global db
    chat_id = message.chat.id
    if chat_id not in db:
        db[chat_id] = {}

    if "queue" not in db[chat_id]:
        db[chat_id]["queue"] = Queue()

    queue = db[chat_id]["queue"]

    if queue.empty():
        return await message.reply_text("__Kuyruk Boş, Tıpkı Hayatınız Gibi.__", quote=False)

    if (len(message.text.split()) > 1 and message.text.split()[1].lower() == "liste"):
        pl_format = True
    else:
        pl_format = False

    text = ""
    for count, song in enumerate(queue._queue, 1):
        if not pl_format:
            text += f"**{count}. {song['service'].__name__}** | __{song['query']}__  |  {song['requested_by']}\n"
        else:
            text += f"`{song['query']}`\n"
    if len(text) > 4090:
        return await message.reply_text(f"**Kuyrukta {queue.qsize()} şarkı var.**")

    await message.reply_text(text, disable_web_page_preview = True)