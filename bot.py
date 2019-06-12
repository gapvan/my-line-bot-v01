import os
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (LineBotApiError,InvalidSignatureError)
from linebot.models import (MessageAction,ImagemapArea,URIImagemapAction,MessageImagemapAction,BaseSize,MessageEvent,TextMessage,ImageMessage,ImageSendMessage,ImagemapSendMessage,TextSendMessage,SourceUser,SourceGroup,SourceRoom,RichMenu,RichMenuSize,RichMenuArea,RichMenuBounds,URIAction)

app = Flask(__name__)
keep_uid = ""
line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])
users = [['oorben','?U60e0f8b22c313b3971d50c2bce9dbaa9'],['gap','U9f6b4dfa2e30a22ad6a282dc34a86de2']]
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
    keep_uid = str(event.source)[str(event.source).find('userId')+10:str(event.source).find('"',str(event.source).find('userId')+10)]
    profile = line_bot_api.get_profile(str(keep_uid))
    displayName = str(profile)[str(profile).find('displayName')+15:str(profile).find('"',str(profile).find('displayName')+15)]
        
    if text == 'Profile':
        line_bot_api.push_message('U9f6b4dfa2e30a22ad6a282dc34a86de2', TextSendMessage(text=str(profile)))
    elif text == 'Hi':
        line_bot_api.reply_message(
            event.reply_token,TextSendMessage(text='hi '+str(displayName)))      
    elif text == 'Register':
        line_bot_api.push_message('U9f6b4dfa2e30a22ad6a282dc34a86de2', TextSendMessage(text=displayName+':'+keep_uid))
    elif text == 'Excel':
        line_bot_api.reply_message(
            event.reply_token,TextSendMessage(text='https://drive.google.com/open?id=1c_Gmmq19LMgDsdBNzo46F1zt_rWp8RXv'))
    elif text == 'Image':
##        line_bot_api.reply_message(
##            event.reply_token,ImageSendMessage(
##                original_content_url='https://raw.githubusercontent.com/gapvan/my-line-bot-v01/master/menu.png',
##                preview_image_url='https://raw.githubusercontent.com/gapvan/my-line-bot-v01/master/menu.png'))
        line_bot_api.reply_message(
            event.reply_token,ImagemapSendMessage(
                base_url='https://raw.githubusercontent.com/gapvan/my-line-bot-v01/master/menu.png?w=1040',
                alt_text='Image',
                base_size=BaseSize(height=1040, width=1040),
                actions=[
                    #URIImagemapAction(link_uri='https://www.facebook.com',
                    MessageImagemapAction(text='full menu',
                        area=ImagemapArea(x=0, y=0, width=1040, height=1040))]
            )
        )
    elif text == 'MeetingRoom':
        line_bot_api.reply_message(
            event.reply_token,ImageSendMessage(
                original_content_url='https://raw.githubusercontent.com/gapvan/my-line-bot-v01/master/RIS_Meeting_Room.jpg',
                preview_image_url='https://raw.githubusercontent.com/gapvan/my-line-bot-v01/master/RIS_Meeting_Room.jpg'))
    elif text == 'Monitor':
        line_bot_api.reply_message(
            event.reply_token,ImagemapSendMessage(
                base_url='https://raw.githubusercontent.com/gapvan/my-line-bot-v01/master/monitor_task.png?w=1040',
                alt_text='monitor_task',
                base_size=BaseSize(height=1040, width=1040),
                actions=[
                    #URIImagemapAction(link_uri='https://www.facebook.com',
                    MessageImagemapAction(text='WPRS',
                        area=ImagemapArea(x=0, y=0, width=347, height=520)),
                    MessageImagemapAction(text='CNSGNSALE1',
                        area=ImagemapArea(x=347, y=0, width=347, height=520)),
                    MessageImagemapAction(text='STSALE',
                        area=ImagemapArea(x=694, y=0, width=347, height=520)),
                    MessageImagemapAction(text='CNSGNSALE',
                        area=ImagemapArea(x=0, y=521, width=347, height=520)),
                    MessageImagemapAction(text='ยังไม่เปิดใช้งานครับ',
                        area=ImagemapArea(x=347, y=521, width=347, height=520)),
                    MessageImagemapAction(text='ยังไม่เปิดใช้งานครับ',
                        area=ImagemapArea(x=694, y=521, width=347, height=520))]
            )
        )
    elif text == 'WPRS':
        chk_permission = 0
        for i in range(len(users)) :  
            if (users[i][0] == displayName) & (users[i][1] == keep_uid) :
                chk_permission = 1
        if chk_permission :
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='WPRS'))
        else :
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='คุณไม่มีสิทธิ์เข้าใช้งาน WPRS ได้ครับ'))
    elif text == 'Menu':
        rich_menu_to_create = RichMenu(
            size=RichMenuSize(width=800, height=540),
            selected=False,
            name="Main Menu",
            chat_bar_text="Tap here",
            areas=[(RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=266, height=270),
                action=MessageAction(label="moniter", text="Monitor"))),
                (RichMenuArea(
                bounds=RichMenuBounds(x=267, y=0, width=267, height=270),
                action=MessageAction(label="report", text="ยังไม่เปิดใช้งานครับ"))),
                (RichMenuArea(
                bounds=RichMenuBounds(x=533, y=0, width=267, height=270),
                action=URIAction(label='cnext', uri='https://passport.central.co.th/adfs/ls/IdpInitiatedSignOn.aspx?loginToRp=https://www.successfactors.com/CENTRAL'))),
		(RichMenuArea(
                bounds=RichMenuBounds(x=0, y=271, width=266, height=270),
                action=URIAction(label='issue', uri='https://ris6789.central.co.th/arsys/shared/login.jsp?/arsys/'))),
                (RichMenuArea(
                bounds=RichMenuBounds(x=267, y=271, width=267, height=270),
                action=MessageAction(label=" ", text="ยังไม่เปิดใช้งานครับ"))),
                (RichMenuArea(
                bounds=RichMenuBounds(x=533, y=271, width=267, height=270),
                action=MessageAction(label="meetingroom", text="MeetingRoom")))				
                ]
        )
        rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
        print(rich_menu_id)    
        with open('.//main_menu.png', 'rb') as f:
            line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)         
        line_bot_api.link_rich_menu_to_user(keep_uid, rich_menu_id)
##        line_bot_api.reply_message(
##            event.reply_token,TextSendMessage(text=str(rich_menu_id)))
    else:
        print(event.message.text)
##        line_bot_api.reply_message(
##            event.reply_token,TextSendMessage(text=event.message.text))
        
if __name__ == "__main__":
    app.run()
