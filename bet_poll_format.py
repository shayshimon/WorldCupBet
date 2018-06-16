import pandas as pd
import json

df = pd.read_csv('./world_cup_bet_poll.csv')

out_json = []
for ind, row in df.iterrows():
    tmp_dic = {'name': row[2]}
    tmp_dic.update({chr(i): [row[(i - ord('A')) * 2 + 3], row[(i - ord('A')) * 2 + 4]] for i in range(ord('A'), ord('I'))})
    out_json.append(tmp_dic)

with open('bet_poll.json', 'w') as outfile:
    json.dump(out_json, outfile)
