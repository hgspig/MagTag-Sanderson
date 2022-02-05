import urllib.request
import re

site = "https://www.brandonsanderson.com/"
hdr = {
    # "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    # "accept-language": "en-US,en;q=0.9",
    # "cache-control": "max-age=0",
    # "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"97\", \"Chromium\";v=\"97\"",
    # "sec-ch-ua-mobile": "?0",
    # "sec-ch-ua-platform": "\"Windows\"",
    # "sec-fetch-dest": "document",
    # "sec-fetch-mode": "navigate",
    # "sec-fetch-site": "same-origin",
    # "sec-fetch-user": "?1",
    # "upgrade-insecure-requests": "1",
    # "Referer": "https://www.brandonsanderson.com/",
    # "Referrer-Policy": "origin-when-cross-origin"
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
}
req = urllib.request.Request(site, headers=hdr)

try:
    page = urllib.request.urlopen(req)
    content = page.read().decode('utf8')
    # print(content)

    # >Cytonic Final Proofread <span class="vc_label_units">100%<

    m = re.findall('>\s*([^<]+?)\s*<span\s+class="vc_label_units">\s*(\d+)%\s*<', content)

    print(m)

except urllib.error.HTTPError as e:
    print(e.fp.read())

