import unittest
import numpy as np
import wave
import base64
import soundfile
from ASR.inference import ASR_inference

#base64编码
def convert(file):
    with open(file,"rb") as document:
        binary=document.read()
    data=base64.b64encode(binary)
    return data


#base64解码
def decodebase64(data):
    decode_data=base64.b64decode(data)
    return decode_data


class MyTestcase(unittest.TestCase):
    def setUp(self) -> None:
        self.asr=ASR_inference()

    def test_asr(self):
        file_name="/home/test/Study/asr/Wavdocument/2.wav"

        speech,rate=soundfile.read(file_name)

        result=self.asr.speech2text(speech)
        print(result)


if __name__ == '__main__':
    unittest.main()