# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from pyrogram import Client, filters
from config   import YETKILI

@Client.on_message(filters.command("radyo") & ~filters.private)
async def help(client, message):
    if message.from_user.id not in YETKILI:
        await message.reply("__admin değilmişsin kekkooo__", quote=True)
        return

    await message.reply_text("""**@KekikAkademi Kıraathanesi Radyocu Teyzesi**

<u>🔒 **Yetkili Komutları __(5)__;**</u>
**/radyo** __Yardım Menüsünü (Burayı Açar)__
**/play** __`Şarkı Adı` veya `Alıntılanan Şarkı Dosyası`nı Çalar__
**/kuyruk** __Çalma Kuyruğunu Gösterir (`liste` ekiyle kullanıldığında playlist'e atılabilir biçimde gösterir)__
**/replay** __Çalan Şarkıyı Tekrarlar__
**/repo** __Github Projesini Gösterir__

<u>🔑 **Root Komutları __(13)__;**</u>
**/joinvc** __Sesli Sohbete Katılır__
**/leavevc** __Sesli Sohbetten Çıkar__
**/listvc** __Dahil Olunan Sesli Sohbetleri Listeler__
**/yetki** __`ver` veya `al` alıntılanan mesaj ile hedef kişiye DJ yetkisi verir__
**/theme** __Yürütülen Temayı Değiştirir__
**/playlist** __Oynatma Listesini Oluşturur__
**/temizle** __Sıra Listesini ve Çalma Listesini Temizler__
**/skip** __Çalmakta olan Müziği Atlar__
**/volume** __`[1-200]` Sesi Ayarlar__
**/dur** __Müziği Durdur__
**/basla** __Son Müziği Çal__
**/pause** __Müziği Duraklat__
**/resume** __Müziği Sürdür__
""", quote=False)