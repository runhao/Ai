from unittest import result
from aip import AipSpeech
import pyaudio
import wave

def sp_re():
    ''' 你的 APPID AK SK '''
    APP_ID = '26032630'
    API_KEY = 'C2Kfa93OcZ6NM3HqD5Y9Dh6Y'
    SECRET_KEY = 'sfX3P51N9fOjQXGwee5ER6iiiRza5jwT'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    CHUNK = 512
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "sp.wav"

    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    print("recording...")
    
    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("done")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # 读取文件
    def get_file_content(file_path):
        with open(file_path, 'rb') as fp:
            return fp.read()
        # 识别本地文件
    result = client.asr(get_file_content('sp.wav'), 'wav', 16000, {'dev_pid': 1537,})
    result = result["result"][0]
    return result