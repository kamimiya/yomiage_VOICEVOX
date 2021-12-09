
import csv

TOKEN_file = 'TOKEN.txt' # 自分のBotのアクセストークン
Synthax_file = 'Synthax_setting.csv' # 自分のBotのアクセストークン


# アクセストークンの読み取り
with open(TOKEN_file,'r', encoding='utf-8') as f:
    TOKEN = f.read()
    f.close()
    

# シンタックス(変更した場合はcommand_list.txtを書き換えてください。)
command_Synthax = '!' #コマンドの先頭に付ける記号
comment_Synthax = '>' #読み上げられたくない文の先頭に付ける記号

# Synthax情報を読み込む
with open(Synthax_file, 'r', encoding='utf-8') as f:
      reader = csv.reader(f)
      for row in reader:
            if not row:
                  continue
            if row[0] == 'command_Synthax':
                  command_Synthax = row[1]
            elif row[0] == 'comment_Synthax':
                  comment_Synthax = row[1]
    
# VOICEVOXのボイス情報{('キャラ名','声種'): 'VOICEVOX側で対応する番号'}
speker_id_list = {('metan', 'amaama'): '0', ('metan', 'normal'): '2', ('metan', 'sexy'): '4', ('metan', 'tsun'): '6',\
                  ('zundamon', 'amaama'): '1', ('zundamon', 'normal'): '3', ('zundamon', 'sexy'): '5', ('zundamon', 'tsun'): '7',\
                  ('tsumugi', 'normal'): '8', ('ritsu', 'normal'): '9'}

# 拡張子リスト{'拡張子名: 'ファイル種別'}
extension_list = {'.jpg': '画像ファイル', '.jpng': '画像ファイル', '.jpe': '画像ファイル', '.ico': '画像ファイル',\
                  '.png': '画像ファイル', '.bmp': '画像ファイル', '.tif': '画像ファイル', '.tiff': '画像ファイル',\
                  '.mp3': '音声ファイル', '.wma': '音声ファイル', '.wav': '音声ファイル', '.mid': '音声ファイル','.midi': '音声ファイル',\
                  '.avi': '動画ファイル', '.mp4': '動画ファイル', '.wmv': '動画ファイル',\
                  '.exe': '実行ファイル', '.dll': '実行ファイル', \
                  '.pdf': 'PDFファイル', '.doc': 'ワードファイル', '.csv': 'シーエスブイファイル',  '.xls': 'エクセルファイル', '.ppt': 'パワーポイントファイル', '.pps': 'パワーポイントファイル',\
                  '.clip': 'クリスタファイル', '.psd': 'PSDファイル',\
                  '.txt': 'テキストファイル', '.html': 'テキストファイル','.htm': 'テキストファイル',\
                  '.shtml': 'テキストファイル', '.css': 'テキストファイル',\
                  '.zip': '圧縮ファイル', '.lzh': '圧縮ファイル'}

# 時報のセリフリスト{'時刻': 'セリフ'}
time_signal_list = {'00:00': '日付が変わったのだ。まだ寝ないのだ？',\
                    '01:00': 'ずんだもんが午前1時ぐらいをお知らせするのだ',\
                    '02:00': 'ずんだもんが午前2時ぐらいをお知らせするのだ。眠い・・・',\
                    '03:00': 'ずんだもんが午前3時ぐらいをお知らせするのだ',\
                    '04:00': 'ずんだもんが午前4時ぐらいをお知らせするのだ',\
                    '05:00': 'ずんだもんが午前5時ぐらいをお知らせするのだ',\
                    '06:00': 'ずんだもんが午前6時ぐらいをお知らせするのだ',\
                    '07:00': 'ずんだもんが午前7時ぐらいをお知らせするのだ。朝ごはんの時間なのだ',\
                    '08:00': 'ずんだもんが午前8時ぐらいをお知らせするのだ',\
                    '09:00': 'ずんだもんが午前9時ぐらいをお知らせするのだ',\
                    '10:00': 'ずんだもんが午前10時ぐらいをお知らせするのだ',\
                    '11:00': 'ずんだもんが午前11時ぐらいをお知らせするのだ',\
                    '12:00': 'ずんだもんが正午をお知らせするのだ。作業を中断してそろそろお昼にするのだ',\
                    '13:00': 'ずんだもんが午後1時ぐらいをお知らせするのだ',\
                    '14:00': 'ずんだもんが午後2時ぐらいをお知らせするのだ',\
                    '15:00': 'ずんだもんが午後3時ぐらいをお知らせするのだ',\
                    '16:00': 'ずんだもんが午後4時ぐらいをお知らせするのだ',\
                    '17:00': 'ずんだもんが午後5時ぐらいをお知らせするのだ',\
                    '18:00': 'ずんだもんが午後6時ぐらいをお知らせするのだ',\
                    '19:00': 'ずんだもんが午後7時ぐらいをお知らせするのだ',\
                    '20:00': 'ずんだもんが午後8時ぐらいをお知らせするのだ。お腹がすいてきたから晩ごはんを食べてくるのだ',\
                    '21:00': 'ずんだもんが午後9時ぐらいをお知らせするのだ',\
                    '22:00': 'ずんだもんが午後10時ぐらいをお知らせするのだ',\
                    '23:00': 'ずんだもんが午後11時ぐらいをお知らせするのだ'}


# 各種フラグのデフォルト値(Trueで有効、Falseで無効)
inform_someone_come = True    # 入退出の通知
time_signal         = True    # 時報
read_name           = False   # 話者の名前を読み上げる。
number_of_people    = True    # 在室人数チェック
auto_leave          = False   # ボイスチャンネルから人がいなくなった時の自動退出機能
word_count_limit = 50         # 文字数制限(50 -> 50文字でストップ)
elapsed_time_limit = 100      # 再生時間制限(100 -> 10秒でストップ)


# 各種コマンド(変更した場合はcommand_list.txtを書き換えてください。)
command_join                = command_Synthax + 'join'
command_leave               = command_Synthax + 'leave'
command_chg_my_voice        = command_Synthax + 'chg_my_voice'
command_wlist               = command_Synthax + 'wlist'
command_inform_someone_come = command_Synthax + 'inform_someone_come'
command_time_signal         = command_Synthax + 'time_signal'
command_read_name           = command_Synthax + 'read_name'
command_number_of_people    = command_Synthax + 'number_of_people'
command_auto_leave          = command_Synthax + 'auto_leave'
command_word_count_limit    = command_Synthax + 'word_count_limit'
command_elapsed_time_limit  = command_Synthax + 'elapsed_time_limit'
command_show_setting        = command_Synthax + 'show_setting'
command_stop                = command_Synthax + 'stop'
command_help                = command_Synthax + 'help'

command_zunhora             = command_Synthax + 'zunhora'
command_tree                = command_Synthax + 'tree'
command_zunko_HP            = command_Synthax + 'zunko_HP'
command_VOICEVOX_HP         = command_Synthax + 'VOICEVOX_HP'

command_zundamon            = command_Synthax + 'zundamon'


#各種メッセージ
message_err       = comment_Synthax + "コマンドが間違っています[!help参照]"
message_join      = comment_Synthax + "接続したのだ。よろしくなのだ。"
message_leave     = comment_Synthax + "僕はこれで失礼するのだ。ばいばーい"
message_chg_voice = comment_Synthax + "ボイスの変更を行いました"

message_inform_someone_come_off   = comment_Synthax + "入退出通知をオフにしたのだ"
message_inform_someone_come_on    = comment_Synthax + "入退出通知をオンにしたのだ"
message_time_signal_off           = comment_Synthax + "時報をオフにしたのだ"
message_time_signal_on            = comment_Synthax + "時報をオンにしたのだ"
message_read_name_off             = comment_Synthax + "名前読み上げをオフにしたのだ"
message_read_name_on              = comment_Synthax + "名前読み上げをオンにしたのだ"
message_number_of_people_off      = comment_Synthax + "在室人数チェックをオフにしたのだ"
message_number_of_people_on       = comment_Synthax + "在室人数チェックをオンにしたのだ"
message_auto_leave_off            = comment_Synthax + "自動退出をオフにしたのだ"
message_auto_leave_on             = comment_Synthax + "自動退出をオンにしたのだ"