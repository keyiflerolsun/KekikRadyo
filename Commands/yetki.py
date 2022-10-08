# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from pyrogram import Client, filters

from Core     import ROOT_ID
from config   import YETKILI

@Client.on_message(filters.command("yetki") & ~filters.private)
async def yetki(client, message):
    if message.from_user.id != ROOT_ID:
        await message.reply("__**root** değilmişsin kekkooo__", quote=True)
        return

    if not message.reply_to_message:
        return await message.reply("**Yalnızca Alntılanan Mesajlarda Çalışır..**", quote=True)

    if (len(message.command) == 1) or (message.command[1] not in ['ver', 'al']):
        return await message.reply("**`ver` veya `al` ile kullanılır..**", quote=True)

    yetki_id = message.reply_to_message.from_user.id

    global YETKILI
    if (message.command[1] == 'ver'):
        YETKILI.append(yetki_id)
        await message.reply_text(f"**{message.reply_to_message.from_user.mention} adlı kişiye Yetki Verildi..**")
    elif message.command[1] == 'al':
        YETKILI.remove(yetki_id)
        await message.reply_text(f"**{message.reply_to_message.from_user.mention} adlı kişinin Yetkisi Alındı..**")