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

@handler.add(FollowEvent)
def followed_message(event):
    # # フォローされた場合にメッセージを送信する(定型文を設定しているのでコメントアウト)
    # message = TextSendMessage(text='フォローありがとうございます')
    # line_bot_api.reply_message(event.reply_token, messages=message)

    # DB登録処理
    profile = line_bot_api.get_profile(event.source.user_id)
    user = session.query(Users).get(profile.user_id)
    # ユーザーがDBに登録されていない場合は新規登録
    if user is None:
        row = Users(user_id=profile.user_id, name=profile.display_name)
        session.add(row)
        session.commit()
    # DBに登録済の場合、情報を更新
    else:
        user.user_id = profile.user_id
        user.name = profile.display_name
        user.del_flag = False
        session.commit()

@handler.add(MessageEvent, message=TextMessage)
def response_message(event):
    # 翌日の天気予報を取得
    weather = wr.getWeatherReport(1)
    # 返信メッセージ
    messages = TextSendMessage(text=('明日の千葉の天気をお知らせします\n{0}').format(weather))
    line_bot_api.reply_message(event.reply_token,messages)

def push_message():

    # 当日の天気予報を取得
    weather = wr.getWeatherReport(0)

    # 全ユーザー取得
    users = session.query(Users).all()
    for user in users:
        if user.del_flag:
            continue

        user_id = user.user_id
        # DB登録時から情報が変更されている可能性があるので、チェックを実施する
        profile = line_bot_api.get_profile(user_id)
        if user.name != profile.display_name:
            user.name = profile.display_name
            session.commit()

        messages = TextSendMessage(text=(
            '{0}さん、おはようございます！\n\n'\
            '本日の千葉の天気をお知らせします\n{1}'
            ).format(profile.display_name, weather))
        line_bot_api.push_message(user_id, messages=messages)

def user_all():
    users = session.query(Users).all()
    for user in users:
        print('==============================')
        print('user_id: ' + user.user_id)
        print('name: ' + user.name)
        print('==============================')

def user_insert():
    row = Users(user_id='U75a1e09719ff2f7e2cbfeaf77ebb3039', name='sekine')
    session.add(row)
    session.commit()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)