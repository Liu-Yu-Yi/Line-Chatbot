import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv

# 載入功能模組 (這些檔案您稍後會建立在 modules/ 資料夾中)
from modules.user_state import UserState
from modules.wishlist import add_to_wishlist, view_wishlist
from modules.product_query import handle_product_query

# 載入 .env 檔案（本地測試用）
load_dotenv()

app = Flask(__name__)

# 從環境變數取得金鑰
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

# 用於儲存每個用戶的對話狀態
user_states = {}

@app.route("/callback", methods=['POST'])
def callback():
    # 驗證 LINE 的簽章
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_input = event.message.text.strip()

    # 初始化用戶狀態
    if user_id not in user_states:
        user_states[user_id] = UserState()
    
    state = user_states[user_id]

    # 1. 處理願望清單功能
    if user_input == "查看願望清單":
        response_text = view_wishlist(user_id)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_text))
    
    elif user_input.startswith("加入清單:"):
        product_name = user_input.replace("加入清單:", "").strip()
        response_text = add_to_wishlist(user_id, product_name)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_text))

    # 2. 處理 3C 產品查詢 (呼叫 OpenAI GPT-4.1)
    else:
        # 顯示「處理中」狀態，增加使用者體驗
        reply_content = handle_product_query(user_input)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_content))

if __name__ == "__main__":
    # Render 部署時會自動使用 port 5000 或環境變數指定的 port
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
