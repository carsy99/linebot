# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from datetime import datetime
import pytz
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('TicAFdiC42N04QEKQNbCPpHk+wKiJEP/+oiXzVefrfwTFBYzfIxmMwf4w5xuoFZG9dsytlUOlin/TXS9RZcOd2jCdxuyPkAI+QwzY7eZFbOmRTFy88mkhPxuVXUkXDE/1wE8M7A194xVmvRIznV3eQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('34363ce357ba3f84f7b7d467de436ad4')

lunar_new_year = datetime(2025, 1, 29)
def calculate_days_to_new_year():
    tz = pytz.timezone('Asia/Taipei')
    today = datetime.now(tz)
    days_left = (lunar_new_year - today).days
    return days_left

def send_initial_message():
    tz = pytz.timezone('Asia/Taipei')
    current_time = datetime.now(tz).strftime("%Y/%m/%d %H:%M")
    days_left = calculate_days_to_new_year()
    message = f"您好，目前時間是 {current_time} ，距離農曆新年還有 {days_left} 天！請問需要什麼服務呢?"
    user_id = 'Ufdcb6f045f7bd653ef96bb0b7c541cd6' 
    line_bot_api.push_message(user_id, TextSendMessage(text=message))

#tz = pytz.timezone('Asia/Taipei')
#current_time = datetime.now(tz).strftime("%Y/%m/%d %H:%M")
#line_bot_api.push_message('Ufdcb6f045f7bd653ef96bb0b7c541cd6', TextSendMessage(text=f'您好，目前時間是 {current_time} ，距離農曆新年還有 {calculate_days_to_new_year()} 天！請問需要什麼服務呢?'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 發送初始化訊息
    send_initial_message()

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message =event.message.text
    if re.match('告訴我秘密',message):
        audio_message = AudioSendMessage(
            original_content_url='https://campus-studio.com/download/twsong.mp3',
            duration=81000
        )
        line_bot_api.reply_message(event.reply_token, audio_message)

    elif re.match('新年運勢占卜',message):
        flex_message = TextSendMessage(text='請點選您想占卜的是',
                               quick_reply=QuickReply(items=[
                                   QuickReplyButton(action=MessageAction(label="健康運", text="身體素質還算不錯，須配合氣候調整飲食與穿著")),
                                   QuickReplyButton(action=MessageAction(label="桃花運", text="今年會吸引有意者，但須辨別真心與虛情")),
                                   QuickReplyButton(action=MessageAction(label="財運", text="小心謹慎，必有不意之財")),
                                   QuickReplyButton(action=MessageAction(label="事業運", text="今年事業運旺，努力會有回報"))
                               ]))
        line_bot_api.reply_message(event.reply_token, flex_message)
    
    elif message == "今天是我的生日":
        image_message = ImageSendMessage(
            original_content_url="https://img.lovepik.com/free-template/20210106/bg/d4e0b6dd02a87.png_detail.jpg!detail808",
            preview_image_url="https://img.lovepik.com/free-template/20210106/bg/d4e0b6dd02a87.png_detail.jpg!detail808"
        )
        text_message = TextSendMessage(text="生日快樂！希望你有個美好的一天 🎉🎂")
        line_bot_api.reply_message(event.reply_token, [image_message, text_message])
    
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)




