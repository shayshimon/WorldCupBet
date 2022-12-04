from flask import Flask, render_template
from itertools import groupby
import requests
import json


def api_login():
    url = 'http://api.cup2022.ir/api/v1/user/login'
    header = {'Content-Type': 'application/json'}
    data = {
        'email': 'makunochi+worldcup@gmail.com',
        'password': 'Shanghai1234'
    }
    res = requests.post(url, data=json.dumps(data), headers=header)
    return res.json()['data']['token']

def get_standings():
    url = 'http://api.cup2022.ir/api/v1/standings'
    header = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_login()}'
    }
    res = requests.get(url, headers=header)
    stand_groups = res.json()['data']
    house_dict = {}
    for item in stand_groups:
        house_key = item['group']
        house_dict[house_key] = sorted(list(item['teams']), key=lambda x: (x['pts'], x['gd'], x['gf'], x['name_en']), reverse=True)

    return house_dict

app = Flask(__name__)

@app.route("/")
def present_scores():
    stand_dict = get_standings()

    with open('./data/nutrino_bet_poll.json', 'r') as infile:
        bet_dict = json.load(infile)

    for item in bet_dict:
        item_rank = 0
        for house in stand_dict:
            house_rank = 0
            if stand_dict[house][0]['name_en'] == item[house][0]:
                house_rank += 3
            elif item[house][0] == stand_dict[house][1]['name_en']:
                house_rank += 2

            if stand_dict[house][1]['name_en'] == item[house][1]:
                house_rank += 3
            elif item[house][1] == stand_dict[house][0]['name_en']:
                house_rank += 2

            item_rank += house_rank

        item['rank'] = item_rank

    sorted_bet_dict = sorted(bet_dict, key=lambda x: x['rank'], reverse=True)
    abc_list = [chr(i) for i in range(ord('A'), ord('I'))]
    return render_template("wc_rank_new.html", result=sorted_bet_dict, abc_list=abc_list, stand_dict=stand_dict)

@app.route("/end_point")
def endp():
    return get_standings()
