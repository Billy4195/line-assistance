from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage,
    ButtonsTemplate
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, URITemplateAction, PostbackTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)
import os
from crawler import pttCrawler
app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event.message)
    if event.message.text == 'CodeJob':
        pttCrawler('CodeJob')
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Hello CodeJob'))
        return 0

    if event.message.text == 'soho':
        pttCrawler('soho')
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Hello soho'))
        return 0

    buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://example.com/image.jpg',
                title='Menu',
                text='Please select',
                actions=[
                MessageTemplateAction(
                    label='CodeJob',
                    text='CodeJob'
                    ),
                MessageTemplateAction(
                    label='soho',
                    text='soho'
                    ),
                URITemplateAction(
                    label='uri',
                    uri='http://example.com/'
                    )
                ]
                )
    )
    line_bot_api.reply_message(
        event.reply_token,
        buttons_template_message)

@handler.default()
def default(event):
    print(event)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Currently Not Support None Text Msg'))
    pass


if __name__ == "__main__":
    app.run()
