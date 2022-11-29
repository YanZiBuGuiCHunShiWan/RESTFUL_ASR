import copy
import os
import numpy as np
import yaml
import torch
import torchaudio.compliance.kaldi as kaldi
import datetime,wave
from wenet.transformer.asr_model import init_asr_model
from wenet.utils.checkpoint import load_checkpoint
from collections import deque
from REST_Engine import logger

class WenetEngine():
    DECODE_CHUNK_SIZE = 4000
    #模型初始化
    def __init__(self,model_config_path):
        'Loads and sets up the model .'
        with open(model_config_path,"r") as document:
            self.configs=yaml.load(document,Loader=yaml.FullLoader)
        #symbol_table = read_symbol_table(self.configs['dict_path'])
        os.environ['CUDA_VISIBLE_DEVICES'] = str(self.configs['gpu'])
        decode_conf = copy.deepcopy(self.configs['data_conf'])
        decode_conf['filter_conf']['max_length'] = 102400
        decode_conf['filter_conf']['min_length'] = 0
        decode_conf['filter_conf']['token_max_length'] = 102400
        decode_conf['filter_conf']['token_min_length'] = 0
        use_cuda = self.configs['gpu'] >= 0 and torch.cuda.is_available()
        self.device = torch.device('cuda')

        # convert num to symbles
        self.num2sym_dict = {}
        with open(self.configs['dict_path'], 'r') as fin:
            for line in fin:
                arr = line.strip().split()
                assert len(arr) == 2
                self.num2sym_dict[int(arr[1])] = arr[0]
        self.eos = len(self.num2sym_dict) - 1

        self.models = deque(maxlen=self.configs['engine_max_decoders'])
        self.asr = init_asr_model(self.configs)  #模型初始化成功
        load_checkpoint(self.asr, self.configs['model_path'])
        self.asr = self.asr.to(self.device)
        logger.info("Model has initialized .")
        self.asr.eval()

    def _get_model(self):
        pass

    def _feature_extraction(self,waveform):
        num_mel_bins = self.configs['data_conf']['fbank_conf']['num_mel_bins']  # 80
        frame_length = self.configs['data_conf']['fbank_conf']['frame_length']  # 25
        frame_shift = self.configs['data_conf']['fbank_conf']['frame_shift']  # 10
        dither = self.configs['data_conf']['fbank_conf']['dither']  # 0.0
        feat = kaldi.fbank(waveform,
                           num_mel_bins=num_mel_bins,
                           frame_length=frame_length,
                           frame_shift=frame_shift,
                           dither=dither,
                           energy_floor=0.0,
                           sample_frequency=self.configs['engine_sample_rate_hertz'])
        feat = feat.unsqueeze(0).to(self.device)
        feat_length = torch.IntTensor([feat.size()[1]]).to(self.device)
        return feat,feat_length

    def get_audio(self,wavfile):
        with wave.open(wavfile, 'rb') as wavfile:
            # ch = wavfile.getnchannels()
            # bits = wavfile.getsampwidth()
            # rate = wavfile.getframerate()
            # nframes = wavfile.getnframes()
            buf = wavfile.readframes(-1)
        return  buf

    def decode_audio(self,audio):
        if len(audio) < 1600:  # 小于0.1秒，不解码
            return ''
        waveform = np.frombuffer(audio, dtype=np.int16)
        waveform = torch.from_numpy(waveform).float().unsqueeze(0)
        waveform = waveform.to(self.device)
        waveform_feat, feat_length = self._feature_extraction(waveform)
        model = self.asr
        with torch.no_grad():
            hyps, scores = model.recognize(waveform_feat,
                                           feat_length,
                                           beam_size=self.configs['beam_size'],
                                           decoding_chunk_size=-1,
                                           num_decoding_left_chunks=self.configs['num_decoding_left_chunks'],
                                           simulate_streaming=False)
            hyps = [hyp.tolist() for hyp in hyps[0]]
            result = self._num2sym(hyps)
        if len(audio) > WenetEngine.DECODE_CHUNK_SIZE:
            #self.save_wave(audio, result)
            pass
        return result

    def _num2sym(self, hyps):
        content = ''
        for w in hyps:
            if w == self.eos:
                break
            content += self.num2sym_dict[w]
        return content

    def save_wave(self, audio, transcript):
        now_time = datetime.datetime.now()
        year = str(now_time.year)
        month = str(now_time.month)
        day = str(now_time.day)
        audio_dir = os.path.join(self.configs['audio_save_path'], year, month, day)
        wav_file = audio_dir + '/' + datetime.datetime.now().strftime("%H-%M-%S-%f_") + transcript[0:20] + '_.wav'
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)
        with wave.open(wav_file, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.configs['engine_sample_rate_hertz'])
            wf.writeframes(audio)
