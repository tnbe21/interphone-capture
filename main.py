import numpy as np
from slackapp import SlackApp
from sound_capture import create_spectrum


def main():
    """1. USBマイクから2s単位で音を拾ってwavを変数に保持しFFT
    2. 650-665Hz間と850-865Hz間で一定振幅以上の周波数があれば
    インターホンが鳴っているとみなす
    3. 直近の通知から一定秒数経っている場合slackに通知
    """
    record_sec = 2

    slack_app = SlackApp()
    while True:
        f_list, fft_data = create_spectrum(record_sec)

        ring_in_650hz = __is_ringing(fft_data, f_list, 650, 665)
        ring_in_850hz = __is_ringing(fft_data, f_list, 850, 865)

        if ring_in_650hz and ring_in_850hz:
            slack_app.notify_slack("interphone has ringed!!!")


def __is_ringing(fft_data, f_list, min_hz, max_hz):
    threshold = 2000000
    for hz in range(min_hz, max_hz):
        indexes = np.where((f_list >= hz) & (f_list < hz + 1))
        if len(indexes) <= 0:
            continue

        for idx in indexes[0]:
            amp = fft_data[idx]
            if amp > threshold:
                return True

    return False


if __name__ == "__main__":
    main()
