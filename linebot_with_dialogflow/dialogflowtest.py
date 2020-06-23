import apiai
import os.path
import sys
import json
CLIENT_ACCESS_TOKEN = '21efc05b37284aec831775c5d4c12cc9'
def dialog_detect(say):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
 
    request = ai.text_request()
 
    request.lang = 'tw'  # optional, default value equal 'en'
 
    request.query = say
    response = request.getresponse().read().decode('utf-8')
    result=json.loads(response)
    return result

