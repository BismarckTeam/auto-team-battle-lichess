# -*- coding: utf-8 -*-
import os

from flask import Flask, jsonify
from flask import url_for
import time
from dotenv import load_dotenv
load_dotenv()

from authlib.integrations.flask_client import OAuth
import requests
import ndjson

r=requests.get("https://lichess.org/api/tournament/4dlFN5hJ/teams")
data=r.json(cls=ndjson.Decoder)
teams_list=data[0]['teams']
teams_id_list=[]

team_leaders=[]
for i in teams_list:
    teams_id_list.append(i['id'])

for i in teams_id_list:
    r2=requests.get("https://lichess.org/api/team/"+i)
    data2=r2.json(cls=ndjson.Decoder)
    try:
        leader=data2[0]['leader']['id']
        team_leaders.append(leader)
        print(leader)
    except BaseException:
        print()
print(team_leaders)

LICHESS_HOST = os.getenv("LICHESS_HOST", "https://lichess.org")

app = Flask(__name__)
app.secret_key = "123"
app.config['LICHESS_CLIENT_ID'] =  os.getenv("LICHESS_CLIENT_ID")
app.config['LICHESS_AUTHORIZE_URL'] = f"{LICHESS_HOST}/oauth"
app.config['LICHESS_ACCESS_TOKEN_URL'] = f"{LICHESS_HOST}/api/token"

oauth = OAuth(app)
oauth.register('lichess', client_kwargs={"code_challenge_method": "S256"})
       
@app.route('/')
def login():
    redirect_uri = url_for("authorize", _external=True)
    return oauth.lichess.authorize_redirect(redirect_uri, scope="msg:write")
        
@app.route('/authorize')
def authorize():
    token = oauth.lichess.authorize_access_token()
    
    
    bearer = "zwA7dl94Ak6tXJrg"
    
    
    headers = {'Authorization': f'Bearer {bearer}'}
    for i in range(len(team_leaders)):
        msg="Здравствуйте! Напоминаю, что сегодня проходит призовой турнир, в котором участвует Ваша команда. Ссылка на турнир: https://lichess.org/tournament/4dlFN5hJ"
        req=requests.post("https://lichess.org/inbox/"+team_leaders[i], data={"text":msg}, headers=headers)
        time.sleep(10)
        print(req)
    return "Nochcho"
if __name__ == '__main__':
    app.run()