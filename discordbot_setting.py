# 自分のBotのアクセストークン
TOKEN = 'aaa'

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
inform_someone_come = True     # 入退出の通知
time_signal         = True     # 時報

# シンタックス(変更した場合はcommand_list.txtを書き換えてください。)
command_Synthax = '!' #コマンドの先頭に付ける記号
comment_Synthax = '>' #読み上げられたくない文の先頭に付ける記号

# 各種コマンド(変更した場合はcommand_list.txtを書き換えてください。)
command_join                = command_Synthax + 'join'
command_leave               = command_Synthax + 'leave'
command_chg_my_voice        = command_Synthax + 'chg_my_voice'
command_wlist               = command_Synthax + 'wlist'
command_inform_someone_come = command_Synthax + 'inform_someone_come'
command_time_signal         = command_Synthax + 'time_signal'
command_show_setting        = command_Synthax + 'show_setting'
command_stop                = command_Synthax + 'stop'
command_help                = command_Synthax + 'help'

command_zunhora             = command_Synthax + 'zunhora'
command_tree                = command_Synthax + 'tree'
command_zunko_HP            = command_Synthax + 'zunko_HP'
command_VOICEVOX_HP         = command_Synthax + 'VOICEVOX_HP'

command_zundamon            = command_Synthax + 'zundamon'