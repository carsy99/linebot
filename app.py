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
import random
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('TicAFdiC42N04QEKQNbCPpHk+wKiJEP/+oiXzVefrfwTFBYzfIxmMwf4w5xuoFZG9dsytlUOlin/TXS9RZcOd2jCdxuyPkAI+QwzY7eZFbOmRTFy88mkhPxuVXUkXDE/1wE8M7A194xVmvRIznV3eQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('34363ce357ba3f84f7b7d467de436ad4')

tz = pytz.timezone('Asia/Taipei')
lunar_new_year = tz.localize(datetime(2025, 1, 29))
current_time = datetime.now(tz).strftime("%Y/%m/%d %H:%M")
days_left = (lunar_new_year - datetime.now(tz)).days
line_bot_api.push_message('Ufdcb6f045f7bd653ef96bb0b7c541cd6', TextSendMessage(text=f'您好，目前時間是 {current_time} ，距離農曆新年還有 {days_left} 天！請問需要什麼服務呢?'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

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

    elif re.match('新年運勢占卜', message):
        flex_message = TextSendMessage(
            text='請點選您想占卜的是',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=PostbackAction(label="健康運", data="fortune_health")),
                    QuickReplyButton(action=PostbackAction(label="桃花運", data="fortune_love")),
                    QuickReplyButton(action=PostbackAction(label="財運", data="fortune_money")),
                    QuickReplyButton(action=PostbackAction(label="事業運", data="fortune_career")),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, flex_message)

    elif re.match('圖片', message):
        image_list = [
            "https://i.imgur.com/GeiH7G0.png",
            "https://i.imgur.com/mR9xSkz.png",
            "https://i.imgur.com/phpdKgF.jpeg",
            "https://i.imgur.com/sWRlimt.jpeg"
            "https://i.imgur.com/N0C90ym.jpeg",
            "https://i.imgur.com/Bup9ULg.jpeg",
            "https://i.imgur.com/v1tnbWm.jpeg",
            "https://i.imgur.com/YuaduGv.jpeg", 
            "https://i.imgur.com/DZ6Y4nS.jpeg"
            
        ]
        # 隨機選擇一張圖片
        selected_image = random.choice(image_list)

        # 傳送隨機圖片給使用者
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=selected_image,
                preview_image_url=selected_image
            )
        )
   
    elif re.match('過年小知識', message):
        image_carousel_template_message = TemplateSendMessage(
            alt_text='過年小知識圖片輪播',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://cdn2.ettoday.net/images/5441/e5441375.jpg',  # 圖片 1: 春聯
                        action=PostbackAction(
                            label='春聯的由來',
                            data='info_spring_couplet'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://cdn01.pinkoi.com/product/WFbGXeRf/2/640x530.jpg',  # 圖片 2: 紅包
                        action=PostbackAction(
                            label='紅包的故事',
                            data='info_red_packet'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://mir-s3-cdn-cf.behance.net/project_modules/max_1200/3ad5fa70124225.5b98e5817ae7e.jpg',  # 圖片 3: 年獸
                        action=PostbackAction(
                            label='年獸傳說',
                            data='info_nian_beast'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, image_carousel_template_message)


    elif re.match('過年菜單推薦', message):
        menu_carousel_template = TemplateSendMessage(
            alt_text="過年菜單推薦",
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url="https://api.elle.com.hk/var/site/storage/images/3/5/5/6/38236553-1-chi-HK/9.jpg",  # 年糕圖片
                        action=URIAction(
                            label="年糕食譜",
                            uri="https://icook.tw/recipes/431575"  # 年糕食譜網址
                        )
                    ),
                    ImageCarouselColumn(
                        image_url="https://i.ytimg.com/vi/INHXNskGlGQ/maxresdefault.jpg",  # 魚圖片
                        action=URIAction(
                            label="魚料理食譜",
                            uri="https://icook.tw/recipes/464311"
                        )
                    ),
                    ImageCarouselColumn(
                        image_url="https://i.epochtimes.com/assets/uploads/2022/12/id13882696-b6ba05c4b2cb55cb0021978e62ad6e75.jpg",  # 湯圓圖片
                        action=URIAction(
                            label="湯圓食譜",
                            uri="https://icook.tw/recipes/470783"
                        )
                    ),
                    ImageCarouselColumn(
                        image_url="https://images.chinatimes.com/newsphoto/2022-01-29/656/20220129003093.jpg",  # 長年菜圖片
                        action=URIAction(
                            label="長年菜食譜",
                            uri="https://icook.tw/recipes/463687"
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, menu_carousel_template)
    
    elif message == "今天是我的生日":
        image_message = ImageSendMessage(
            original_content_url="https://img.lovepik.com/free-template/20210106/bg/d4e0b6dd02a87.png_detail.jpg!detail808",
            preview_image_url="https://img.lovepik.com/free-template/20210106/bg/d4e0b6dd02a87.png_detail.jpg!detail808"
        )
        text_message = TextSendMessage(text="生日快樂！希望你有個美好的一天 🎉🎂")
        line_bot_api.reply_message(event.reply_token, [image_message, text_message])
    
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))



@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    
    # 運勢
    fortunes = {
        "fortune_health": [
            "身體素質還算不錯，須配合氣候調整飲食與穿著",
            "注意日常作息，健康是最大的本錢",
            "今年容易感冒，記得補充維生素",
            "適當運動有助於提高免疫力",
            "健康狀況良好，但偶爾也要放鬆身心"
        ],
        "fortune_love": [
            "今年會吸引有意者，但須辨別真心與虛情",
            "感情運平穩，但需多用心經營",
            "有機會邂逅對的人，保持心態開放",
            "感情中可能會有小波折，但能順利解決",
            "桃花旺盛，但不要被表象迷惑"
        ],
        "fortune_money": [
            "小心謹慎，必有不意之財",
            "獲利的速度沒有很快，但能逐步累積",
            "記得控制花費，不要衝動消費",
            "偏財運佳，有機會中獎或獲得意外收入",
            "今年的財運適合穩中求進，投資需謹慎"
        ],
        "fortune_career": [
            "今年事業運旺，努力會有回報",
            "有升遷或加薪的機會，把握好時機",
            "需要多與同事合作，團隊精神是關鍵",
            "工作壓力稍大，但能順利完成目標",
            "事業進展平穩，但需避免過於冒進"
        ]
    }

    # 小知識邏輯
    knowledge_responses = {
        'info_spring_couplet': '春聯 最早起源於桃符，據說是用來驅邪的。後來演變為現在的紅色對聯，寓意喜慶與平安。',
        'info_red_packet': '紅包 代表著祝福與吉祥，特別是在農曆新年，長輩會將紅包送給晚輩，象徵一年的好運。',
        'info_nian_beast': '年獸 是一種傳說中的怪物，每逢除夕會出來騷擾人們。後來人們發現它害怕紅色、火光與聲響，便有了放鞭炮的習俗。'
    }
    # 統一回應邏輯
    if data in fortunes:
        reply_text = random.choice(fortunes[data])
    else:
        reply_text = knowledge_responses.get(data, "抱歉，我不清楚這個請求的內容。")
    
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)




