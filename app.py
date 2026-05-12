import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv
from modules.user_state import UserState
from modules.wishlist import view_wishlist, add_to_wishlist
from modules.product_query import handle_product_query

load_dotenv() [cite: 18]

app = Flask(__name__) [cite: 19]

# 初始化 Line Bot 配置 [cite: 21]
line_bot_api = LineBotApi(os.environ.get('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('LINE_CHANNEL_SECRET'))

user_states = {} # 存儲用戶狀態 [cite: 29]

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature'] [cite: 23]
    body = request.get_data(as_text=True) [cite: 25]
    try:
        handler.handle(body, signature) [cite: 26]
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id [cite: 28]
    text = event.message.text.strip()

    # 初始化狀態機 [cite: 29]
    if user_id not in user_states:
        user_states[user_id] = UserState()
    
    user_state = user_states[user_id]

    # 處理指令 [cite: 31]
    if text == "查看願望清單":
        view_wishlist(line_bot_api, event.reply_token, user_id)
    elif text.startswith("添加到願望清單:"):
        add_to_wishlist(line_bot_api, event.reply_token, user_id, text)
    else:
        # 預設進行產品查詢 [cite: 129]
        handle_product_query(line_bot_api, event.reply_token, text)

if __name__ == "__main__":
    app.run()
