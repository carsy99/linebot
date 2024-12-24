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
                    ),
                    ImageCarouselColumn(
                        image_url='https://watermark.lovepik.com/photo/40009/2423.jpg_wh1200.jpg',  # 圖片 4: 團圓飯
                        action=PostbackAction(
                            label='團圓飯的意義',
                            data='info_reunion_dinner'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://www.peponews.tw/wp-content/uploads/2019/01/685050_0.jpg',  # 圖片 5: 放鞭炮
                        action=PostbackAction(
                            label='放鞭炮的習俗',
                            data='info_firecracker'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://cn.chinadaily.com.cn/img/attachement/jpg/site1/20180217/d8cb8a3d71831bf1c00f30.jpg',  # 圖片 7: 新衣服
                        action=PostbackAction(
                            label='過年穿新衣',
                            data='info_new_clothes'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://img2.voc.com.cn/remote/2021/02/08/1029_f8f5ecf91c799a9cdf6d4a2bafef440d59dbaa78.jpg',  # 圖片 8: 倒貼福字
                        action=PostbackAction(
                            label='倒貼福字的由來',
                            data='info_upside_down_fu'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://thumbor.4gamers.com.tw/C_7ZkPIHSKI4xUjoqRR3y3J-QwU=/adaptive-fit-in/1200x1200/filters:no_upscale():extract_cover():format(jpeg):quality(85)/https%3A%2F%2Fugc-media.4gamers.com.tw%2Fpuku-prod-zh%2Fanonymous-story%2Fc5f5cd51-6da2-4976-9340-62f61440bbc9.jpg',  # 圖片 9: 大掃除
                        action=PostbackAction(
                            label='過年大掃除',
                            data='info_spring_cleaning'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://doqvf81n9htmm.cloudfront.net/data/TommyHuang_147/all/%E5%B9%B4%E8%8F%9C.jpg',  # 圖片 10: 過年菜肴
                        action=PostbackAction(
                            label='過年吃什麼',
                            data='info_new_year_food'
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
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://img.ltn.com.tw/Upload/food/page/2015/11/19/151119-716-0-YOtoq.jpg",  # 獅子頭圖片
                        title="獅子頭 - 團團圓圓",
                        text="大大的獅子頭🦁象徵團圓和喜氣！",
                        actions=[
                            URIAction(
                                label="查看獅子頭食譜",
                                uri="https://icook.tw/recipes/461553"
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://www.unileverfoodsolutions.tw/dam/global-ufs/mcos/na/taiwan/calcmenu/recipes/TW-recipes/general/%E5%8F%B0%E5%BC%8F%E6%A5%B5%E5%93%81%E4%BD%9B%E8%B7%B3%E7%89%86/main-header.jpg",  # 佛跳牆圖片
                        title="佛跳牆 - 招財進寶",
                        text="🧱多種食材熬製，寓意財富與富貴。",
                        actions=[
                            URIAction(
                                label="查看佛跳牆食譜",
                                uri="https://icook.tw/recipes/454556"
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://tokyo-kitchen.icook.network/uploads/recipe/cover/344880/3ed01d080c54cdf9.jpg",  # 蘿蔔糕圖片
                        title="蘿蔔糕 - 好運年年",
                        text="蒸糕象徵步步高升⬆️，是年節必備糕點。",
                        actions=[
                            URIAction(
                                label="查看蘿蔔糕食譜",
                                uri="https://icook.tw/recipes/412165"
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://img.ltn.com.tw/Upload/food/page/2020/01/22/200122-10227-0-VZ4kN.jpg",  # 八寶飯圖片
                        title="八寶飯 - 豐收與團圓",
                        text="甜美的八寶飯象徵豐收與圓滿⭕。",
                        actions=[
                            URIAction(
                                label="查看八寶飯食譜",
                                uri="https://icook.tw/recipes/454083"
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://i1.kknews.cc/wscmuiUc4F5c4cgljS0Ldhxt_yBeYxeMiw/0.jpg",  # 水晶餃圖片
                        title="水晶餃 - 聚財進寶",
                        text="晶瑩剔透的餃子寓意財富滿滿🤑。",
                        actions=[
                            URIAction(
                                label="查看水晶餃食譜",
                                uri="https://icook.tw/recipes/450546"
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://tokyo-kitchen.icook.network/uploads/category/background/50/6ae919ff4b3c9ae9.jpg",  # 更多料理圖片
                        title="更多料理推薦",
                        text="探索更多過年菜肴🫕，豐富你的年節餐桌❗",
                        actions=[
                            URIAction(
                                label="探索更多食譜",
                                uri="https://icook.tw/categories/50"
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
        'info_nian_beast': '年獸 是一種傳說中的怪物，每逢除夕會出來騷擾人們。後來人們發現它害怕紅色、火光與聲響，便有了放鞭炮的習俗。',
        'info_reunion_dinner': '團圓飯 是除夕夜全家團聚共享的晚餐，象徵家人團聚、幸福美滿。常見的菜色包括魚、雞、年糕等，寓意美好祝願。',
        'info_firecracker': '放鞭炮 是過年期間的重要習俗，聲響可以驅走年獸與邪氣，同時增添節日的熱鬧氣氛。',
        'info_new_clothes': '過年穿新衣 象徵除舊佈新，迎接新的一年的新氣象，也帶來嶄新的希望。',
        'info_upside_down_fu': '倒貼福字 是過年一種有趣的習俗，“福倒了”與“福到了”諧音，寓意福氣到來，增添節日的喜慶氣氛。',
        'info_spring_cleaning': '過年大掃除 是農曆年前的傳統習俗，清理家中的灰塵與舊物，象徵送走過去的不順，迎接全新的開始。',
        'info_new_year_food': '過年菜肴 象徵著對新年的美好祝願，如魚代表“年年有餘”，長年菜寓意“長長久久”，年糕則寓意“步步高升”。'
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




