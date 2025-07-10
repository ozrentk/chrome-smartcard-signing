# Project: chrome-smartcard-signing
POC for signing documents using certificate available on smarcard and chrome extension

# Download SWIG for Windows

Use: https://sourceforge.net/projects/swig/files/swigwin/swigwin-4.3.1/
Download locally and unpack it to e.g. C:\Tools\swigwin-4.3.1
Add to PATH; like... `System > Environment Variables > User PATH`
Restart VS Code (unfortunately the easiesat way, otherwise mess with persistent sessions).

# Create virtual environment

This setup explicitly avoids the Rust toolchain. Rust toolchain is required for `cryptography>=42`.
To use newer versions (e.g. Python >= 3.12 and `cryptography>=42`), you'll need Rust and a working build environment.

To install without compiling, I use Python 3.11 and prefer prebuilt binary wheels (`--prefer-binary`).
If you wish to build from source, remove the `--prefer-binary` flag.

```cmd
cd native-host
py -3.11 -m venv venv311
.\venv311\Scripts\activate
python.exe -m pip install --upgrade pip

pip install --prefer-binary -r requirements.txt
```

As a simple test, you can run `card.py`.
The real deal is `card_host.py`, which is unfortunately a script, so we need to embed it into an executable cmd, like `card_host.cmd`.
The `card_host.py` is easily extendable, see `__main__`, ifelifelif...

You can test the `card_host.py`, just `cd` to `native-host` and execute:

    test_card_host.ps1

# Register native host

Open `register-host-win.reg` and fix the path to the `hr.toiletdoc.signer.json` manifest file.
Then execute `register-host-win.reg`, or add the key to registry manually if you want to be 100% sure of what you're doing.

NOTE: I'm not sure if it will work without escaping the backslashes.

# Load Chrome extension in developer mode

Do the following:
- Open Chrome, then URL chrome://extensions
- Turn on Developer mode
- Click `Load unpacked`
- Select the chrome-extension folder from the project
    - You get a new Chrome Extension ID
- Update `allowed_origins` in hr.toiletdoc.signer.json with your brand new Chrome Extension ID
- Pin the new "Smart Card ATR Reader" extension in chrome

# Test

Do the following
- Click "Smart Card ATR Reader" Chrome extension icon
- Click `Read ATR` button
- Observe the response message

# If you'd like to use this as a development toy

When opening the project in VS Code, use...

```cmd
cd native-host
.\venv311\Scripts\activate
```

Ideas:
- add new commands
- detect which card is it - see https://smartcard-atr.apdu.fr/
- hack some APDU commands and brick your card reader: https://www.blackhat.com/presentations/bh-usa-08/Buetler/BH_US_08_Buetler_SmartCard_APDU_Analysis_V1_0_2.pdf
- or, according to ChatGPT you can try the following, and I'm NOT RESPONSIBLE if you damage either your reader or your card:
    - SELECT Master File (MF):                 00 A4 00 0C 02 3F 00
    - SELECT Dedicated File (DF) PKCS#15:      00 A4 00 0C 02 50 15
    - SELECT Certificate Directory File (CDF): 00 A4 00 0C 02 4F 03
    - READ BINARY data (CDF content):          00 B0 00 00 FF... 00 B0 01 FE FF...
    - PARSE CDF, check where is a certificate; CDF contains ASN.1 structures that state FID of the certificate (like 4401, 4402, 4403), type (authentication, signature, CA...), offset, length etc.
    - SELECT certificate FILE (like 4402):     00 A4 00 0C 02 44 02
    - READ BINARY (certificate):               00 B0 00 00 FF... read segments until you get X.509 certificate in DER format
- add support for signing PDF/XML/plaintext with card's private key
- use Get Challenge / Verify PIN
