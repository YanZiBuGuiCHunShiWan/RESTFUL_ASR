import json
import base64
import unittest
import requests
import threading

HOST = '127.0.0.1'
PORT = 7777

file_name="/home/test/Study/asr/Wavdocument/out.wav"

def convert(file):
    with open(file,"rb") as document:
        binary=document.read()
    data=base64.b64encode(binary)
    return data


bs64_encode=convert(file_name)
info={
    "filename":"out.wav",
    "encode":"false",
"speech":bs64_encode.decode("utf-8")}



def test_asr(): #正常例子
    r=requests.post("http://{}:{}/asr".format(HOST,PORT),json=info)
    assert r.status_code==200 and json.loads(r.text)["status"]=="OK","ERR"
    print(json.loads(r.text))

if __name__ == '__main__':
    threads=[]
    nloops=10
    for i in range(nloops):
        t=threading.Thread(target=test_asr,args=(i,))
        threads.append(t)
    for i in range(nloops):
        threads[i].start()

    for i in range(nloops):
        threads[i].join()

    print("Don't wait .")

