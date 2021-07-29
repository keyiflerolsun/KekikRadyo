# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from pyrogram.types import Message
from Core import db
import asyncio

async def pause_skip_watcher(message:Message, duration:int, chat_id:int):
    try:
        chat_id = message.chat.id

        db[chat_id]["call"].set_is_mute(False)

        if "skipped" not in db[chat_id]:
            db[chat_id]["skipped"] = False
        if "paused" not in db[chat_id]:
            db[chat_id]["paused"] = False
        if "stopped" not in db[chat_id]:
            db[chat_id]["stopped"] = False
        if "replayed" not in db[chat_id]:
            db[chat_id]["replayed"] = False

        restart_while = False
        while True:
            for _ in range(duration * 10):
                if db[chat_id]["skipped"]:
                    db[chat_id]["skipped"] = False
                    return await message.delete()

                if db[chat_id]["paused"]:
                    while db[chat_id]["paused"]:
                        await asyncio.sleep(0.1)
                        continue

                if db[chat_id]["stopped"]:
                    restart_while = True
                    break

                if db[chat_id]["replayed"]:
                    restart_while = True
                    db[chat_id]["replayed"] = False
                    break

                if ("queue_breaker" in db[chat_id] and db[chat_id]["queue_breaker"] != 0):
                    break

                await asyncio.sleep(0.1)

            if not restart_while:
                break

            restart_while = False
            await asyncio.sleep(0.1)

        db[chat_id]["skipped"] = False
    except Exception:
        pass