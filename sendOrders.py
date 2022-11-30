import signal

import cv2

from EthernetAPI.client import Client
from EthernetAPI.message_types import RC_ORDER


if __name__ == "__main__":
    client = Client()
    client.connect("192.168.137.1", 60006)

    old_mask = signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGINT})

    # Throttle (0, 3-10), Steering (Duty % (6 - 9))
    orders = [(3, 7.5), (3, 7.5), (3, 7.7), (3, 7.8), (5, 6.5)]
    idx = 0

    while True:
        # Theoretical: message = f"{model.get_speed()}|{model.get_steering()}"
        message = f"{orders[idx][0]}|{orders[idx][1]}"
        client.send_message(RC_ORDER, message)

        idx += 1
        if idx > len(orders):
            break

        if signal.SIGINT in signal.sigpending():
            client.disconnect()
            break

    signal.pthread_sigmask(signal.SIG_SETMASK, old_mask)
