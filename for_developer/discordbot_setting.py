import csv

TOKEN_file = 'TOKEN.txt' # 自分のBotのアクセストークン
Synthax_file = 'Synthax_setting.csv' # 自分のBotのアクセストークン
voibox_version = 'v20220313'

# アクセストークンの読み取り
with open(TOKEN_file,'r', encoding='utf-8') as f:
      TOKEN = f.read()
      f.close()



# Synthax情報を読み込む
with open(Synthax_file, 'r', encoding='utf-8') as f:
      other_bots_Synthax = []
      reader = csv.reader(f)
      for row in reader:
            if not row:
                  continue
            if row[0] == 'command_Synthax':
                  command_Synthax = row[1]
            elif row[0] == 'comment_Synthax':
                  comment_Synthax = row[1]
            elif row[0] == 'other_bots_Synthax':
                  other_bots_Synthax.append(row[1])

# VOICEVOX音声再生（.bat）ファイルへのパス
bat_json = "output_json_from_VOICEVOX.bat"   
bat_voice = "output_voice_from_VOICEVOX.bat"   

#各種ファイルへのパス(discordbot.pyからみた相対パス)
voice_file = "tmp/tmp_voice.wav"      # VOICEVOX音声の保存先
json_file = 'tmp/query.json'          # jsonファイルへのパス
vlist_file = "data/voice_list.csv"    # ユーザー毎のボイスリスト 
flist_file = "data/flag_list.csv"
wlist_file = "data/word_list.csv"     # 単語帳
clist_file = "data/command_list.txt"  # コマンドリスト
SE_file = "SE_list.csv"               # SEリスト
image_file = "image_list.csv"         # 画像リスト
pie_data = 'pie_data.txt'             # パイ練り記録

# 各種フラグのデフォルト値
inform_someone_come = True     # 入退出の通知
time_signal         = True     # 時報
read_name           = False    # 話者の名前を読み上げる。
number_of_people    = True    # 在室人数チェック
auto_leave          = True    # ボイスチャンネルから自動的に退出する
SE_on               = True    # SE機能をオンにする
auto_fire           = True   # 自動発火機能
word_count_limit = 50

# 各種コマンド(変更した場合はcommand_list.txtを書き換えてください。)
command_hello               = command_Synthax + 'hello'
command_help                = command_Synthax + 'help'
command_join                = command_Synthax + 'join'
command_leave               = command_Synthax + 'leave'
command_wlist               = command_Synthax + 'wlist'
command_chg_my_voice        = command_Synthax + 'chg_my_voice'
command_inform_someone_come = command_Synthax + 'inform_someone_come'
command_time_signal         = command_Synthax + 'time_signal'
command_read_name           = command_Synthax + 'read_name'
command_number_of_people    = command_Synthax + 'number_of_people'
command_auto_leave          = command_Synthax + 'auto_leave'
command_word_count_limit    = command_Synthax + 'word_count_limit'
command_chg_speed           = command_Synthax + 'chg_speed'
command_show_setting        = command_Synthax + 'show_setting'
command_reload              = command_Synthax + 'reload'
command_stop                = command_Synthax + 'stop'


# VOICEVOXのボイス情報
speker_id_dict = {("metan", "amaama"): '0', ("metan", "normal"): '2', ("metan", "sexy"): '4', ("metan", "tsun"): '6',
                  ("zundamon", "amaama"): '1', ("zundamon", "normal"): '3', ("zundamon", "sexy"): '5', ("zundamon", "tsun"): '7',
                  ("tsumugi", "normal"): '8', ("ritsu", "normal"): '9', ("hau", "normal"): '10',
                  ("takehiro", "normal"): '11', ("torataro", "normal"): '12', ("ryusei", "normal"): '13',
                  ("himari", "normal"): '14'}

# テンプレートコメントリスト
comment_dict = {'message_reload': comment_Synthax + '更新完了',
                'message_err': comment_Synthax + 'コマンドが間違っているのだ',
                'message_join': comment_Synthax + "接続したのだ。よろしくなのだ。",
                'message_leave': comment_Synthax + "僕はこれで失礼するのだ。ばいばーい",
                'message_chg_voice': comment_Synthax + "ボイスの変更を行いました",
                'message_not_actualized': comment_Synthax + "まだ実装されていないです",}

# 拡張子リスト
extension_dict = {".jpg": "画像ファイル", ".jpng": "画像ファイル", ".jpe": "画像ファイル", ".ico": "画像ファイル",
                  ".png": "画像ファイル", ".bmp": "画像ファイル", ".tif": "画像ファイル", ".tiff": "画像ファイル",
                  ".mp3": "音声ファイル", ".wma": "音声ファイル", ".wav": "音声ファイル", ".mid": "音声ファイル",".midi": "音声ファイル",
                  ".avi": "動画ファイル", ".mp4": "動画ファイル", ".wmv": "動画ファイル",
                  ".exe": "実行ファイル", ".dll": "実行ファイル", 
                  ".pdf": "PDFファイル", ".doc": "ワードファイル", ".csv": "シーエスブイファイル",  ".xls": "エクセルファイル", ".ppt": "パワーポイントファイル", ".pps": "パワーポイントファイル",
                  ".clip": "クリスタファイル", ".psd": "PSDファイル",
                  ".txt": "テキストファイル", ".html": "テキストファイル",".htm": "テキストファイル",
                  ".shtml": "テキストファイル", ".css": "テキストファイル",
                  ".zip": "圧縮ファイル", ".lzh": "圧縮ファイル"}

# 時報のセリフリスト
time_signal_dict = {'00:00': '日付が変わったのだ。まだ寝ないのだ？',
                    '01:00': 'ずんだもんが午前1時ぐらいをお知らせするのだ',
                    '02:00': 'ずんだもんが午前2時ぐらいをお知らせするのだ。眠い・・・',
                    '03:00': 'ずんだもんが午前3時ぐらいをお知らせするのだ',
                    '04:00': 'おはようなのだ!朝4時に何してるのだ？',
                    '05:00': 'ずんだもんが午前5時ぐらいをお知らせするのだ',
                    '06:00': 'ずんだもんが午前6時ぐらいをお知らせするのだ',
                    '07:00': 'ずんだもんが午前7時ぐらいをお知らせするのだ。朝ごはんの時間なのだ',
                    '08:00': 'ずんだもんが午前8時ぐらいをお知らせするのだ',
                    '09:00': 'ずんだもんが午前9時ぐらいをお知らせするのだ',
                    '10:00': 'ずんだもんが午前10時ぐらいをお知らせするのだ',
                    '11:00': 'ずんだもんが午前11時ぐらいをお知らせするのだ',
                    '12:00': 'ずんだもんが正午をお知らせするのだ。作業を中断してそろそろお昼にするのだ',
                    '13:00': 'ずんだもんが午後1時ぐらいをお知らせするのだ',
                    '14:00': 'ずんだもんが午後2時ぐらいをお知らせするのだ',
                    '15:00': 'ずんだもんが午後3時ぐらいをお知らせするのだ',
                    '16:00': 'ずんだもんが午後4時ぐらいをお知らせするのだ',
                    '17:00': 'ずんだもんが午後5時ぐらいをお知らせするのだ',
                    '18:00': 'ずんだもんが午後6時ぐらいをお知らせするのだ',
                    '19:00': 'ずんだもんが午後7時ぐらいをお知らせするのだ',
                    '20:00': 'ずんだもんが午後8時ぐらいをお知らせするのだ。お腹がすいてきたから晩ごはんを食べてくるのだ',
                    '21:00': 'ずんだもんが午後9時ぐらいをお知らせするのだ',
                    '22:00': 'ずんだもんが午後10時ぐらいをお知らせするのだ',
                    '23:00': 'ずんだもんが午後11時ぐらいをお知らせするのだ'}



# コマンドリスト
help_message = "```"+\
                       "■基本コマンド \n" +\
                       command_Synthax + "join: BOTをボイスチャンネルに呼ぶ \n" + \
                       command_Synthax + "leave: BOTをボイスチャンネルから退出させる \n" +\
                       command_Synthax + "stop: 音声ストップ \n" +\
                       command_Synthax + "hello: バージョン情報確認 \n\n" +\
                       "■辞書コマンド \n" +\
                       command_Synthax + "wlist add A B: 読み仮名の登録。AをBと読ませる。 \n" + \
                       command_Synthax + "wlist delete A: 辞書登録の削除。 \n" +\
                       command_Synthax + "wlist show: 辞書登録の確認 \n\n" +\
                       "■調声コマンド \n" +\
                       command_Synthax + "chg_my_voice: ボイス変更。!chg_my_voice A B \n" + \
                       "A: zundamon, metan, tsumugi, ritsu, hau \n" +\
                       "B: normal, amaama, sexy, tsun \n" +\
                       "注意: tsumugi,ritsu,hauはnormalしか実装されていない。\n" +\
                       command_Synthax + "chg_speed: 音声再生スピード変更。!chg_speed Aで設定。Aは0.5から2.0までの実数。 \n\n" +\
                       "■各種設定 \n" +\
                       command_Synthax + "inform_someone_come: 入退出通知のオンオフ。 \n" + \
                       command_Synthax + "time_signal: 時報のオンオフ \n" +\
                       command_Synthax + "read_name: 名前読み上げのオンオフ \n" +\
                       command_Synthax + "number_of_people: 接続人数のチェックオンオフ\n" +\
                       command_Synthax + "auto_leave: BOTの自動退出のオンオフ\n" +\
                       command_Synthax + "word_count_limit A: 文字数制限の設定\n" +\
                       command_Synthax + "show_setting: 現在の設定の確認\n" +\
                       "```"
version_info = comment_Synthax + 'ずんだもんは現在起動中なのだ！(バージョン' + voibox_version + ')\n' +\
               comment_Synthax + command_Synthax + 'joinで呼び出してくれたらすぐに参加するのだ！'

