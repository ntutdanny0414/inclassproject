import json
import os
import re


index = 'tag_5_5'
wifi_pth = os.path.join(index, 'wifi')
sim_pth = os.path.join(index, 'sim')


match_txt = r'(SIM(卡)?|網卡|sim)'

for f in sorted(os.listdir(index)):
    if f.endswith('.json'):
        with open(os.path.join(index, f), 'r') as j:
            print(f)
            a = json.load(j)
            found_wifi = False
            for qa in a[f[:-5]]:
                if not len(qa['answer']): continue
                question, answer = qa['question'][0], qa['answer'][0]
                #print(question, answer)
                
                if re.search(match_txt, question) or re.search(match_txt, answer):
                    with open(os.path.join(sim_pth, f), 'w') as jj:
                        json.dump(a, jj,sort_keys=False, indent = 4,ensure_ascii=False)
                    found_wifi = True
                    break
                
            if not found_wifi:
                with open(os.path.join(wifi_pth, f), 'w') as jj:
                    json.dump(a, jj,sort_keys=False, indent = 4,ensure_ascii=False)

    