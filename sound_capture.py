import numpy as np
import matplotlib.pyplot as plt
import pyaudio

_FRAMERATE = 16000


def _capture_sound(record_sec=2):
    CHANNELS = 1
    CHUNK = 1024 * 2

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=CHANNELS,
                    rate=_FRAMERATE, input=True)

    data = []
    for i in range(0, int(_FRAMERATE / CHUNK * record_sec)):
        data.append(stream.read(CHUNK))

    stream.close()
    p.terminate()

    return b''.join(data)


def create_spectrum(record_sec=2):
    captured_sound = _capture_sound(record_sec)
    return _create_spectrum(captured_sound, record_sec)


def _create_spectrum(captured_sound, record_sec=2):
    wave_data = np.frombuffer(captured_sound, dtype='int16')
    fft_data = np.abs(np.fft.fft(wave_data))
    f_list = np.fft.fftfreq(fft_data.shape[0], d=1.0 / _FRAMERATE)
    return f_list, fft_data


def _plot_spectrum():
    f_list, fft_data = create_spectrum()
    plt.plot(f_list[:int(len(f_list) / 2)], fft_data[:int(len(fft_data) / 2)])
    plt.show()


if __name__ == '__main__':
    _plot_spectrum()
