# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

import asyncio
from youtubesearchpython.__future__ import VideosSearch
from json import dumps

async def get_youtube(query:str) -> dict:
    video_search = VideosSearch(query, limit = 1)
    video_result = await video_search.next()
    # print(dumps(video_result, indent = 2, ensure_ascii = False))

    result = {'id' : video_result['result'][0]['id'], 'title' : video_result['result'][0]['title'], 'duration' : video_result['result'][0]['duration'], 'views' : video_result['result'][0]['viewCount']['text'].replace(' views', ''), 'thumbnail' : video_result['result'][0]['thumbnails'][0]['url']}
    # print(dumps(result, indent = 2, ensure_ascii = False))

    return result

# m_loop = asyncio.get_event_loop()
# m_loop.run_until_complete(get_youtube('birini seviyorum'))

from pyrogram.types import Message
from Core import db
from Lib import time_to_seconds, generate_cover, transcode, pause_skip_watcher
from config import YT_MAX_MINUTES
import youtube_dl, os, functools

# Youtube
async def youtube(requested_by, query, message:Message):
    ydl_opts = {"format": "bestaudio", "quiet": True}
    mesaj = await message.reply_text(f"**YouTube'da `{query}` aranıyor.**", quote=False)

    try:
        result = await get_youtube(query)
    except Exception as hata:
        return await mesaj.edit(f"`{type(hata).__name__}` **| {hata}**")

    link      = f"https://youtube.com/watch?v={result['id']}"
    title     = result['title']
    chat_id   = message.chat.id
    thumbnail = result['thumbnail']
    duration  = result['duration']
    views     = result['views']

    if time_to_seconds(duration) >= YT_MAX_MINUTES * 60:
        return await mesaj.edit(f"**Bruh! Sadece {YT_MAX_MINUTES} Dakika içindeki şarkılar.**")

    await mesaj.edit("**Küçük Resim İşleniyor.**")
    cover = await generate_cover(requested_by, title, views, duration, thumbnail, chat_id)

    await mesaj.edit("**Müzik İndiriliyor..**")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict  = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
    except Exception as hata:
        return await mesaj.edit(f"⁉️ **Bir Hata Oluştu!**\n\n__{type(hata).__name__}__ | ```{hata}```")

    await mesaj.edit("**Kod Dönüştürülüyor..**")
    song = f"audio{chat_id}.webm"
    os.rename(audio_file, song)
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, functools.partial(transcode, song, chat_id))
    await mesaj.delete()

    caption = (
        f"🏷 **Başlık:** [{title[:45]}]({link})\n⏳ **Süre:** {duration}\n"
        + f"🎧 **İsteyen:** {message.from_user.mention}\n📡 **Platform:** YouTube"
    )

    global db
    db[chat_id]["currently"] = {"artist": None, "song": title, "query": query}

    mesaj = await message.reply_photo(photo=cover, caption=caption)
    os.remove(cover)

    duration = int(time_to_seconds(duration))
    await pause_skip_watcher(mesaj, duration, chat_id)
    await mesaj.delete()