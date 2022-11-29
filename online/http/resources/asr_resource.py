import time,os
import datetime,uuid
import base64
from pydub import AudioSegment
from flask import request,make_response
from flask_restful import Resource
from online import logger
from REST_Engine.VAD_Warpper import *

#定义路径
path='/home/tangtianchi/ASR_project/Wavdocument/'

#定义错误描述
##参数错误---6种描述
paramerr1="Parameter 'encode' should be 'false' or 'true' ."
paramerr2="Parameter 'encode' can't be none ."
paramerr3="Parameter 'filename' can't be none ."
paramerr4="Parameter 'filename' should end with *.wav or *.mp3."
paramerr5="Parameter 'speech' can't be none ."
paramerr6="Parameter 'speech' should be 'str' type ."
paramerrlist=[]

names=globals()
for i in range(1,7):
    paramerrlist.append(names['paramerr%s'%i])


#无效的base64编码,传入的不是wav数据的编码
Invalid_bs64code="Invalid base64-encode string or format err ."

#传入的json字符串内容是空的
Nonespace="None space"

#采样率错误
ErrorSamplingrate="Sampling rate error,sampling rate should in [16000,32000,44100,48000] ."

#未知错误
Unknown_err="Unknown error"

sample_rate=16000
channels=1

def convertbase64(byte_data):
    return base64.b64decode(byte_data)

def convert2base64(text):
    return base64.b64encode(text.encode("utf-8"))

def MP32WAV(mp3_path,wav_path):
    MP3_File = AudioSegment.from_mp3(mp3_path)
    MP3_File.export(wav_path, format="wav")


class ASR_Resource(Resource):
    def __init__(self,asr,punc):
        self.asr_model=asr
        self.punc_model=punc
    def post(self):
        init_time = time.time()
        result = {
            'status': 'OK',
            'msg': ''
        }
        data=request.get_json()
        try:
            assert data,Nonespace
            if data.get('encode'):
                mode = data.get('encode')
                assert mode in ["false", "true"], paramerr1
            else:
                raise Exception(paramerr2)

            #判断参数file_name:
            if data.get('filename'):
                filename=data.get("filename")
                assert  filename.endswith(".wav") or filename.endswith(".mp3") or filename.endswith(".pcm"),paramerr4
            else:
                raise Exception(paramerr3)

            #判断参数speech
            if data.get('speech'):
               upload_wav =data.get("speech")
               id = str(uuid.uuid1())
               suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
               name = "_".join([suffix, id]) + "_" + filename
                #把字符串改成bytes类型
               #对bytes进行解码
               filename=os.path.join(path,name)
               wav_byte=bytes(upload_wav,encoding="utf-8")
               decode_info=convertbase64(wav_byte) #对二进制度语音编码数据进行解码得到bytes
               if filename.endswith(".wav"):
                    assert "WAVEfmt" in decode_info[:15].decode("unicode_escape"),Invalid_bs64code

               #write_wave(filename,audio=decode_info,sample_rate=sample_rate) #讲文件写入指定文件夹
               with open(filename,"wb") as doc:
                   doc.write(decode_info)
               if filename.endswith(".mp3"):
                   filename_new=str(filename).replace("mp3","wav")
                   MP32WAV(filename,filename_new)
                   filename=filename_new
            else:
               raise Exception(paramerr5)

            #声学模型解码
            audio_bytes,sr,duration_time=read_wave(filename)

            if duration_time>=10.0: #长语音
                content_list=[]
                audio_bytes=crop_audio_vad(filename,aggressiveness=3,frame_duration_ms=30) #bytes是生成器
                for i,audio_byte in enumerate(audio_bytes):
                    content=self.asr_model.decode_audio(audio_byte)
                    content_list.append(content)
                text="".join(content_list)
                text=self.punc_model(text)
            else:  #短语音
                text=self.asr_model.decode_audio(audio_bytes)
                text=self.punc_model(text)

            if mode=="true":
                result["text"]=convert2base64(text.decode("utf-8"))
            else:
                result["text"]=text

            result['rate']=sr
            result['bitDepth']="PCM_16"
            result['code']='000000'
            result['time']=str(time.time()-init_time)[:4]+'s'
            logger.info('text:{},rate:{},code:{},cost_time:{}'.format(result["text"],result["rate"],result['code'],result['time']))

        except Exception as e:
            logger.exception(e)
            err=str(e)
            result['msg'] = err
            if err in paramerrlist:
                 result['code']="110001"
            elif err==Invalid_bs64code:
                 result['code']="110002"
            elif err==Nonespace:
                 result['code']="110003"
            elif err==ErrorSamplingrate:
                 result['code']="110004"
            else:
                 result['code']="110005"
            result['status'] = 'fail'
            result['time']=str(time.time()-init_time)[:4]+'s'
            logger.info('msg: {}, cost_time:{}'.format(result['msg'],result['time']))

        return result
