# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Kekik.cli import cikis_yap, hata_yakala
from config    import API_ID, API_HASH, YETKILI
from pyrogram  import Client, filters

from pytgcalls                           import GroupCallFactory
from pytgcalls.implementation.group_call import GroupCall

client               = Client(name="KekikRadyo", api_id=API_ID, api_hash=API_HASH)
group_call_factory   = GroupCallFactory(client)
voice_chat:GroupCall = group_call_factory.get_group_call()

from pafy import new as yt_vid

@client.on_message(filters.command("oynat") & ~filters.private)
async def oynat_vc(client, message):
    if message.from_user.id not in YETKILI:
        await message.reply("__**root** değilmişsin kekkooo__", quote=True)
        return

    if len(message.command) <= 1:
        return await message.reply_text("**Kullanım:**\n\n`/oynat yt_vid https://www.youtube.com/watch?v=59Q_lhgGANc`", quote=False)

    match message.command[1]:
        case "yt_vid":
            YOUTUBE_URL = message.command[2]

            video     = yt_vid(YOUTUBE_URL)
            video_url = video.getbest().url

            await voice_chat.stop()
            await voice_chat.join(message.chat.id)
            await voice_chat.start_video(video_url)
        case "yt_mp3":
            YOUTUBE_URL = message.command[2]

            video     = yt_vid(YOUTUBE_URL)
            video_url = video.getbest().url

            await voice_chat.stop()
            await voice_chat.join(message.chat.id)
            await voice_chat.start_audio(video_url)
        case "mp4":
            await voice_chat.stop()
            await voice_chat.join(message.chat.id)
            await voice_chat.start_video(message.command[2])
        case "mp3":
            await voice_chat.stop()
            await voice_chat.join(message.chat.id)
            await voice_chat.start_audio(message.command[2])
        case _:
            return await message.reply_text("__oynat__ » `yt_vid` `-` `yt_mp3` `-` `mp3` `-` `mp4`", quote=False)

if __name__ == "__main__":
    try:
        client.run()
        cikis_yap(False)
    except Exception as hata:
        hata_yakala(hata)