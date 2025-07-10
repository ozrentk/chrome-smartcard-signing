import sys
import struct
import json
from smartcard.System import readers
from smartcard.util import toHexString

def get_card_atr():
    rdrs = readers()
    if not rdrs:
        return { "status": "no_readers" }

    try:
        connection = rdrs[0].createConnection()
        connection.connect()
        atr = toHexString(connection.getATR())
        return { "status": "ok", "atr": atr }
    except Exception as e:
        return { "status": "no_card", "error": str(e) }

def read_message():
    raw_length = sys.stdin.buffer.read(4)
    if len(raw_length) == 0:
        return None
    message_length = struct.unpack('<I', raw_length)[0]
    message = sys.stdin.buffer.read(message_length).decode('utf-8')
    return json.loads(message)

def send_message(message):
    encoded = json.dumps(message).encode('utf-8')
    sys.stdout.buffer.write(struct.pack('<I', len(encoded)))
    sys.stdout.buffer.write(encoded)
    sys.stdout.buffer.flush()

if __name__ == "__main__":
    # with open("host.log", "a", encoding="utf-8") as log:
    #     log.write("Started...\n")

    while True:
        try:
            received = read_message()
            if received.get("action") == "get_atr":
                response = get_card_atr()
            # elif received.get("action") == "get_somethig_else":
            #     response = get_somethig_else()
            else:
                response = { "status": "unknown_action" }
            send_message(response)
        except Exception as e:
            send_message({ "status": "error", "message": str(e) })
            break
