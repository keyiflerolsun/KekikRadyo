# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Core import session, app
import aiofiles, os, re
from PIL import Image, ImageDraw, ImageFont

from Lib.theme import get_theme
from Lib.change_vc_title import change_vc_title

def remove_html_tags(text):
    pattern = re.compile(r'<.*?>')
    return pattern.sub('', text)

# Change image size
def change_image_size(max_width: int, max_height: int, image):
    width_ratio  = max_width / image.size[0]
    height_ratio = max_height / image.size[1]

    new_width  = int(width_ratio * image.size[0])
    new_height = int(height_ratio * image.size[1])

    return image.resize((new_width, new_height))


# Generate cover for youtube
async def generate_cover(requested_by, title, views_or_artist, duration, thumbnail, chat_id):
    async with session.get(thumbnail) as resp:
        if resp.status == 200:
            file = await aiofiles.open(f"background{chat_id}.png", mode="wb")
            await file.write(await resp.read())
            await file.close()

    background = f"./background{chat_id}.png"
    final      = f"final{chat_id}.png"
    temp       = f"temp{chat_id}.png"

    music_pic      = Image.open(background)
    foreground_pic = Image.open(f"etc/foreground_{get_theme(chat_id)}.png")

    resize_music_pic      = change_image_size(1280, 720, music_pic)
    resize_foreground_pic = change_image_size(1280, 720, foreground_pic)

    rgb_music_pic      = resize_music_pic.convert("RGBA")
    rgb_foreground_pic = resize_foreground_pic.convert("RGBA")

    Image.alpha_composite(rgb_music_pic, rgb_foreground_pic).save(temp)

    after_text = Image.open(temp)
    draw = ImageDraw.Draw(after_text)
    font = ImageFont.truetype("etc/font.otf", 32)

    draw.text((300, 550), f"Başlık  : {title}",                          (255, 255, 255), font=font)
    draw.text((300, 590), f"Süre    : {duration}",                       (255, 255, 255), font=font)
    draw.text((300, 630), f"İzlenme  : {views_or_artist}",                (255, 255, 255), font=font)
    draw.text((300, 670), f"İsteyen   : {remove_html_tags(requested_by)}", (255, 255, 255), font=font)

    after_text.save(final)
    os.remove(temp)
    os.remove(background)

    try:
        await change_vc_title(title, chat_id)
    except Exception:
        await app.send_message(chat_id, text="[HATA]: VC BAŞLIĞI DÜZENLENMEDİ, BENİ YÖNETİCİ YAPIN.")

    return final