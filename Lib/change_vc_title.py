# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core import app
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.phone import EditGroupCallTitle

async def change_vc_title(title: str, chat_id: int):
    peer = await app.resolve_peer(chat_id)
    chat = await app.send(GetFullChannel(channel=peer))
    data = EditGroupCallTitle(call=chat.full_chat.call, title=title)
    await app.send(data)