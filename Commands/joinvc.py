# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core     import db, ROOT_ID
from pyrogram import Client, filters
from config   import DEFAULT_SERVICE

from os                                         import popen
from pytgcalls                                  import GroupCallFactory
from pytgcalls.implementation                   import GroupCallFile
from pyrogram.raw.functions.phone               import CreateGroupCall
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired

@Client.on_message(filters.command("joinvc") & ~filters.private)
async def joinvc(client, message):
    if message.from_user.id != ROOT_ID:
        await message.reply("__**root** değilmişsin kekkooo__", quote=True)
        return

    global db
    chat_id = message.chat.id
    if chat_id not in db:
        db[chat_id] = {}

    if "call" in db[chat_id]:
        return await message.reply_text("**Bot Zaten Sesli Sohbette**")

    group_call_factory = GroupCallFactory(client)
    popen(f"cp etc/sample_input.raw input{chat_id}.raw")
    vc:GroupCallFile = group_call_factory.get_file_group_call(f"input{chat_id}.raw")

    db[chat_id]["call"] = vc

    try:
        await db[chat_id]["call"].start(chat_id)
    except Exception:
        peer = await client.resolve_peer(chat_id)
        print(peer)
        start_voice_chat = CreateGroupCall(peer=peer, random_id=client.rnd_id() // 9000000000),
        try:
            await client.send(start_voice_chat)
            await db[chat_id]["call"].start(chat_id)
        except ChatAdminRequired:
            del db[chat_id]["call"]
            return await message.reply_text("Mesaj silme ve sesli sohbet yönetme izniyle beni yönetici yap")

    await message.reply_text(f"**Sesli Sohbet'e katıldı.**\n\n__Varsayılan Servis :__ `{DEFAULT_SERVICE}`")