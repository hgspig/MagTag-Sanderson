
from adafruit_magtag.magtag import MagTag
from adafruit_progressbar.progressbar import ProgressBar
import rtc
import terminalio
import re

magtag = MagTag()
magtag.network.connect()

# set progress bar width and height relative to board's display
BAR_WIDTH = magtag.graphics.display.width // 2 - 20
BAR_HEIGHT = 15

BAR_X = magtag.graphics.display.width // 2 + 10

percentages = []

site = "https://www.brandonsanderson.com/"
hdr = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
}
try:
    response = magtag.network.fetch(site, headers=hdr )

    r = re.compile('>\s*([^<]+?)\s*<span\s+class="vc_label_units">\s*(\d+)%\s*<')
    content = ""
    found = False

    for chunk in response.iter_content(1024):
        if not chunk:
            break

        content += chunk.decode('utf-8')
        if len(content) < 16384:
            continue

        if found and r.search(content) == None:
            break

        while True:
            m = r.search(content)

            if m == None:
                content = content[1024:]
                break

            # print("matches",
            #     # len(response.text), m, m.span(0), m.start(0), m.end(0),
            #     m.groups()[0], " <<<>>> ",
            #     m.groups()[1], " <<<>>> ",
            #     # response.text[m.start(0):m.end(0)], " <<<>>> ",
            #     # response.text[m.start(1):m.end(1)], " <<<>>> ",
            #     # response.text[m.start(2):m.end(2)]
            # )

            found = True
            percentages.append((m.groups()[0], m.groups()[1]))
            content = content[m.end(0):]

except RuntimeError as e:
    print(e)

# percentages = [
#     ('Cytonic Final Proofread', '78'), 
#     ('Wax & Wayne Book 4 (Mistborn 7) Draft 2.0', '48'), 
#     ('Skyward Four Draft 1.0', '20'), 
#     ('Evershore (Skyward Novella 3) Final Draft', '88')
# ]

try:
    magtag.add_text(
        text_font="/fonts/leaguespartan18.bdf",        # text_font="/fonts/epilogue18.bdf",
        text_position=(
            10, # (magtag.graphics.display.width // 2) - 1,
            15,
        ),
        line_spacing=0.9,
        text_scale=1,
        text_anchor_point=(0, 0.5),
        is_data=False,
    )
    magtag.set_text("Brandon Sanderson", auto_refresh=False, index=0)
    LINE_HEIGHT=23
    LINE_X_SHIFT=37
    for i in range(min(len(percentages), 4)):
        (title, percent) = percentages[i]
        percent = int(percent)

        # Create a new progress_bar object at (x, y)
        
        progress_bar = ProgressBar(
            BAR_X, LINE_HEIGHT*i+LINE_X_SHIFT, BAR_WIDTH, BAR_HEIGHT, 1.0, bar_color=0xffffff, outline_color=0x000000
        )
        progress_bar.fill = 0x999999

        magtag.graphics.splash.append(progress_bar)

        progress_bar.progress = percent / 100
        print(title, percent)
        magtag.add_text(
            text_font = terminalio.FONT, 
            # text_font="/fonts/epilogue18.bdf",
            text_position=(
                10, # (magtag.graphics.display.width // 2) - 1,
                LINE_HEIGHT*i+LINE_X_SHIFT+5,
            ),
            line_spacing=0.9,
            text_scale=1,
            text_wrap=25,
            text_maxlen=50,
            text_anchor_point=(0, 0.5),
            is_data=False,
        )
        
        magtag.add_text(
            text_font = terminalio.FONT, 
            # text_font="/fonts/epilogue18.bdf",
            text_position=(
                (magtag.graphics.display.width // 2) + BAR_WIDTH//2 +20,
                LINE_HEIGHT*i+LINE_X_SHIFT+7,
            ),
            line_spacing=0.9,
            text_scale=1,
            text_maxlen=10,
            text_color = 0x000000,
            text_anchor_point=(0.5, 0.5),
            is_data=False,
        )
        magtag.set_text( title, auto_refresh=False, index = i*2+1)
        magtag.set_text( "{}%".format(percent), auto_refresh=False, index = i*2 +2)
    
    # Create the QR code
    url = "https://www.brandonsanderson.com/"
    magtag.graphics.qrcode(url, qr_size=1, x=(magtag.graphics.display.width-35), y=3)

    magtag.refresh()
    # magtag.exit_and_deep_sleep(24 * 60 * 60)  # one day
    magtag.exit_and_deep_sleep(24*60*60)

except (ValueError, RuntimeError) as e:
    print("Some error occurred, retrying after 1 minute! -", e)
    magtag.exit_and_deep_sleep(60)  # one  minute
