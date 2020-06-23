import json
import re
from flask import Flask, request
from flask import make_response
app = Flask(__name__)
'''
統一回復
'''
wifi_product = '10691'
take_return_reply = '未事前通知KKday而有提早、延後取件情況發生，現場櫃檯有權拒絕領機，且此訂單將不予以退費。'
take_return_reply2 = '若無法於日本機場營業時間領取者，歡迎選擇台灣領取歸還，請至https://www.kkday.com/zh-tw/product/11157\n'
price_reply = '提供您價錢資訊，請注意點選的使用日即為您的出國日。\n如有問題歡迎聯絡客服'
dataflow_reply = '\n請勿在目的之外的國家開啟機器，避免產生漫遊費用。\n\
通信品質受到不同使用環境影響，網路速度將隨地形、氣候、建物遮蔽、使用人數及地點等因素影響。​\n如有問題歡迎詢問客服'
location_reply = ",偏遠山區及海邊可能訊號稍弱。\n如有問題歡迎詢問客服。"
mobile_power_reply='\n目前免費提供租借，一筆訂單可租借一個行動電源，麻煩下單後幫我們備註需要承租行動電源喔。'
def catch_inform():    
    '''
    抓商品資訊
    '''
    with open('data_wifi.json' , 'r', encoding='utf8') as reader:#讀json檔
        jf = json.loads(reader.read())
    getdata = jf.get(wifi_product)
    return getdata
def get_product_url_catch(search_product,search_airport):
    '''
    搜尋相關產品回傳proid(為了json檔設)
    '''
    search_product_place = re.search(r'【(.)+(?=】)', search_product).group(0).replace('【', '')
    #先找相關產品
    search_product_list = []
    with open('data_wifi.json' , 'r', encoding='utf8') as reader:#讀json檔
        jf = json.loads(reader.read())
    for i in jf:
        if search_product_place in jf[i].get("product_name"):
            search_product_list.append(i)
    #再找可領取的商品導引
#    search_product_take = []
    for i in search_product_list:
        if search_airport in jf[i].get("product_name"):
            return [i]
        for j in jf[i].get("QA_inform").get("take_return"):
            if search_airport in j:
                return [i]
#                search_product_take.append(i)
#                break        
    return []
def get_product_url(search_product,search_airport):
    '''
    拿到商品網址(找不到時)
    '''    
    other_product = get_product_url_catch(search_product,search_airport)
    taiwan_product = get_product_url_catch(search_product,'台灣')
    search_product_place = re.search(r'【(.)+(?=】)', search_product).group(0).replace('【', '').replace(' ', '')
    if len(other_product) != 0:
        text = 'https://www.kkday.com/zh-tw/product/' + other_product[0]
    else:
        text = 'https://www.kkday.com/zh-tw/product/productlist?page=1&sort=rdesc&keyword='+search_product_place + search_airport +'&qs='+ search_product_place + search_airport
    if len(taiwan_product) != 0:
        taiwan = 'https://www.kkday.com/zh-tw/product/' + taiwan_product[0]
    else:
        taiwan = 'https://www.kkday.com/zh-tw/product/productlist?page=1&sort=rdesc&keyword='+search_product_place +'台灣' +'&qs='+ search_product_place + '台灣'
    return '為您搜尋相關產品\n' + text + '\n或選擇台灣機場領取\n'+ taiwan + '\n請參考相關領取地點，歡迎詢問客服'
def process_take_information(getdata,airport):
    '''
    機場取還資訊
    '''
    text = "您好,\n"
    count = 0
    if getdata.get("QA_inform").get("take_return") is not None:
        for i in getdata.get("QA_inform").get("take_return"):
            if airport.split('機場')[0] in i:
                text = text + i + '\n'#到所有產品，建議台灣領取或尋找方案
                count = count + 1
    if count == 0:#找不到
        text = text + '找不到' + airport + '資訊\n' + \
            get_product_url(getdata.get("product_name"),airport.split('機場')[0])#抓網址
        return [text]
    return [text ,take_return_reply]#加統一回復

def process_price(getdata):
    '''
    這裡拿方案價格
    '''
    text = "您好\n"
    for i in getdata.get("option_group"):
        option_price = getdata.get("option_group").get(i)
        text = text + option_price.get("title") + str(option_price.get("price")) + option_price.get("currency") + '\n'
    if getdata.get("QA_inform").get("use_date") is not None:
        text = text + getdata.get("QA_inform").get("use_date") + '\n'
    return [text + price_reply]

def process_flow(getdata):
    '''
    這裡拿是否流量資訊回傳
    '''
    text = '您好此商品為'
    product_detail = getdata.get("product_info")
    text = text +  product_detail.get("data") + '\n最高連線台數:' + product_detail.get("phonecount") + '\n速度:' + product_detail.get("speed")
    return  [text + dataflow_reply]
def process_location(getdata):
    '''
    這裡拿訊號範圍
    '''
    text = '您好訊號範圍為'
    product_detail = getdata.get("product_info")
    text = text +  product_detail.get("coverage") +'\n速度:' + product_detail.get("speed")
    return  [text + location_reply]
def process_Mobile_power(getdata):
    '''
    這裡拿行動電源
    '''
    text = '您好初步為您查詢，此商品'
    product_detail = getdata.get("QA_inform")
    if product_detail.get("Mobile_power"):
        text = text +  '是可加租行動電源。'
    else:
        text = text +  '沒有查到有關資訊，為您詢問客服'
    return  [text + mobile_power_reply+'謝謝']
def process_Atake_Breturn(getdata):
    '''
    這裡拿甲地乙還
    '''
    text = '您好初步為您查詢，此商品'
    product_detail = getdata.get("QA_inform")
    if product_detail.get("Atake_Breturn"):
        text = text +  '是可甲地乙還的。'
    else:
        text = text +  '沒有查到有關資訊，為您詢問客服'
    return  [text + '謝謝']
def check_intent(intent,parameters):
    '''
    依intent給回復(center)
    '''
    data = catch_inform()
    fulfillmentMessages = []
    if data is None:
        fulfillmentMessages.append({"text": {"text": ['找不到相關資訊，請詢問客服']}})   
        return fulfillmentMessages
    if intent == "take_information" or intent == "return":#取還資訊 
        airport = parameters.get("airport")[0]
        fulfillmentText = process_take_information(data,airport)
    elif intent == "per_price":#價格
        fulfillmentText = process_price(data)
    elif intent == "flow_data":#流量
        fulfillmentText = process_flow(data) 
    elif intent == "signal_area_restriction":#訊號範圍
        fulfillmentText = process_location(data) 
    elif intent == "Atake_Breturn":#甲地乙還
        fulfillmentText = process_Atake_Breturn(data) 
    elif intent == "Mobile_power":#行動電源
        fulfillmentText = process_Mobile_power(data) 
    for i in range(len(fulfillmentText)):
        fulfillmentMessages.append({"text": {"text": [fulfillmentText[i]]}})    
    return fulfillmentMessages
def makeWebhookResult(req):
    '''
    製作回復
    '''
    #Dialogflow>Intent>Action 取名的內容
    if req.get("queryResult").get("action") != "get_product" and req.get("queryResult").get("action") != "get_inform":
        return {}
    result = req.get("queryResult")
    intent = result.get("intent").get("displayName")
    parameters = result.get("parameters")
    if parameters is None:
        parameters = result.get("outputContexts").get("parameters")
    #假設我去抓資料寫這
    fulfillmentText = check_intent(intent,parameters)
    print("Response:")
    print(fulfillmentText)
    #回傳
    return {"fulfillmentMessages": fulfillmentText}#'fulfillmentText': fulfillmentText
@app.route('/webhook', methods=['POST'])
def webhook():
    '''
    回復dialogflow webhook
    '''
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4,ensure_ascii=False))
    #製作回復
    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4,ensure_ascii=False)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

if __name__ == "__main__":
    app.run(debug=True,port=80)
    
