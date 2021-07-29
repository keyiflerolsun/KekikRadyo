# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core import db, themes

def get_theme(chat_id) -> str:
    global db
    if chat_id not in db:
        db[chat_id] = {}

    if "theme" not in db[chat_id]:
        db[chat_id]["theme"] = themes[0]

    return db[chat_id]["theme"]

def change_theme(name: str, chat_id):
    if chat_id not in db:
        db[chat_id] = {}

    if "theme" not in db[chat_id]:
        db[chat_id]["theme"] = themes[0]

    db[chat_id]["theme"] = name