from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)

app = Flask(__name__)

line_bot_api = LineBotApi('E4ABmKEmT3dLY53SL8AV2UhvlQh16gWPFCBI086NfByC7O1+odYU/i6K/JPAOVCLh8bygVtlNRP8ZCnY4Gx1QvNagk4eN/0gwfDzDGhUQ/T4JjPD8tEoBbZiCubTH1Uyxvi23Im9stUDxiQMzthQnwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1c8b7fb623926e7f7f22af4554ebf6d9')

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/webhook", methods=['POST'])
def webhook():
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
    

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
