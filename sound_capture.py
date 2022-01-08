import numpy as np
import pyaudio

__FRAME_RATE = 16000


def _capture_sound(record_sec=2):
    channels = 1
    chunk = 1024 * 2

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=channels, rate=__FRAME_RATE, input=True)

    data = []
    for i in range(0, int(__FRAME_RATE / chunk * record_sec)):
        data.append(stream.read(chunk))

    stream.close()
    p.terminate()

    return b"".join(data)


def create_spectrum(record_sec=2):
    captured_sound = _capture_sound(record_sec)
    return _create_spectrum(captured_sound)


def _create_spectrum(captured_sound):
    wave_data = np.frombuffer(captured_sound, dtype="int16")
    fft_data_ = np.abs(np.fft.fft(wave_data))
    f_list_ = np.fft.fftfreq(fft_data_.shape[0], d=1.0 / __FRAME_RATE)
    return f_list_, fft_data_


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    f_list, fft_data = create_spectrum()
    plt.plot(f_list[:int(len(f_list) / 2)], fft_data[:int(len(fft_data) / 2)])
    plt.show()
