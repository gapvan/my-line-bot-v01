from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, SourceUser, SourceGroup)

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
def handle_text_message(event):
    text = event.message.text
    
##    if text == 'menu':
##        rich_menu_to_create = RichMenu(
##        size=RichMenuSize(width=2500, height=843),
##        selected=False,
##        name="Nice richmenu",
##        chat_bar_text="Tap here",
##        areas=[RichMenuArea(
##            bounds=RichMenuBounds(x=0, y=0, width=2500, height=843),
##            action=URIAction(label='Go to line.me', uri='https://line.me'))]
##        )
##        rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
##        line_bot_api.link_rich_menu_to_user(user_id, rich_menu_id)
##        print(rich_menu_id)
    if text == 'profile':
        #if isinstance(event.source, SourceUser):
        profile = line_bot_api.get_profile(event.source.user_id)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='Display name: ' + profile.display_name),
                TextSendMessage(text='Status message: ' + profile.status_message)
            ]
        )
##        else:
##            line_bot_api.reply_message(
##                event.reply_token,
##                TextSendMessage(text="Bot can't use profile API without user ID"))
    elif text == 'chk':
        line_bot_api.reply_message(
            event.reply_token,TextSendMessage(text="no"))        
    else:
        line_bot_api.reply_message(
            event.reply_token,TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
