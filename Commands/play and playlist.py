# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from contextlib     import suppress
from Core           import db, ROOT_ID
from pyrogram       import Client, filters
from pyrogram.types import Message

from config    import YETKILI
from Lib       import get_default_service
from asyncio   import Queue
from traceback import format_exc

from Music import available_services

@Client.on_message(filters.command("play") & ~filters.private)
async def play_song(client, message):
    if message.from_user.id not in YETKILI:
        await message.reply("__admin değilmişsin kekkooo__", quote=True)
        return

    global db
    chat_id = message.chat.id
    try:
        if len(message.command) < 2 and (not message.reply_to_message or not message.reply_to_message.audio):
            return await message.reply_text("**Kullanım:**\n\n`/play Eypio - Dardayım`", quote=False)

        if chat_id not in db:
            db[chat_id] = {}

        if "call" not in db[chat_id]:
            return await message.reply_text("**Önce /joinvc !**")

        if message.reply_to_message:
            if not message.reply_to_message.audio:
                return await message.reply_text("**Ses dosyasına cevap verin veya alıntılamadan komut verin!**")

            service   = "telegram"
            song_name = message.reply_to_message.audio.title
        else:
            text = message.text.split("\n")[0]
            text = text.split(None, 2)[1:]
            service = text[0].lower()
            services = list(available_services.keys())
            if service in services:
                song_name = text[1]
            else:
                service   = get_default_service()
                song_name = " ".join(text)

        requested_by = message.from_user.mention

        if chat_id not in db:
            db[chat_id] = {}

        if "queue" not in db[chat_id]:
            db[chat_id]["queue"] = Queue()

        if not db[chat_id]["queue"].empty() or ("running" in db[chat_id] and db[chat_id]["running"]):
            await message.reply_text(f"🎵 `{song_name}`\n\n🎧 **{message.from_user.mention} tarafından** __Kuyruğa Eklendi.__", quote=False, disable_web_page_preview=True)

        await db[chat_id]["queue"].put(
            {
                "service"       : available_services[service],
                "requested_by"  : requested_by,
                "query"         : song_name,
                "message"       : message,
            }
        )

        if "running" not in db[chat_id]:
            db[chat_id]["running"] = False

        if not db[chat_id]["running"]:
            db[chat_id]["running"] = True
            await start_queue(chat_id)

    except Exception as e:
        await message.reply_text(str(e), quote=False)
        e = format_exc()
        print(e)


@Client.on_message(filters.command("playlist") & ~filters.private)
async def playlist(client: Client, message: Message, redirected=False):
    if message.from_user.id != ROOT_ID:
        await message.reply("__**root** değilmişsin kekkooo__", quote=True)
        return

    global db
    chat_id = message.chat.id
    if message.reply_to_message:
        raw_playlist = message.reply_to_message.text
    elif len(message.text) > 9:
        raw_playlist = message.text[10:]
    else:
        return await message.reply_text("**Kullanım:** /play ile aynı\n\n**Misal:**\n```/playlist Mary Jane - Mevsim Bahar\nFikri Karayel - Yol\nEypio - Dardayım```", quote=False)

    if chat_id not in db:
        db[chat_id] = {}

    if "call" not in db[chat_id]:
        return await message.reply_text("**Önce /joinvc !**")

    if "playlist" not in db[chat_id]:
        db[chat_id]["playlist"] = False

    if "running" in db[chat_id] and db[chat_id]["running"]:
        db[chat_id]["queue_breaker"] = 1

    db[chat_id]["playlist"] = True
    if "queue" not in db[chat_id]:
        db[chat_id]["queue"] = Queue()

    services = list(available_services.keys())

    for line in raw_playlist.split("\n"):
        if line.split()[0].lower() in services:
            service = line.split()[0].lower()
            song_name = " ".join(line.split()[1:])
        else:
            service = "youtube"
            song_name = line

        requested_by = message.from_user.mention
        await db[chat_id]["queue"].put(
            {
                "service": available_services[service],
                "requested_by": requested_by,
                "query": song_name,
                "message": message,
            }
        )

    if not redirected:
        db[chat_id]["running"] = True
        await message.reply_text(f"🎧 **{message.from_user.mention} tarafından Yeni Oynatma Listesi Başlatıldı..**")
        await start_queue(chat_id, message=message)

# Queue handler
async def start_queue(chat_id, message=None):
    global db
    while True:
        await db[chat_id]["call"].set_is_mute(True)
        if ("queue_breaker" in db[chat_id] and db[chat_id]["queue_breaker"] != 0 ):
            db[chat_id]["queue_breaker"] -= 1

            if db[chat_id]["queue_breaker"] == 0:
                with suppress(KeyError):
                    del db[chat_id]["queue_breaker"]
            break

        if db[chat_id]["queue"].empty():
            if "playlist" not in db[chat_id] or not db[chat_id]["playlist"]:
                db[chat_id]["running"] = False
                await db[chat_id]["call"].set_is_mute(False)
                break
            else:
                await playlist(Client, message, redirected=True)

        data = await db[chat_id]["queue"].get()
        service = data["service"]
        await service(data["requested_by"], data["query"], data["message"])