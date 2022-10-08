# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core import session
import ffmpeg, os, asyncio, aiofiles, functools

def transcode(filename: str, chat_id: str):
    ffmpeg.input(filename).output(
                  f"input{chat_id}.raw",
        format    = "s16le",
        acodec    = "pcm_s16le",
        ac        = 2,
        ar        = "48k",
        loglevel  = "error"
    ).overwrite_output().run()

    os.remove(filename)

# Download song
async def download_and_transcode_song(url, chat_id):
    song = f"{chat_id}.mp3"

    async with session.get(url) as resp:
        if resp.status == 200:
            file = await aiofiles.open(song, mode="wb")
            await file.write(await resp.read())
            await file.close()

    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, functools.partial(transcode, song, chat_id))