"""Builds the two fictional demo exports in demo/ (German Android, English iPhone)."""
import os, subprocess, zipfile, math, random, tempfile
from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'demo'))
os.makedirs(OUT, exist_ok=True)
TMP = tempfile.mkdtemp()
random.seed(7)

def grad(w, h, top, bottom):
    im = Image.new('RGB', (w, h))
    d = ImageDraw.Draw(im)
    for y in range(h):
        t = y / (h - 1)
        d.line([(0, y), (w, y)], fill=tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return im

def sunset(path):
    w, h = 900, 1200
    im = grad(w, h, (255, 160, 90), (110, 60, 140))
    d = ImageDraw.Draw(im)
    d.ellipse([w/2-130, 430, w/2+130, 690], fill=(255, 220, 140))
    water = grad(w, 520, (70, 50, 120), (30, 30, 70))
    im.paste(water, (0, 680))
    for i in range(26):
        y = 700 + i * 18; half = 150 - i * 5
        if half > 10: d.line([(w/2-half, y), (w/2+half, y)], fill=(255, 200, 130), width=5)
    d.polygon([(0, 690), (180, 560), (330, 640), (520, 520), (720, 630), (900, 560), (900, 690)], fill=(60, 35, 80))
    im.filter(ImageFilter.SMOOTH).save(path, quality=88)

def mountains(path):
    w, h = 1200, 900
    im = grad(w, h, (120, 180, 235), (220, 235, 250))
    d = ImageDraw.Draw(im)
    d.ellipse([930, 90, 1030, 190], fill=(255, 250, 225))
    for base, col, peaks in [(900, (95, 115, 140), [(0, 520), (260, 260), (520, 560), (760, 220), (1200, 600)]),
                             (900, (60, 90, 80), [(0, 640), (300, 430), (600, 680), (900, 400), (1200, 700)]),
                             (900, (40, 70, 55), [(0, 760), (400, 600), (800, 800), (1000, 660), (1200, 780)])]:
        d.polygon([(0, base)] + peaks + [(1200, base)], fill=col)
    for (x, y) in [(260, 260), (760, 220)]:
        d.polygon([(x, y), (x - 60, y + 70), (x - 20, y + 55), (x + 10, y + 80), (x + 55, y + 62)], fill=(250, 250, 255))
    im.save(path, quality=88)

def pancakes(path):
    w, h = 1000, 1000
    im = grad(w, h, (250, 236, 214), (236, 214, 186))
    d = ImageDraw.Draw(im)
    d.ellipse([140, 520, 860, 860], fill=(255, 255, 255), outline=(220, 210, 200), width=6)
    for i in range(6):
        y = 640 - i * 55
        d.ellipse([260, y - 40, 740, y + 60], fill=(205, 140, 70))
        d.ellipse([260, y - 50, 740, y + 45], fill=(232, 175, 95))
    d.polygon([(470, 330), (540, 330), (560, 420), (450, 420)], fill=(255, 225, 120))
    for _ in range(14):
        x, y = random.randint(300, 700), random.randint(260, 380)
        d.ellipse([x, y, x + 34, y + 34], fill=random.choice([(70, 60, 150), (180, 30, 60)]))
    im.save(path, quality=88)

def sticker(path):
    im = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([46, 46, 466, 466], fill=(255, 205, 60, 255), outline=(255, 255, 255, 255), width=18)
    d.ellipse([160, 170, 210, 250], fill=(60, 40, 20, 255)); d.ellipse([302, 170, 352, 250], fill=(60, 40, 20, 255))
    d.arc([150, 210, 362, 390], 20, 160, fill=(60, 40, 20, 255), width=22)
    im.save(path, 'WEBP')

def voice(path, seed, secs):
    rnd = random.Random(seed)
    notes = [rnd.choice([262, 294, 330, 392, 440, 523]) for _ in range(int(secs * 2))]
    expr = '+'.join(f"0.3*sin(2*PI*{f}*t)*between(t,{i*0.5},{i*0.5+0.45})" for i, f in enumerate(notes))
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'lavfi', '-i', f"aevalsrc='{expr}':s=48000:d={secs}",
                    '-c:a', 'libopus', '-b:a', '24k', '-ac', '1', path], check=True)

def video(path):
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'lavfi', '-i', 'mandelbrot=size=640x360:rate=24', '-t', '4',
                    '-pix_fmt', 'yuv420p', '-c:v', 'libx264', '-preset', 'veryfast', '-movflags', '+faststart', path], check=True)

def pdf(path, title):
    im = Image.new('RGB', (1240, 1754), 'white'); d = ImageDraw.Draw(im)
    d.rectangle([100, 100, 1140, 220], fill=(0, 128, 105))
    for i in range(18): d.rectangle([100, 300 + i * 60, 100 + random.randint(500, 1040), 320 + i * 60], fill=(210, 210, 210))
    im.save(path, 'PDF', title=title)

def build(zip_name, txt_name, text, files):
    with zipfile.ZipFile(os.path.join(OUT, zip_name), 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr(txt_name, text)
        for arc, src in files:
            z.write(src, arc, compress_type=zipfile.ZIP_STORED if arc.endswith(('.jpg', '.mp4', '.opus', '.webp')) else zipfile.ZIP_DEFLATED)

T = lambda n: os.path.join(TMP, n)
sunset(T('sunset.jpg')); mountains(T('mountains.jpg')); pancakes(T('pancakes.jpg')); sticker(T('sticker.webp')); video(T('clip.mp4'))
for i, s in enumerate([4, 7, 3, 9, 5]): voice(T(f'v{i}.opus'), i, s)
pdf(T('plan.pdf'), 'Reiseplan'); pdf(T('itinerary.pdf'), 'Itinerary')

# ---- German, Android ----
de = """08.06.24, 18:02 - Nachrichten und Anrufe sind Ende-zu-Ende-verschlüsselt. Niemand außerhalb dieses Chats kann sie lesen oder anhören.
08.06.24, 18:02 - Lena: Hey Alex! Steht das Wochenende am See noch? 🏕️
08.06.24, 18:05 - Alex: Auf jeden Fall! Ich bring das Zelt mit
08.06.24, 18:05 - Alex: Und *Pfannkuchen* zum Frühstück 😄
08.06.24, 18:09 - Lena: ‎PTT-20240608-WA0004.opus (Datei angehängt)
08.06.24, 18:12 - Alex: ‎PTT-20240608-WA0005.opus (Datei angehängt)
08.06.24, 18:13 - Lena: Perfekt. Ich schick dir gleich den Plan
08.06.24, 18:14 - Lena: ‎Reiseplan.pdf (Datei angehängt)
Reiseplan.pdf
14.06.24, 07:41 - Alex: Bin unterwegs! Abfahrt 8:15
14.06.24, 07:42 - Lena: ‎STK-20240614-WA0002.webp (Datei angehängt)
14.06.24, 21:03 - Lena: ‎IMG-20240614-WA0011.jpg (Datei angehängt)
Was für ein Sonnenuntergang!
14.06.24, 21:04 - Alex: Wow 😍
14.06.24, 21:04 - Alex: <Medien ausgeschlossen>
14.06.24, 21:06 - Lena: Das Foto von dir ist leider verloren gegangen, schick's nochmal?
15.06.24, 09:30 - Alex: ‎IMG-20240615-WA0003.jpg (Datei angehängt)
Frühstück ist fertig ☕
15.06.24, 09:31 - Lena: Komme! Noch 5 Minuten
15.06.24, 09:31 - Lena: Diese Nachricht wurde gelöscht.
15.06.24, 14:20 - Alex: ‎VID-20240615-WA0007.mp4 (Datei angehängt)
15.06.24, 14:22 - Lena: ‎PTT-20240615-WA0008.opus (Datei angehängt)
16.06.24, 19:45 - Lena: Danke für das tolle Wochenende!
Nächstes Mal in die Berge?
16.06.24, 19:50 - Alex: ‎IMG-20240616-WA0014.jpg (Datei angehängt)
So in etwa? ⛰️ <Diese Nachricht wurde bearbeitet>
16.06.24, 19:51 - Lena: Genau so 🙌
16.06.24, 19:52 - Lena: Wetter: https://www.dwd.de
"""
build('WhatsApp-Chat mit Lena.zip', 'WhatsApp-Chat mit Lena.txt', de, [
    ('PTT-20240608-WA0004.opus', T('v0.opus')), ('PTT-20240608-WA0005.opus', T('v1.opus')), ('Reiseplan.pdf', T('plan.pdf')),
    ('STK-20240614-WA0002.webp', T('sticker.webp')), ('IMG-20240614-WA0011.jpg', T('sunset.jpg')), ('IMG-20240615-WA0003.jpg', T('pancakes.jpg')),
    ('VID-20240615-WA0007.mp4', T('clip.mp4')), ('PTT-20240615-WA0008.opus', T('v2.opus')), ('IMG-20240616-WA0014.jpg', T('mountains.jpg'))])

# ---- English, iPhone (US format, AM/PM) ----
N = ' '
def L(d, t, ap, who, msg): return f"[{d}, {t}{N}{ap}] {who}: {msg}"
en = '\n'.join([
 L('6/8/24', '6:02:11', 'PM', 'Sam', '‎Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them.'),
 L('6/8/24', '6:02:11', 'PM', 'Sam', 'Hey Jordan! Still on for the lake weekend? 🏕️'),
 L('6/8/24', '6:05:40', 'PM', 'Jordan', 'Absolutely! I’ll bring the tent'),
 L('6/8/24', '6:05:52', 'PM', 'Jordan', 'And _pancakes_ for breakfast 😄'),
 L('6/8/24', '6:09:03', 'PM', 'Sam', '‎<attached: 00000005-AUDIO-2024-06-08-18-09-03.opus>'),
 L('6/8/24', '6:12:20', 'PM', 'Jordan', '‎<attached: 00000006-AUDIO-2024-06-08-18-12-20.opus>'),
 L('6/8/24', '6:14:31', 'PM', 'Sam', 'Itinerary.pdf • 1 page ‎<attached: 00000007-Itinerary.pdf>'),
 L('6/14/24', '7:41:09', 'AM', 'Jordan', 'On my way! Leaving at 8:15'),
 L('6/14/24', '7:42:00', 'AM', 'Sam', '‎<attached: 00000009-STICKER-2024-06-14-07-42-00.webp>'),
 L('6/14/24', '9:03:44', 'PM', 'Sam', '‎<attached: 00000010-PHOTO-2024-06-14-21-03-44.jpg>'),
 L('6/14/24', '9:03:50', 'PM', 'Sam', 'What a sunset!'),
 L('6/14/24', '9:04:02', 'PM', 'Jordan', 'Wow 😍'),
 L('6/14/24', '9:04:30', 'PM', 'Jordan', '‎image omitted'),
 L('6/15/24', '9:30:12', 'AM', 'Jordan', '‎<attached: 00000013-PHOTO-2024-06-15-09-30-12.jpg>'),
 L('6/15/24', '9:31:00', 'AM', 'Sam', 'Coming! 5 more minutes'),
 L('6/15/24', '9:31:40', 'AM', 'Sam', '‎This message was deleted.'),
 L('6/15/24', '2:20:15', 'PM', 'Jordan', '‎<attached: 00000016-VIDEO-2024-06-15-14-20-15.mp4>'),
 L('6/15/24', '2:22:05', 'PM', 'Sam', '‎<attached: 00000017-AUDIO-2024-06-15-14-22-05.opus>'),
 L('6/16/24', '7:45:00', 'PM', 'Sam', 'Thanks for a great weekend!\nMountains next time?'),
 L('6/16/24', '7:50:10', 'PM', 'Jordan', '‎<attached: 00000020-PHOTO-2024-06-16-19-50-10.jpg>'),
 L('6/16/24', '7:50:30', 'PM', 'Jordan', 'Something like this? ⛰️ <This message was edited>'),
 L('6/16/24', '7:51:02', 'PM', 'Sam', 'Exactly 🙌'),
 L('6/16/24', '7:52:40', 'PM', 'Sam', 'Forecast: https://www.weather.gov'),
]) + '\n'
build('WhatsApp Chat - Sam.zip', '_chat.txt', en, [
    ('00000005-AUDIO-2024-06-08-18-09-03.opus', T('v3.opus')), ('00000006-AUDIO-2024-06-08-18-12-20.opus', T('v1.opus')), ('00000007-Itinerary.pdf', T('itinerary.pdf')),
    ('00000009-STICKER-2024-06-14-07-42-00.webp', T('sticker.webp')), ('00000010-PHOTO-2024-06-14-21-03-44.jpg', T('sunset.jpg')),
    ('00000013-PHOTO-2024-06-15-09-30-12.jpg', T('pancakes.jpg')), ('00000016-VIDEO-2024-06-15-14-20-15.mp4', T('clip.mp4')),
    ('00000017-AUDIO-2024-06-15-14-22-05.opus', T('v4.opus')), ('00000020-PHOTO-2024-06-16-19-50-10.jpg', T('mountains.jpg'))])
print('demo written to', OUT, os.listdir(OUT))
