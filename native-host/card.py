from smartcard.System import readers
from smartcard.util import toHexString

def print_readers():
    rdrs = readers()
    if not rdrs:
        print("No available readers found")
        exit()

    for idx, reader in enumerate(rdrs):
        print(f"[{idx}] {reader}")

def print_card_atr(reader_idx):
    rdrs = readers()
    reader = rdrs[reader_idx]
    connection = reader.createConnection()

    try:
        connection.connect()
        atr = connection.getATR()
        print(f"Card inserted. ATR: {toHexString(atr)}")
    except Exception as e:
        print(f"No card inserted or no response from reader.\nDetails: {e}")

print_readers()
print_card_atr(0)
