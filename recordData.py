import signal

import cv2

from EthernetAPI.client import Client
from EthernetAPI.message_types import RC_DATA

def cleanup(signum, stackframe):
    print("\nCleaning up...\n")
    #client.disconnect()
    exit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, cleanup)

    client = Client()
    client.connect("192.168.137.1", 60006)

    old_mask = signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGINT})

    while True:
        messages = client.read_messages()
        if messages:
            for mtype, message in messages:
                if mtype == RC_DATA:
                    throttle, steering = message.split("|")
                    print(f"{throttle}|{steering}")

        if signal.SIGINT in signal.sigpending():
            client.disconnect()
            break

        signal.pthread_sigmask(signal.SIG_SETMASK, old_mask)