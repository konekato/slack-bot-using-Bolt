import os
import re
import random
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# ボットトークンとソケットモードハンドラーを使ってアプリを初期化します
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.message(re.compile("shift (.*)"))
def shift(say, context):
    # message.react('+1')

    list = context['matches'][0].split()

    # Validations
    #  第一引数チェック
    try:
        num_of_groups = int(list[0])
    except:
        say(f'第1引数<グループ数>には数値を入力してね！\n"{list[0]}"はダメだよ！')
        # message.react('sweat')
        return

    members = list[1:] # メンバー名のリスト
    num_of_members = len(members)

    #  グループ数 <= メンバー數 であるかチェック
    if num_of_groups > num_of_members:
        say(f'<グループ数>がメンバー数よりも大きいのはだめだよ！うまく分けられないからね！')
        # message.react('sweat')
        return
    
    say('シフトを振り分けるよ！')
    random.shuffle(members) # リスト内シャッフル
    
    num_of_members_per_group = int(num_of_members / num_of_groups) # グループあたりの人數
    rem = num_of_members % num_of_groups # 余り
    start = 0
    for group_num in range(num_of_groups):
        end = start + num_of_members_per_group
        if rem > 0:
            end += 1
            rem -= 1
        members_by_group = members[start:end]
        
        msg = '```'
        msg += f'【グループ{group_num+1}】\n'
        for member in members_by_group:
            msg += f'・{member}\n'
        msg += '```'

        say(msg)

        start = end

    say('シフト振り分け終わったよ！')


# アプリを起動します
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()