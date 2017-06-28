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
from crawler import getCaseJobArticles,triggerCrawler,getDiscussionArticles
app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])
triggerCrawler()


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
    if event.message.text.lower() in ['codejob','soho','nctu_talk']:
        if event.message.text.lower() == 'codejob':
            board = 'CodeJob'
        elif event.message.text.lower() == 'soho':
            board = 'soho'
        elif event.message.text.lower() == 'nctu_talk':
            board = 'NCTU_TALK'

        aritcles = getCaseJobArticles(board)
        action_list = []
        for article in aritcles:
            action_list.append(URITemplateAction(
                label=article['title'],
                uri='https://www.ptt.cc'+article['link']))
        buttons_message = TemplateSendMessage(
                alt_text='PTT {0}'.format(board),
                template=ButtonsTemplate(
                    thumbnail_image_url='https://i.imgur.com/prgAiYk.jpg',
                    title='PTT {0}'.format(board),
                    text='選選選',
                    actions=action_list)
        )
        line_bot_api.reply_message(
            event.reply_token,
            buttons_message
        )
        return 0
    if event.message.text.lower() in ['tech_job','soft_job','stupidclown']:
        if event.message.text.lower() == 'tech_job':
            board = 'Tech_job'
        elif event.message.text.lower() == 'soft_job':
            board = 'Soft_Job'
        elif event.message.text.lower() == 'stupidclown':
            board = 'StupidClown'
        
        aritcles = getDiscussionArticles(board)
        action_list = []
        for article in aritcles:
            action_list.append(URITemplateAction(
                label=article['title'],
                uri='https://www.ptt.cc'+article['link']))
        buttons_message = TemplateSendMessage(
            alt_text='PTT {0}'.format(board),
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/WBdWmBt.jpg',
                title='PTT {0}'.format(board),
                text='選選選',
                actions=action_list
            )
        )
        line_bot_api.reply_message(
            event.reply_token,
            buttons_message
        )
        return 0
    
    caseJobBoard = CarouselColumn(
        thumbnail_image_url='https://i.imgur.com/tUiZQdV.png',
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
            MessageTemplateAction(
                label='NCTU_TALK',
                text='NCTU_TALK'
                )
        ]
    )
    discussionBoard = CarouselColumn(
        thumbnail_image_url='https://i.imgur.com/QgxjXUf.jpg',
        title='Discussion board',
        text='Please select',
        actions=[
            MessageTemplateAction(
                label='Soft Job',
                text='Soft_job'
                ),
            MessageTemplateAction(
                label='Tech Job',
                text='Tech_job'
                ),
            MessageTemplateAction(
                label='StupidClown',
                text='StupidClown'
                )
        ]
    )
    carousel_template_message = TemplateSendMessage(
        alt_text='PTT cralwer',
        template=CarouselTemplate(
            columns=[
                caseJobBoard,
                discussionBoard
            ]
        )
    )
    print(carousel_template_message)
    line_bot_api.reply_message(
        event.reply_token,
        carousel_template_message)

@handler.default()
def default(event):
    print(event)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Currently Not Support None Text Msg'))
    pass

if __name__ == "__main__":
    app.run()
