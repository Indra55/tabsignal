#!/usr/bin/env python3
"""Create Chrome Web Store images from TabSignal's existing brand and UI."""

from pathlib import Path
import io
import subprocess

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "assets"
W, H = 1280, 800
BG = (10, 12, 16)
WHITE = (244, 246, 249)
MUTED = (151, 161, 176)
BLUE = (59, 130, 246)
FONT = "/usr/share/fonts/OTF/AtkinsonHyperlegibleNext-Regular.otf"
MED = "/usr/share/fonts/OTF/AtkinsonHyperlegibleNext-Medium.otf"
BOLD = "/usr/share/fonts/OTF/AtkinsonHyperlegibleNext-Bold.otf"


def f(size, weight="reg"):
    return ImageFont.truetype({"reg": FONT, "med": MED, "bold": BOLD}[weight], size)


def logo(name, size):
    path = ROOT / "icons" / name
    if path.suffix == ".svg":
        data = subprocess.run(["convert", "-background", "none", str(path), "-resize", f"{size}x{size}", "png:-"], check=True, capture_output=True).stdout
        image = Image.open(io.BytesIO(data)).convert("RGBA")
    else:
        image = Image.open(path).convert("RGBA")
    image.thumbnail((size, size), Image.Resampling.LANCZOS)
    return image


LOGOS = {
    "TabSignal": logo("tabsignal.svg", 128),
    "ChatGPT": logo("chatgpt.svg", 64),
    "Gemini": logo("gemini.png", 64),
    "DeepSeek": logo("deepseek.svg", 64),
    "Grok": logo("grok.svg", 64),
}


def background(size=(W, H)):
    im = Image.new("RGB", size, BG)
    glow = Image.new("RGBA", size)
    d = ImageDraw.Draw(glow)
    w, h = size
    d.ellipse((w*.38, h*.03, w*1.12, h*.95), fill=(25, 73, 148, 34))
    glow = glow.filter(ImageFilter.GaussianBlur(max(size)*.12))
    return Image.alpha_composite(im.convert("RGBA"), glow)


def rr(d, box, radius, fill, outline=None, width=1):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def brand_header(im, eyebrow, title, subtitle):
    d = ImageDraw.Draw(im)
    d.text((84, 58), eyebrow.upper(), font=f(15,"bold"), fill=(132,166,219))
    d.text((84, 100), title, font=f(46,"bold"), fill=WHITE)
    d.text((84, 164), subtitle, font=f(20), fill=MUTED)


def export_store_icon():
    # CWS icon artwork is centered at 96x96 with 16px transparent margins.
    src = Image.open(ROOT / "icons" / "icon-128.png").convert("RGBA")
    mark = src.resize((96, 96), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (128, 128), (0,0,0,0))
    canvas.alpha_composite(mark, (16,16))
    canvas.save(OUT / "store-icon-128.png")
    canvas.save(ROOT / "icons" / "icon-128.png")


def screenshot_working():
    im = background(); d = ImageDraw.Draw(im)
    brand_header(im, "TabSignal · status at a glance", "Know when to come back.", "A quiet tab signal while your AI response is generating.")
    # Browser tabs with genuine service marks and the real grey working dot.
    rr(d,(120,300,1160,570),22,(18,21,27),(54,61,72),2)
    rr(d,(121,301,1159,363),20,(27,31,38))
    d.rectangle((121,340,1159,364),fill=(27,31,38))
    for i,c in enumerate(((245,99,91),(245,190,75),(87,196,112))):
        d.ellipse((148+i*22,325,160+i*22,337),fill=c)
    tabs=[("ChatGPT",True), ("Gemini",False), ("DeepSeek",False), ("Grok",False)]
    x=230
    for i,(name,active) in enumerate(tabs):
        tw=(222 if i==0 else 196)
        rr(d,(x,314,x+tw,356),10,(13,16,21) if active else (27,31,38))
        im.alpha_composite(LOGOS[name].resize((24,24),Image.Resampling.LANCZOS),(x+13,323))
        d.text((x+46,325),name,font=f(15,"med"),fill=(212,218,227) if active else (142,152,168))
        color=(161,169,181) if active else (59,68,80)
        d.ellipse((x+tw-28,330,x+tw-18,340),fill=color)
        x+=tw+8
    d.text((165,415),"Working",font=f(26,"med"),fill=WHITE)
    d.text((165,458),"A blinking grey dot means the response is still generating.",font=f(17),fill=MUTED)
    # Accurate status key.
    d.ellipse((166,520,178,532),fill=(161,169,181));d.text((190,515),"Working",font=f(15,"med"),fill=(205,211,220))
    d.ellipse((328,520,340,532),fill=BLUE);d.text((352,515),"Ready to read",font=f(15,"med"),fill=(205,211,220))
    im.convert("RGB").save(OUT/"screenshot-01-working.png",quality=95)


def draw_switch(d, x, y, on=True):
    color=(59,130,246) if on else (54,60,70)
    rr(d,(x,y,x+52,y+30),15,color)
    cx=x+35 if on else x+15
    d.ellipse((cx-10,y+5,cx+10,y+25),fill=(246,248,251))


def screenshot_controls():
    im=background(); d=ImageDraw.Draw(im)
    brand_header(im,"TabSignal · simple controls","Choose what gets a signal.","Toggle each service separately, or pause every indicator at once.")
    # Large but faithful rendering of the actual popup structure.
    card=(592,250,1050,660)
    rr(d,card,28,(17,20,26),(56,63,74),2)
    im.alpha_composite(LOGOS["TabSignal"].resize((46,46),Image.Resampling.LANCZOS),(624,278))
    d.text((684,280),"TabSignal",font=f(21,"bold"),fill=WHITE)
    d.text((684,309),"AI tab status",font=f(15),fill=MUTED)
    draw_switch(d,964,286,True)
    services=["ChatGPT","Gemini","DeepSeek","Grok"]
    positions=[(624,362),(850,362),(624,444),(850,444)]
    for name,(x,y) in zip(services,positions):
        rr(d,(x,y,x+198,y+65),15,(27,31,38),(55,62,73),1)
        im.alpha_composite(LOGOS[name].resize((34,34),Image.Resampling.LANCZOS),(x+17,y+15))
        draw_switch(d,x+128,y+17,True)
    d.line((624,539,1018,539),fill=(47,53,63),width=1)
    d.ellipse((633,568,645,580),fill=(161,169,181))
    d.text((659,559),"Working",font=f(15,"med"),fill=WHITE)
    d.text((659,582),"Blinking grey dot",font=f(12),fill=MUTED)
    d.ellipse((823,568,835,580),fill=BLUE)
    d.text((849,559),"Ready to read",font=f(15,"med"),fill=WHITE)
    d.text((849,582),"Blue until you return",font=f(12),fill=MUTED)
    d.text((624,625),"Settings saved locally",font=f(12),fill=(125,135,150))
    d.text((88,310),"Your tabs stay yours.",font=f(28,"med"),fill=WHITE)
    d.text((88,357),"Settings are stored on this device.",font=f(17),fill=MUTED)
    d.text((88,389),"No account or setup flow.",font=f(17),fill=MUTED)
    im.convert("RGB").save(OUT/"screenshot-02-controls.png",quality=95)


def screenshot_ready():
    im=background(); d=ImageDraw.Draw(im)
    brand_header(im,"TabSignal · when you’re away","Blue means it’s ready.","When generation stops in a background tab, the blue dot waits for you.")
    rr(d,(170,310,1110,500),24,(18,22,29),(56,64,77),2)
    rr(d,(194,330,1086,382),15,(28,33,41))
    im.alpha_composite(LOGOS["ChatGPT"].resize((28,28),Image.Resampling.LANCZOS),(213,342))
    d.text((254,345),"ChatGPT · your conversation",font=f(16,"med"),fill=(202,210,221))
    d.ellipse((1036,350,1050,364),fill=BLUE)
    d.text((230,421),"Your answer is ready",font=f(24,"med"),fill=WHITE)
    d.text((230,460),"The blue indicator clears when you return to the tab.",font=f(17),fill=MUTED)
    d.text((172,570),"TabSignal reads the response-control state on supported pages to detect generation.",font=f(16),fill=(174,184,199))
    d.text((172,605),"It doesn’t read conversation text or send page data anywhere.",font=f(16),fill=(174,184,199))
    im.convert("RGB").save(OUT/"screenshot-03-ready.png",quality=95)


def promo_tile(size, filename, marquee=False):
    w,h=size
    im=background(size); d=ImageDraw.Draw(im)
    scale=w/1280
    im.alpha_composite(LOGOS["TabSignal"].resize((int(68*scale),int(68*scale)),Image.Resampling.LANCZOS),(int(64*scale),int(63*scale)))
    d.text((int(150*scale),int(67*scale)),"TabSignal",font=f(max(18,int(28*scale)),"bold"),fill=WHITE)
    if marquee:
        d.text((int(76*scale),int(220*scale)),"Know when your AI is ready.",font=f(int(55*scale),"bold"),fill=WHITE)
        d.text((int(80*scale),int(310*scale)),"A quiet signal for the tabs you leave running.",font=f(int(22*scale)),fill=MUTED)
        labels=["ChatGPT","Gemini","DeepSeek","Grok"]
        x=int(82*scale); y=int(410*scale)
        for label in labels:
            rr(d,(x,y,x+int(170*scale),y+int(76*scale)),int(17*scale),(25,30,39),(60,69,83),max(1,int(scale)))
            im.alpha_composite(LOGOS[label].resize((int(38*scale),int(38*scale)),Image.Resampling.LANCZOS),(x+int(16*scale),y+int(19*scale)))
            d.text((x+int(62*scale),y+int(26*scale)),label,font=f(int(15*scale),"med"),fill=(225,230,238))
            x+=int(190*scale)
        d.ellipse((int(1130*scale),int(260*scale),int(1146*scale),int(276*scale)),fill=BLUE)
    else:
        d.text((int(62*scale),int(150*scale)),"Know when your",font=f(int(31*scale),"med"),fill=WHITE)
        d.text((int(62*scale),int(190*scale)),"AI is ready.",font=f(int(31*scale),"bold"),fill=WHITE)
        # Compact tab motif with the familiar blue ready indicator.
        rr(d,(int(303*scale),int(146*scale),int(402*scale),int(239*scale)),int(17*scale),(25,30,39),(63,74,91),1)
        im.alpha_composite(LOGOS["ChatGPT"].resize((int(48*scale),int(48*scale)),Image.Resampling.LANCZOS),(int(328*scale),int(166*scale)))
        d.ellipse((int(374*scale),int(214*scale),int(390*scale),int(230*scale)),fill=BLUE)
    im.convert("RGB").save(OUT/filename,quality=95)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    export_store_icon()
    screenshot_working();screenshot_controls();screenshot_ready()
    promo_tile((440,280),"promo-small-440x280.png")
    promo_tile((1400,560),"promo-marquee-1400x560.png",marquee=True)
    print("Created Chrome Web Store assets in",OUT)


if __name__=="__main__":
    main()
