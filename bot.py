from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (LineBotApiError,InvalidSignatureError)
from linebot.models import (MessageEvent,TextMessage,TextSendMessage,SourceUser,SourceGroup,SourceRoom,RichMenu,RichMenuSize,RichMenuArea,RichMenuBounds,URIAction)

app = Flask(__name__)
keep_uid = ""
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
    if text == 'Profile':
        #if isinstance(event.source, SourceUser):
##        line_bot_api.reply_message(
##            event.reply_token,TextSendMessage(text="ok"))
##        line_bot_api.reply_message(
##            event.reply_token,TextSendMessage(text="บ้าบอ"))
        keep_uid = str(event.source)[str(event.source).find('userId')+10:str(event.source).find('"',str(event.source).find('userId')+10)]
##        line_bot_api.reply_message(
##            event.reply_token,TextSendMessage(text=str(keep_uid)))
##        line_bot_api.reply_message(
##            event.reply_token,TextSendMessage(text=event.source.type))
##        line_bot_api.reply_message(
##            event.reply_token,TextSendMessage(text=event.source.userId))
        
        profile = line_bot_api.get_profile(str(keep_uid))
        line_bot_api.reply_message(
            event.reply_token,TextSendMessage(text=str(profile)))
##        line_bot_api.reply_message(
##            event.reply_token, [
##                TextSendMessage(text='Display name: ' + profile.display_name),
##                TextSendMessage(text='user_id: ' + profile.user_id),
##                TextSendMessage(text='picture_url: ' + profile.picture_url),
##                TextSendMessage(text='Status message: ' + profile.status_message)  
##            ]
##        )
##        print(profile.display_name)
##        print(profile.user_id)
##        print(profile.picture_url)
##        print(profile.status_message)

##        profile = line_bot_api.get_profile(event.source.user_id)
##        line_bot_api.reply_message(
##            event.reply_token, [
##                TextSendMessage(text='Display name: ' + profile.display_name),
##                TextSendMessage(text='Status message: ' + profile.status_message)
##            ]
##        )
##        else:
##            line_bot_api.reply_message(
##                event.reply_token,
##                TextSendMessage(text="Bot can't use profile API without user ID"))
    elif text == 'Hi':
        keep_uid = str(event.source)[str(event.source).find('userId')+10:str(event.source).find('"',str(event.source).find('userId')+10)]
        profile = line_bot_api.get_profile(str(keep_uid))
        displayName = str(profile)[str(profile).find('displayName')+15:str(profile).find('"',str(profile).find('displayName')+15)]
#str(event.source).find('"',str(event.source).find('displayName')+15)
        line_bot_api.reply_message(
            event.reply_token,TextSendMessage(text='hi '+str(displayName)))
            #event.reply_token,TextSendMessage(text='hi '+str(displayName)))
    elif text == 'Excel':
        line_bot_api.reply_message(
            event.reply_token,TextSendMessage(text='https://drive.google.com/open?id=1c_Gmmq19LMgDsdBNzo46F1zt_rWp8RXv'))
    elif text == 'Image':
        line_bot_api.reply_message(
            event.reply_token,TextSendMessage(text='https://drive.google.com/open?id=1h1e1iLJ20LgH2H_nqR1FWE1bmJ_Ks9md'))
    elif text == 'Menu':
        rich_menu_to_create = RichMenu(
            size=RichMenuSize(width=800, height=270),
            selected=False,
            name="Nice richmenu",
            chat_bar_text="Tap here",
            areas=[(RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=266, height=270),
                action=URIAction(label='facebook', uri='https://www.facebook.com'))),
                (RichMenuArea(
                bounds=RichMenuBounds(x=267, y=0, width=267, height=270),
                action=URIAction(label='youtube', uri='https://www.youtube.com'))),
                (RichMenuArea(
                bounds=RichMenuBounds(x=533, y=0, width=267, height=270),
                action=URIAction(label='twitter', uri='https://twitter.com')))
                ]
        )
        rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
        print(rich_menu_id)
        
        with open('.//sample_menu 002.png', 'rb') as f:
            line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)
                
        keep_uid = str(event.source)[str(event.source).find('userId')+10:str(event.source).find('"',str(event.source).find('userId')+10)]
        line_bot_api.link_rich_menu_to_user(keep_uid, rich_menu_id)
        line_bot_api.reply_message(rich_menu_id)

    else:
        line_bot_api.reply_message(
            event.reply_token,TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
