from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

app = Flask(__name__)

# 環境変数取得
# LINE Developersで設定されているアクセストークンとChannel Secretをを取得し、設定します。
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
 
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)
 

## 1 ##
# Webhookからのリクエストをチェックします。
@app.route("/callback", methods=['POST'])
def callback():
    # リクエストヘッダーから署名検証のための値を取得
    signature = request.headers['X-Line-Signature']

    # リクエストボディを取得
    body = request.get_data(as_text=True)
    #app.logger.info("Request body: " + body)

    # handle webhook body
    # 署名を検証し、問題なければhandleに定義されている〜〜
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

##20200712一旦オウム返しに戻すため、コメントアウト
#@app.route("/index", methods=['POST'])
#def index():
#    return 'OK'

## 2 ##
###############################################
#LINEのメッセージの取得と返信内容の設定(オウム返し)
###############################################
 
#LINEでMessageEvent（普通のメッセージを送信された場合）が起こった場合に、
#def以下の関数を実行します。
#reply_messageの第一引数のevent.reply_tokenは、イベントの応答に用いるトークンです。 
#第二引数には、linebot.modelsに定義されている返信用のTextSendMessageオブジェクトを渡しています。
 
#inquiry_text = "お問合せ内容を選択してください。\n1.福利厚生について\n2.規則について\n3.手当について\n3-1.家賃補助について\n3-2.資格手当について\n4.手続きについて"
inquiry_list = {
     '福利厚生' : '○○○○',
     '手続き' : '◇◇◇◇',
     '規則' : 'XXXX',
     '手当' : '番号をお選びください（1:家賃補助、2:資格手当）',
     '1': '家賃補助について',
     '2': '資格手当について', 
}

# TODO:ユーザIDを取得し、質問羅列→回答の順番にできるようにしたい↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
# user_id_list = []

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     if event.message.text == "質問":
#         print(event)
#         user_id_list.append(event.source.userId)
#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage(text=inquiry_text))
#     elif event.message.text in inquiry_list.keys():
#         if event.source.userId in user_id_list:
#             user_id_list.remove(event.source.userId)
#             line_bot_api.reply_message(
#                 event.reply_token,
#                 TextSendMessage(text=inquiry_list[event.message.text]))
#         else:
#             user_id_list.append(event.source.userId)
#             line_bot_api.reply_message(
#                 event.reply_token,
#                 TextSendMessage(text=inquiry_text))
#     else:
#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage(text=event.message.text)) #ここでオウム返しのメッセージを返します。

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "質問":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=inquiry_text))
    elif event.message.text in inquiry_list.keys():
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=inquiry_list[event.message.text]))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)) #ここでオウム返しのメッセージを返します。

# ポート番号の設定
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
