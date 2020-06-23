# -*- coding: UTF-8 -*-
import pandas as pd
import time
import json


with open('kk_message.csv_20180101_20181231.csv', 'r') as csvfile:
    reader = pd.read_csv(csvfile)
    #print(reader[0])

    all_data = {}
    file_index = 2
    #reader[reader['msg_oid'] == 6311276]
    filtered_reader = reader[reader['parent_msg_oid'] == 0]
    filtered_reader = filtered_reader[filtered_reader['msg_type'] == 'PROD']
    print(len(list(filtered_reader['msg_oid'])))
    for index, (oid, product_oid, content, lang) in enumerate(zip(filtered_reader['msg_oid'], filtered_reader['prod_oid'], filtered_reader['msg_content'], filtered_reader['msg_reply_lang'])):
        if index % 100 == 0: print(index, end='\r')
        #if parent_oid != 0: continue
        
        #print(oid, parent_oid, content) 
        #print(reader[reader['parent_msg_oid'] == oid])
        sorted_list = reader[reader['parent_msg_oid'] == oid].sort_values(by=['create_date'])
        
        find_zh_tw = False
        find_prod_oid = False
        m_turn = True

        final_prod_oid = None
        data = {"question": [], "answer": [], "reply": [], "lang": None}
        #data[oid] = {"question": [], "answer": [], 'lang': None}
        
        for p, c, t, l in zip(sorted_list['prod_oid'], sorted_list['msg_content'], sorted_list['send_type'], sorted_list['msg_reply_lang']):
            if not find_zh_tw:
                if l == 'zh-tw':
                    data['lang'] = 'zh-tw'
                    find_zh_tw = True
            
            if not find_prod_oid:
                if p != 'NA':
                    final_prod_oid = p
                    find_prod_oid = True
    

            if t == 'M':
                if not m_turn:
                    data['answer'].append('')
                    data['reply'].append('')
                    
                data['question'].append(c)
                m_turn = False
            
            elif t == 'K' or t == 'S':
                if m_turn:
                    data['question'].append('')
                    
                data['answer'].append(c)
                data['reply'].append(t)
                m_turn = True

        
        if final_prod_oid and find_zh_tw:
            if int(final_prod_oid) not in all_data:
                all_data[int(final_prod_oid)] = [data]
            else:
                #print('Y')
                all_data[int(final_prod_oid)].append(data)
        
       
        if len(all_data) == 20000:
            with open(f'./prod/{file_index}.json', 'w') as jsonfile:
                json.dump(all_data, jsonfile, sort_keys=False, indent = 4,ensure_ascii=False)

            all_data = {}
            file_index += 1
            #break

        

    with open(f'./prod/{file_index}.json', 'w') as jsonfile:
        json.dump(all_data, jsonfile, sort_keys=False, indent = 4,ensure_ascii=False)
