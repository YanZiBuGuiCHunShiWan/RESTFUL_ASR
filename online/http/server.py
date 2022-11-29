import flask.scaffold
import os
from flask import Flask
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restful import Api
from online import logger
from online.http.resources.hello_resource import  HelloResource
from online.http.resources.asr_resource import ASR_Resource
from REST_Engine.REST_WenetEngine import WenetEngine
from Puntuation.puntuation_model import pun_executor


port=7777
asr_model_config_path="/home/tangtianchi/ASR_project/conf/decode_engine.yaml"
punc_model_config_path="/home/tangtianchi/ASR_project/Puntuation/pun_models"



app = Flask(__name__)
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
app.config['UPLOAD_FOLDER'] = '/asr'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['BUNDLE_ERRORS'] = True
api = Api(app)
asr = WenetEngine(asr_model_config_path)
punc_model=pun_executor
resource_class_kwargs = {'asr': asr,"punc":punc_model}
api.add_resource(HelloResource, '/')
api.add_resource(ASR_Resource, '/asr', resource_class_kwargs=resource_class_kwargs)

# 启动服务，设置host port
# host='0.0.0.0'，表示外部机器可以访问，必须设置为0.0.0.0
logger.info('server starts port {}'.format(port))
# server = pywsgi.WSGIServer(('0.0.0.0', port), app)
# server.serve_forever()

