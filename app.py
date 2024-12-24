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
line_bot_api.push_message('Ufdcb6f045f7bd653ef96bb0b7c541cd6', TextSendMessage(text=f'🤖您好～目前時間是 {current_time} ，距離農曆新年還有 {days_left} 天！可點選下方選單迎新春🧧'))

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
    if re.search('告訴我秘密',message):
        audio_message = AudioSendMessage(
            original_content_url='https://campus-studio.com/download/twsong.mp3',
            duration=81000
        )
        line_bot_api.reply_message(event.reply_token, audio_message)

    elif re.search('新年運勢占卜', message):
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

    elif re.search('年味圖片', message):
        image_list = [
            "https://i.imgur.com/GeiH7G0.png",
            "https://i.imgur.com/mR9xSkz.png",
            "https://i.imgur.com/phpdKgF.jpeg",
            "https://i.imgur.com/sWRlimt.jpeg"
            "https://i.imgur.com/N0C90ym.jpeg",
            "https://i.imgur.com/Bup9ULg.jpeg",
            "https://i.imgur.com/v1tnbWm.jpeg",
            "https://i.imgur.com/YuaduGv.jpeg", 
            "https://i.imgur.com/DZ6Y4nS.jpeg",
            "https://stage.taipei101mall.com.tw/uploads/content/4644d118-c050-92d6-dffa-4fe18a0798e6.jpg",
            "https://i0.wp.com/salespower.com.tw/wp-content/uploads/2024/09/2025%E8%9B%87%E5%B9%B4.png",
            "https://hips.hearstapps.com/hmg-prod/images/new-year-card-with-a-cute-snake-in-a-santa-royalty-free-illustration-1731315137.jpg",
            "https://shopee.tw/blog/wp-content/uploads/2024/01/bd9876fb352dc552b3426d2fa65b63a5.jpg"     
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
   
    elif re.search('過年小知識', message):
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


    elif re.search('年菜推薦', message):
        menu_carousel_template = TemplateSendMessage(
            alt_text="過年菜單推薦",
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url="https://api.elle.com.hk/var/site/storage/images/3/5/5/6/38236553-1-chi-HK/9.jpg",  # 年糕圖片
                        title="年糕 - 步步高升",
                        text="象徵步步高升⬆️的甜點，適合全家共享！",
                        actions=[
                            URIAction(
                                label="查看年糕食譜",
                                uri="https://icook.tw/recipes/431575"  # 年糕食譜網址
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://i.ytimg.com/vi/INHXNskGlGQ/maxresdefault.jpg",  # 魚圖片
                        title="魚 - 年年有餘",
                        text="不可或缺的魚🐟料理，代表著豐足和富裕。",
                        actions=[
                            URIAction(
                                label="查看魚料理食譜",
                                uri="https://icook.tw/recipes/464311"
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://i.epochtimes.com/assets/uploads/2022/12/id13882696-b6ba05c4b2cb55cb0021978e62ad6e75.jpg",  # 湯圓圖片
                        title="湯圓 - 團團圓圓",
                        text="甜蜜的🔴湯圓⚪寓意著一家人團聚。",
                        actions=[
                            URIAction(
                                label="查看湯圓食譜",
                                uri="https://icook.tw/recipes/470783"
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://images.chinatimes.com/newsphoto/2022-01-29/656/20220129003093.jpg",  # 長年菜圖片
                        title="長年菜 - 長長久久",
                        text="象徵健康長壽的必備青菜🥬。",
                        actions=[
                            URIAction(
                                label="查看長年菜食譜",
                                uri="https://icook.tw/recipes/463687"
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, menu_carousel_template)

    elif re.search('音樂分享', message):
        # 定義音樂清單
        music_list = [
            "https://www.youtube.com/watch?v=_VCAeYVYmyI",  # 千金娃娃 - 恭喜恭喜 《童星飞舞闹新年》
            "https://www.youtube.com/watch?v=Fz9GLF8Vcek",  # 財神到
            "https://www.youtube.com/watch?v=b4SRZurGg1c",  # 劉德華Andy Lau-恭喜發財(Gong Xi Fa Cai)
            "https://www.youtube.com/watch?v=_mmpY-Si4sc",  # 七個隆咚鏘
            "https://www.youtube.com/watch?v=VGnOpZhsPk4",  # ATEEZ(에이티즈) - 'WORK' Official MV
        ]
    
        # 隨機選擇一首音樂
        selected_music = random.choice(music_list)
    
        # 回應訊息
        reply_message = TextSendMessage(
            text=f"🎼為您推薦音樂：\n{selected_music}"
        )
        line_bot_api.reply_message(event.reply_token, reply_message)

    elif re.search('祝福語音', message):
        audio_list = [
            {
                "url": "https://your-audio-storage.com/happy_new_year.mp3",
                "text": "祝您新年快樂！",
                "duration": 5000
            },
            {
                "url": "https://your-audio-storage.com/congratulations.mp3",
                "text": "恭喜發財！",
                "duration": 4500
            }
        ]
    
        selected_audio = random.choice(audio_list)
    
        text_message = TextSendMessage(text=selected_audio["text"])
        audio_message = AudioSendMessage(
            original_content_url=selected_audio["url"],
            duration=selected_audio["duration"]
        )
        line_bot_api.reply_message(event.reply_token, [text_message, audio_message])
    
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
            "身體素質還算不錯👍，須配合氣候調整飲食與穿著",
            "注意日常作息，健康是最大的本錢💵",
            "今年容易感冒😷，記得補充維生素🥦",
            "適當運動有助於提高免疫力🏃‍➡️",
            "健康狀況良好，但偶爾也要放鬆身心☺️"
        ],
        "fortune_love": [
            "今年會吸引有意者，但須辨別真心與虛情🤔",
            "感情運平穩，但需多用心經營🙂",
            "有機會邂逅對的人，保持心態開放🤗",
            "感情中可能會有小波折，但能順利解決👌",
            "桃花旺盛，但不要被表象迷惑🫸"
        ],
        "fortune_money": [
            "小心謹慎，必🈶不意之財💵",
            "獲利的速度沒有很快，但能逐步累積💹",
            "記得控制花費，不要衝動消費💸",
            "偏財運佳，🈶機會中獎或獲得意外收入💰",
            "今年的財運適合穩中求進，投資需謹慎🪙"
        ],
        "fortune_career": [
            "今年事業運旺，努力會🈶回報",
            "有升遷⤴️或加薪⤴️的機會，把握好時機",
            "需要多與同事合作，團隊精神是關鍵👥",
            "工作壓力稍大，但能順利完成目標✅",
            "事業進展平穩，但需避免過於冒進📋"
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




