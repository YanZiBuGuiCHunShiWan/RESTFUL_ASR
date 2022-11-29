import json
import random
import base64
import unittest

import requests

HOST = '127.0.0.1'
PORT = 7788

file_name="../../Wavdocument/2.wav"
file_name4="../../Wavdocument/1.wav"
file_name1="../../Wavdocument/a.txt"
file_name2="../../Wavdocument/out.wav"
file_name5="../../Wavdocument/4.wav"
file_name6="../../Wavdocument/5.wav"
file_name7="../../Wavdocument/16k.pcm"
def convert(file):
    with open(file,"rb") as document:
        binary=document.read()
    data=base64.b64encode(binary)
    return data

class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        bs64_encode=convert(file_name)
        bs64_encode1=convert(file_name4)
        bs64_encode2=convert(file_name1)
        bs64_encode3=convert(file_name2)
        bs64_encode5=convert(file_name5)
        bs64_encode6=convert(file_name6)
        bs64_encode7=convert(file_name7)
        self.info={
            "filename":"out.wav",
            "encode":"false",
        "speech":bs64_encode.decode("utf-8")}

        self.info1={
            "filename": "",
            "encode": "false",
            "speech": bs64_encode.decode("utf-8")
        }

        self.info2={
            "filename": "1.wav",
            "encode": "false",
            "speech": bs64_encode.decode("utf-8")
        }

        self.info3 = {
            "filename": "1.wav",
            "encode": "true",
            "speech": ""
        }

        self.info4={
            "filename": "1.txt",
            "encode": "true",
            "speech": ""
        }
        self.info5={}

        self.info6={
            "filename":"1.wav",
            "encode":"false",
            "speech":bs64_encode2.decode("utf-8")
                }


        self.info7={
            "filename":"1.wav",
            "encode":"false",
            "speech":bs64_encode1.decode("utf-8")
                }


        self.info8={
            "filename":"1.wav",
            "encode":"false",
            "speech":bs64_encode3.decode("utf-8")
                }

        self.info9={
            "filename":"1.wav",
            "encode":"false",
            "speech":str(bs64_encode3)
                }

        self.info10={
            "filename":"out.wav",
            "encode":"false",
        "speech":bs64_encode5.decode("utf-8")}

        self.info11={
            "filename":"out.wav",
            "encode":"false",
        "speech":bs64_encode6.decode("utf-8")}

        self.info12={
            "filename":"out.pcm",
            "encode":"false",
        "speech":bs64_encode7.decode("utf-8")}

    def test_asr13(self):
        r = requests.post("http://{}:{}/asr".format(HOST, PORT), json=self.info12)
        print(json.loads(r.text))
        print("***********************************************************************")

if __name__ == '__main__':
    unittest.main()
