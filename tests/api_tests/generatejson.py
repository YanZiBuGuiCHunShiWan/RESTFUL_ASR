import json
import base64
a={
        "encode":"false",
        "filename":"5.wav",
        "speech":None}
file_path="./Wavdocument/5.wav"
with open(file_path,"rb") as doc:
    binary=doc.read()
    binary_encode=base64.b64encode(binary)
    a["speech"]=binary_encode.decode("utf-8")

with open("./info5.json","w") as doc:
    json.dump(a,doc)
