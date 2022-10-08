# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from pyrogram import Client, filters
from config   import YETKILI

@Client.on_message(filters.command("repo") & ~filters.private)
async def repo(client, message):
    if message.from_user.id not in YETKILI:
        await message.reply("__admin değilmişsin kekkooo__", quote=True)
        return

    await message.reply_text("**[Github](https://github.com/keyiflerolsun/KekikRadyo)** | **[KekikAkademi](t.me/KekikAkademi)**", quote=False)