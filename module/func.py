from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage

import http.client, json
from qnaapi.models import users

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


host = 'ehappyqna-0528.azurewebsites.net'  #主機
endpoint_key = "ffcc8ec4-929b-4526-b850-aeed48b53eb1"  #授權碼
kb = "da993f3a-f08f-46ab-b5c8-11d6ba7a0d36"  #GUID碼
method = "/qnamaker/knowledgebases/" + kb + "/generateAnswer"

def sendUse(event):  #使用說明
    try:
        text1 ='''
        這是回答關於Gina的問答機器人，請輸入您想問Gina的問題。
        This is a line bot to answer questions about Gina, I'm ready for your questions.
               '''
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendQnA(event, mtext):  #QnA
    question = {
        'question': mtext,
    }
    content = json.dumps(question)
    headers = {
        'Authorization': 'EndpointKey ' + endpoint_key,
        'Content-Type': 'application/json',
        'Content-Length': len(content)
    }
    conn = http.client.HTTPSConnection(host)
    conn.request ("POST", method, content, headers)
    response = conn.getresponse ()
    result = json.loads(response.read())
    result1 = result['answers'][0]['answer']
    if 'No good match' in result1:
        text1 = '''很抱歉，資料庫中無適當解答！請再輸入問題。\n 
        Sorry, the answer to this question isn't avaliable, please try another question.'''
        #將沒有解答的問題寫入資料庫
        userid = event.source.user_id
        unit = users.objects.create(uid=userid, question=mtext)
        unit.save()
    else:
        result2 = result1[2:]  #移除「A：」
        text1 = result2  
    message = TextSendMessage(
        text = text1
    )
    line_bot_api.reply_message(event.reply_token,message)
