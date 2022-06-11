
# 設定ファイルの読み込み
import discord
import os
import csv
import re
import asyncio
import queue
from for_developer.discordbot_setting import *

flag_name_dict = {command_inform_someone_come: "入退出の通知", command_time_signal: "時報", command_read_name: "名前読み上げ",
                  command_number_of_people: "在室人数チェック", command_auto_leave: "自動退出", 
                  command_chg_speed: "音声のスピード", command_word_count_limit: "文字数制限"}  # フラグの名前
bool_name_dict = {True: "オン", False: "オフ"}  # フラグオンオフ通知用

# 関数の定義
# 以下、引数のmessage_tmpはdiscord.message型を入れる。
# 非同期関数 (async関数) はawaitで呼び出すこと。

# 単語帳 (dict) を単語の長さ順にソートする
def sort_dict(dict):
    keys = sorted(dict.keys(), key=len, reverse=True)
    for k in keys:
        dict[k] = dict.pop(k)


# 単語帳 (dict) を単語の長さ順にソートして書き換える
def revise_dict(dict, file):
    # キーの文字長順でソートする
    sort_dict(dict)
    # word_list.csvを更新する
    with open(file, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        for k, v in dict.items():
            writer.writerow([k, v])


# 他の音源が再生されている間スリープする
async def already_playing_plz_sleep(message_tmp):
    while True:
        if message_tmp.guild.voice_client is None:
            break
        else:
            if message_tmp.guild.voice_client.is_playing():
                await asyncio.sleep(0.05)
            else:
                break

# データ書き込み
def output_data(filename, listname):
    with open(filename, 'w', encoding='utf-8') as f:  
        writer = csv.writer(f)
        for k, v in listname.items():
            writer.writerow([k, v])
    return

# チャンネル情報クラス
class room_information():
    def __init__(self, bot = None, TEXT_ROOM_ID=0, TEXT_ROOM_NAME='', VOICE_ROOM_ID=0, VOICE_ROOM_NAME='', GUILD_ID=0):
        self.bot = None
        self.text_room_id = TEXT_ROOM_ID
        self.text_room_name = TEXT_ROOM_NAME
        self.voice_room_id = VOICE_ROOM_ID
        self.voice_room_name = VOICE_ROOM_NAME
        self.guild_id = GUILD_ID
        # 各種リスト
        self.voice_dict = {}  # 使用ボイスの管理
        self.word_dict = {}  # 単語帳の管理
        self.flag_valid_dict = {command_inform_someone_come: inform_someone_come, command_time_signal: time_signal,
                                command_read_name: read_name, command_number_of_people: number_of_people,
                                command_auto_leave: auto_leave, 
                                command_chg_speed: 1.2, command_word_count_limit: word_count_limit}
        self.image_list = {}  # 画像と呼び出しコマンドの管理
        # キュー処理用
        self.speaking_queue = queue.Queue()
        self.now_loading = False

    def text_room_id_exist(self):
        if self.text_room_id == 0:
            return False
        else:
            return True


    # 人数カウント+自動退出
    async def count_number_of_people(self, text_channel, voice_channel):
        user_count = sum(1 for member in voice_channel.members if not member.bot)
        await text_channel.send('>現在' + str(user_count) + '人接続しているのだ')
        if(user_count == 0 and self.flag_valid_dict[command_auto_leave]):
            await text_channel.send('>誰もいなくなったみたいだから僕もそろそろ抜けるのだ')
            await voice_channel.guild.voice_client.disconnect()
            # 切断に成功したことの報告
            print(self.voice_room_name + "から切断しました")
            # チャンネル情報を初期化
            self.text_room_name = ''
            self.text_room_id = 0
            self.voice_room_name = ''
            self.voice_room_id = 0
            self.guild_id = 0


    # sentenceで得たメッセージをVOICEVOXで音声ファイルに変換しそれを再生する
    def play_voice(self, sentence, message_tmp):
        # チャットの内容をutf-8でエンコードする
        text = sentence.encode('utf-8')

        # HTTP POSTで投げられるように形式を変える
        arg = ''
        for item in text:
            arg += '%'
            arg += hex(item)[2:].upper()

        # batファイルを呼び起こしてwavファイルを作成する
        if message_tmp.author.id in self.voice_dict.keys():
            command1 = bat_json + ' ' + arg + ' ' + self.voice_dict[message_tmp.author.id]
            command2 = bat_voice + ' ' + self.voice_dict[message_tmp.author.id]
        else:
            command1 = bat_json + ' ' + arg + ' ' + '1'
            command2 = bat_voice + ' ' + '1'
        os.system(command1)
        
        # jsonファイルのかきかえ
        with open(json_file, encoding="utf-8") as f:
            data_lines = f.read()
        data_lines = data_lines.replace('"speedScale":1.0', '"speedScale":'+str(self.flag_valid_dict[command_chg_speed]))
        # 同じファイル名で保存
        with open(json_file, mode="w", encoding="utf-8") as f:
            f.write(data_lines)
        os.system(command2)
        
        # wavの再生
        # ffmpegがインストールされていない場合エラーを出す。
        try:
            tmp = discord.FFmpegOpusAudio(voice_file)
        except discord.errors.ClientException:
            print(" ")
            print(" ")
            print("[エラーメッセージ(by かみみや)]")
            print("ffmpegがインストールされていないです（またはPathが通っていないです）")
            print("そのため、音声再生ができません。")
            print("詳しくはreadmeの導入が必要なソフト1.をご覧ください")
            print(" ")
            print(" ")
        
        try:
            tmp = discord.FFmpegOpusAudio(voice_file)
            message_tmp.guild.voice_client.play(tmp)
        except:
            print("再生時エラー")
        return


    # 他の読み込み処理が行われている間スリープする
    async def already_loading_plz_sleep(self):
        while True:
            if self.now_loading:
                await asyncio.sleep(0.05)  
            else:       
                break 


    # 投げられたメッセージの辞書置換から再生までまとめた関数
    async def plz_speak(self, sentence, message_tmp):
        # 読み上げ制限
        if len(sentence) > word_count_limit:
            sentence = sentence[0:word_count_limit - 1] + "以下略"

        # 音声の再生
        for item in re.split('\n|;', sentence):
            # word_dictに含まれる場合は置換する
            for key in self.word_dict.keys():
                item = item.replace(key, self.word_dict[key])
            # 他の音源が再生されている間スリープする
            await already_playing_plz_sleep(message_tmp)
            
            if ('http' in item) or ('https' in item):
                self.play_voice("URLが貼られたのだ", message_tmp)  # 音声の再生
            else:
                self.play_voice(item, message_tmp)  # 音声の再生


    # キューに投げ込まれた文章を逐次再生する
    async def queuing(self, message_tmp):
        while not self.speaking_queue.empty():
            item = self.speaking_queue.get()
            await self.plz_speak(item, message_tmp)
            
    # キューを初期化する
    def queue_clear(self):
        while not self.speaking_queue.empty():
            self.speaking_queue.get()
            self.now_loading = False


    async def reload(self):        
        # voice_dict情報を読み込む
        with open(vlist_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                self.voice_dict[int(row[0])] = row[1]
        # word_dict情報を読み込む
        with open(wlist_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                self.word_dict[row[0]] = row[1]
        # flag_list情報を読み込む
        with open(flist_file,'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row or row[0] not in self.flag_valid_dict.keys():
                    continue
                if row[1] == 'True':
                    self.flag_valid_dict[row[0]] = True
                elif row[1] == 'False':
                    self.flag_valid_dict[row[0]] = False
                else:
                    self.flag_valid_dict[row[0]] = float(row[1])
            f.close()
            
        print('更新完了')
        
    # コマンドを実行する
    async def execute_commands(self, message_tmp):
        # ボイスチャンネルに接続
        if message_tmp.content == command_join:
            # message_tmpの送信者がいるボイスチャンネルに接続
            await message_tmp.author.voice.channel.connect()
            # 接続先のチャンネル情報を記録
            self.text_room_name = str(message_tmp.channel)
            self.text_room_id = int(message_tmp.channel.id)
            self.voice_room_name = str(message_tmp.author.voice.channel)
            self.voice_room_id = int(message_tmp.author.voice.channel.id)
            self.guild_id = message_tmp.guild.id
            # statusの更新
            game = discord.Game(self.voice_room_name)
            await self.bot.change_presence(status=None, activity=game)


            # 接続に成功したことの報告
            print(self.voice_room_name + "に接続しました")
            await message_tmp.channel.send(comment_dict['message_join'])

        # ボイスチャンネルから切断
        elif message_tmp.content == command_leave:
            # statusの初期化
            game = discord.Game("待機中")
            await self.bot.change_presence(status=None, activity=game)
            # ボイスチャンネルから切断
            await message_tmp.guild.voice_client.disconnect()
            # 切断に成功したことの報告
            print(self.voice_room_name + "から切断しました")
            await message_tmp.channel.send(comment_dict['message_leave'])
            # チャンネル情報を初期化
            self.text_room_name = ''
            self.text_room_id = 0
            self.voice_room_name = ''
            self.voice_room_id = 0
            self.guild_id = 0
            
        # helpコマンド
        elif message_tmp.content == command_help:
            await message_tmp.channel.send(help_message)
        elif message_tmp.content == command_hello:
            await message_tmp.channel.send(version_info)
        
        # ボイスの変更
        elif message_tmp.content.startswith(command_chg_my_voice):
            voice_tmp = message_tmp.content.split()
            if len(voice_tmp) == 3:                # エラーチェック
                if (voice_tmp[1], voice_tmp[2]) in speker_id_dict:
                    self.voice_dict[message_tmp.author.id] = speker_id_dict[(voice_tmp[1], voice_tmp[2])]
                    await message_tmp.channel.send(comment_dict['message_chg_voice'])
                    # voice_list.csvを更新する
                    with open(vlist_file, 'w', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        for k, v in self.voice_dict.items():
                            writer.writerow([k, v])
                    return
                else:
                    await message_tmp.channel.send(comment_dict['message_not_actualized'])
                    return
            else:
                await message_tmp.channel.send(comment_dict['message_err'])

        # ワードリストの追加
        elif message_tmp.content.startswith(command_wlist):
            wlist_tmp = message_tmp.content.split()
            if (len(wlist_tmp) == 4) and (wlist_tmp[1] == "add"):                # エラーチェック
                self.word_dict[wlist_tmp[2]] = wlist_tmp[3]
                await message_tmp.channel.send(comment_Synthax + wlist_tmp[2] + "を" + wlist_tmp[3] + "として追加しました")
                revise_dict(self.word_dict, wlist_file)
                return
            elif (len(wlist_tmp) == 3) and (wlist_tmp[1] == "delete"):           # エラーチェック
                self.word_dict.pop(wlist_tmp[2])
                await message_tmp.channel.send(comment_Synthax + wlist_tmp[2] + "を削除しました")
                revise_dict(self.word_dict, wlist_file)
                return
            elif (len(wlist_tmp) == 2) and (wlist_tmp[1] == "show"):             # エラーチェック
                await message_tmp.channel.send(file=discord.File(wlist_file))
                return
            else:  # 例外処理
                await message_tmp.channel.send(comment_dict['message_err'])

        # 読み上げスピードの設定
        elif message_tmp.content.startswith(command_chg_speed):
            command_tmp = message_tmp.content.split()
            # 要素数エラー
            if len(command_tmp) != 2:
                await message_tmp.channel.send(comment_dict['message_err'])
                return            
            # 2つめの要素が数値でなければエラー
            try:
                speed_tmp = '{:3}'.format(command_tmp[1])
                if float(speed_tmp) < 0.5 or 2.0 < float(speed_tmp):
                    await message_tmp.channel.send(comment_Synthax + '0.5から2.0の範囲で指定するのだ')
                else:
                    self.flag_valid_dict[command_chg_speed] = '{:3}'.format(command_tmp[1])
                    await message_tmp.channel.send(comment_Synthax + "読み上げスピードを"+command_tmp[1]+'に設定したのだ')
                    #設定の更新
                    output_data(flist_file, self.flag_valid_dict)
            except ValueError:
                await message_tmp.channel.send(comment_dict['message_err'])
            return
        
        # 文字数制限の設定
        elif message_tmp.content.startswith(command_word_count_limit):
            command_tmp = message_tmp.content.split()
            # 要素数エラー
            if len(command_tmp) != 2:
                await message_tmp.channel.send(comment_dict['message_err'])
                return            
            # 2つめの要素がintでなければエラー
            try:
                self.flag_valid_dict[command_word_count_limit] = int(command_tmp[1])
                await message_tmp.channel.send(comment_Synthax + "文字数制限を"+command_tmp[1]+'に設定したのだ')            #設定の更新
                output_data(flist_file, self.flag_valid_dict)
            except ValueError:
                await message_tmp.channel.send(comment_dict['message_err'])
            return
                
        # 各種設定の変更
        elif message_tmp.content in self.flag_valid_dict.keys():
            self.flag_valid_dict[message_tmp.content] = not self.flag_valid_dict[message_tmp.content]
            await message_tmp.channel.send(comment_Synthax + flag_name_dict[message_tmp.content] + "を" + bool_name_dict[self.flag_valid_dict[message_tmp.content]] + "にしたのだ")
            #設定の更新
            output_data(flist_file, self.flag_valid_dict)
            
        # 現在の設定の確認
        elif message_tmp.content == command_show_setting:
            sentence = '```'
            for flag in self.flag_valid_dict.keys():
                if type(self.flag_valid_dict[flag]) == bool:
                    sentence = sentence + flag_name_dict[flag] + ';' + bool_name_dict[self.flag_valid_dict[flag]] + "\n"
                else:
                    sentence = sentence + flag_name_dict[flag] + ';' + str(self.flag_valid_dict[flag]) + "\n"
            sentence = sentence + '```'
            await message_tmp.channel.send(sentence)

        # 情報の再読み込み
        elif message_tmp.content == command_reload:
            await self.reload()

        # 例外処理
        else:
            await message_tmp.channel.send(comment_dict['message_err'])
