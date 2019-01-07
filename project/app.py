from flask import Flask, request, render_template
import os
import requests
import random
from pprint import pprint as pp

app = Flask(__name__)

token = os.getenv('TELEGRAM_TOKEN')
naver_id = os.getenv('NAVER_ID')
naver_secret = os.getenv('NAVER_SECRET')

# use this route when telegram send alram to our server
#   if user send a message to our bot,
#   telegram send alram to our server.(json)

# set Webhook = request telegram for sending alram whenever a message is sent


@app.route('/setWebhook')
def setWebhook() :
    baseUrl = "https://api.hphk.io/telegram" # replace api.telegram.org
    myUrl = "https://clova-face-recognition-don2101.c9users.io"
    
    url = "{}/bot{}/setWebhook?url={}/{}".format(baseUrl, token, myUrl, token)
    response = requests.get(url)
    
    return '{}'.format(response), 200

# telegram use this route. data will be put through this router
@app.route('/{}'.format(token), methods=['POST'])
def telegram() :
    doc = request.get_json()

    # for every messages, this chatbot say 'shut up'
    baseUrl = "https://api.hphk.io/telegram"
    chat_id = doc['message']['chat']['id']
    #sentMessage = doc['message']['text']
    #sendMessage = ""
    
    # if fromMessage == 'lotto' :
    #     sendMessage = random.sample(range(1, 46), 6)
    # else :
    #     sendMessage = fromMessage
    # myUrl = "bot{}/sendMessage?chat_id={}&text={}".format(token, chat_id, sendMessage)
    
    # # sends message
    # requests.get(baseUrl+myUrl)
    
    img = False
    
    if doc.get('message').get('photo') is not None:
        img = True
    
    if img:
        file_id = doc.get('message').get('photo')[-1].get('file_id')
        file = requests.get("{}/bot{}/getFile?file_id={}".format(baseUrl, token, file_id))
        file_url = "{}/file/bot{}/{}".format(baseUrl, token, file.json().get('result').get('file_path'))
        
        # 네이버로 요청
        res = requests.get(file_url, stream=True)
        clova_res = requests.post('https://openapi.naver.com/v1/vision/celebrity',
            headers={
                'X-Naver-Client-Id':naver_id,
                'X-Naver-Client-Secret':naver_secret
            },
            files={
                'image':res.raw.read()
            })
        if clova_res.json().get('info').get('faceCount'):
            print(clova_res.json().get('faces'))
            text = "{}".format(clova_res.json().get('faces')[0].get('celebrity').get('value'))
        else:
            text = "인식된 사람이 없습니다."
    else:
    	# text 처리
    	text = doc['message']['text']
        
    
    requests.get('{}/bot{}/sendMessage?chat_id={}&text={}'.format(baseUrl, token, chat_id, text))

    
    return '', 200
    