import os
import datetime
import weather_report as wr
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent)
from assets.database import session
from assets.models import Users

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

dt_now = datetime.datetime.now()


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def response_message(event):
    print('response_message has called')
    print('userId : {0}'.format(event.source.user_id))
    # 返信メッセージ
    line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=event.message.text))

@handler.add(FollowEvent)
def followed_message(event):
    print('followed_message has called')
    print('userId : {0}'.format(event.source.user_id))
    # フォローされた場合にメッセージを送信する
    message = TextSendMessage(text='フォローありがとうございます')
    line_bot_api.reply_message(event.reply_token, messages=message)

    # DB登録処理
    row = Users(user_id=event.source.user_id)
    # TODO: ユーザ情報取得API -> https://developers.line.biz/ja/reference/messaging-api/#get-profile
    session.add(row)
    session.commit()


def push_message():
    # user_id = "U75a1e09719ff2f7e2cbfeaf77ebb3039"
    print('push_message has called')
    print('userId : user_id')

    # 当日の天気予報を取得
    weather = wr.getWeatherReport()

    # 全ユーザー取得
    users = session.query(Users).all()
    for user in users:
        user_id = user.user_id
        messages = TextSendMessage(text=(
            '{0}さん、おはようございます！\n'\
            'テスト用のPUSHメッセージです\n\n現在の日時:{1}\n\n本日の千葉の天気\n{2}'
            ).format(user.name, dt_now.strftime('%Y年%m月%d日 %H:%M:%S'), weather))
        line_bot_api.push_message(user_id, messages=messages)


    # user = session.query(User).get(user_id)
    # if (user is None):
    #     print('userは未登録です')
    # else:
    #     print('userは登録済みです\n')
    #     print('userId:' + user.user_id)
    # for user in users:
    #     print('userId:' + user.user_id)
    #     if (user.del_flag):
    #         print('del_flag:true')
    #     else:
    #         print('del_flag:false')

    


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)