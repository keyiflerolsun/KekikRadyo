# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from pyrogram import Client, __version__
from aiohttp  import ClientSession

from config   import YETKILI, API_ID, API_HASH

SESSION_ADI = "KekikRadyo"
ROOT_ID     = YETKILI[0]

app     = Client(name=SESSION_ADI, api_id=API_ID, api_hash=API_HASH, plugins=dict(root="Commands"))
session = ClientSession()

themes  = ["kekik"]

global db
db = {}

from Kekik.cli import konsol, cikis_yap, hata_yakala

import os, sys

tum_eklentiler = [
    f"📂 {dosya.replace('.py','')}"
        for dosya in os.listdir("Commands")
            if dosya.endswith(".py") and not dosya.startswith("_")
]

def basarili(yazi:str):
   konsol.print(yazi, style="bold green", width=70, justify="center")

def baslangic():
    app.start()

    surum = f"{str(sys.version_info[0])}.{str(sys.version_info[1])}"
    konsol.print(f"[gold1]@{SESSION_ADI}[/] [yellow]:bird:[/] [bold red]Python: [/][i]{surum}[/]", width=70, justify="center")
    basarili(f"{SESSION_ADI} [magenta]v[/] [blue]{__version__}[/] [red]Pyrogram[/] tabanında [magenta]{len(tum_eklentiler)} eklentiyle[/] çalışıyor...\n")

    app.stop()