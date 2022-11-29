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
file_name7="../../Wavdocument/1.mp3"
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
            "filename":"out.mp3",
            "encode":"false",
        "speech":bs64_encode7.decode("utf-8")}


    def test_asr(self): #正常例子
        r=requests.post("http://{}:{}/asr".format(HOST,PORT),json=self.info)
        assert r.status_code==200 and json.loads(r.text)["status"]=="OK","ERR"

    def test_asr1(self): #不携带文件名称
        r = requests.post("http://{}:{}/asr".format(HOST, PORT), json=self.info1)
        print(json.loads(r.text))

    def test_asr2(self): #encode为true
        r = requests.post("http://{}:{}/asr".format(HOST, PORT), json=self.info2)
        encode_content=json.loads(r.text)["text"]
        content=base64.b64decode(encode_content.encode("utf-8")).decode("utf-8")
        print(json.loads(r.text))

    def test_asr3(self):#speech参数为空
        r = requests.post("http://{}:{}/asr".format(HOST, PORT), json=self.info3)
        print(json.loads(r.text))

    def test_asr4(self):
        r = requests.post("http://{}:{}/asr".format(HOST, PORT), json=self.info4)
        print(json.loads(r.text))

    def test_asr5(self):
        r = requests.post("http://{}:{}/asr".format(HOST, PORT), json=self.info6)
        print(json.loads(r.text))

    def test_asr7(self):
        r = requests.post("http://{}:{}/asr".format(HOST, PORT), json=self.info7)
        print(json.loads(r.text))

    def test_asr8(self):
        r = requests.post("http://{}:{}/asr".format(HOST, PORT), json=self.info5)
        print(json.loads(r.text))

    def test_asr9(self):
        r = requests.post("http://{}:{}/asr".format(HOST, PORT), json=self.info8)
        print(json.loads(r.text))

    def test_asr10(self):
        r = requests.post("http://{}:{}/asr".format(HOST, PORT), json=self.info9)
        print(json.loads(r.text))
        print("------------------end------------------")

    def test_asr11(self):
        r = requests.post("http://{}:{}/asr".format(HOST, PORT), json=self.info10)
        print(json.loads(r.text))

    def test_asr12(self):
        r = requests.post("http://{}:{}/asr".format(HOST, PORT), json=self.info11)
        print(json.loads(r.text))
        
    def test_asr13(self):
        r = requests.post("http://{}:{}/asr".format(HOST, PORT), json=self.info12)
        print(json.loads(r.text))
        print("***********************************************************************")

if __name__ == '__main__':
    unittest.main()
