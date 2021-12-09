# パッケージのインストール
from enum import auto
import discord
from discord.ext import commands
from discord.ext import tasks

import os
import sys
import csv
import re
from datetime import datetime 
import asyncio

# 設定ファイルの読み込み
from discordbot_setting import *

# 各種ファイルへのパス
bat_file = 'output_voice_from_VOICEVOX.bat'  # VOICEVOX音声再生（.bat）ファイルへのパス 
vlist_fname = 'data/voice_list.csv'  # ボイス情報へのパス 
wlist_fname = 'data/word_list.csv'  # 単語リストへのパス 
flist_file = 'data/flag_list.csv' # 各種設定リストへのパス
command_list_fname = 'command_list.txt' # コマンドリストへのパス
voice_file = 'tmp/tmp_voice.wav'  # VOICEVOX音声ファイルへのパス


#チャンネル情報保存用
TEXT_ROOM_NAME = ''  #テキストチャンネルの名前
TEXT_ROOM_ID = 0     #テキストチャンネルのID
VOICE_ROOM_NAME = '' #ボイスチャンネルの名前
VOICE_ROOM_ID = 0    #ボイスチャンネルのID

# 各種リスト
voice_list = {} # 使用ボイスの管理
word_list = {} # 単語リストの管理
flag_list = {'inform_someone_come': inform_someone_come, 'time_signal': time_signal,\
             'read_name': read_name, 'number_of_people': number_of_people, 'auto_leave': auto_leave,\
             'word_count_limit': word_count_limit, 'elapsed_time_limit': elapsed_time_limit} # フラグの管理
flag_name = {'inform_someone_come': '入退出通知', 'time_signal': '時報',\
             'read_name': '名前読み上げ', 'number_of_people': '在室人数チェック', 'auto_leave': '自動退出',\
             'word_count_limit': '文字数制限(50 -> 50文字でストップ)', 'elapsed_time_limit': '再生時間制限(100 -> 10秒でストップ)'} # フラグの管理
bool_list = {True: "オン", False: "オフ"} # フラグオンオフ通知用

# 各種変数
elapsed_time = 0

intents=discord.Intents.all()    
client = discord.Client(intents=intents)


# 起動時に動作する処理
@client.event
async def on_ready():
    print('起動しました')
    # voice_list情報を読み込む
    with open(vlist_fname, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            voice_list[int(row[0])] = row[1]
        f.close()
    # word_list情報を読み込む
    with open(wlist_fname, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            word_list[row[0]] = row[1]
        f.close()
    # flag_list情報を読み込む
    with open(flist_file,'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            if row[1] == 'True':
                flag_list[row[0]] = True
            elif row[1] == 'False':
                flag_list[row[0]] = False
            else:
                flag_list[row[0]] = int(row[1])
        f.close()


                

#メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    
    global TEXT_ROOM_NAME 
    global TEXT_ROOM_ID 
    global VOICE_ROOM_NAME 
    global VOICE_ROOM_ID 
    global flag_list
    global elapsed_time
    text_channel = client.get_channel(TEXT_ROOM_ID)

    # sentenceで得たメッセージをVOICEVOXで音声ファイルに変換しそれを再生する
    def play_voice(sentence):
        # チャットの内容をutf-8でエンコードする
        text = sentence.encode('utf-8')

        # HTTP POSTで投げられるように形式を変える
        arg = ''
        for item in text:
            arg += '%'
            arg += hex(item)[2:].upper()

        # batファイルを呼び起こしてwavファイルを作成する
        if message.author.id in voice_list.keys():
            command = bat_file + ' ' + arg + ' ' + voice_list[message.author.id]
        else:
            command = bat_file + ' ' + arg + ' ' + '1'
        os.system(command)

        #wavの再生    
        #ffmpegがインストールされていない場合エラーを出す。
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
            
        message.guild.voice_client.play(tmp)
        return
    
    # データ書き込み
    def output_data(filename, listname):
        with open(filename, 'w', encoding='utf-8') as f:  
            writer = csv.writer(f)
            for k, v in listname.items():
                writer.writerow([k, v])
        return
    
    # flag_listデータ書き込み
    def output_flist_data(filename, listname):
        with open(filename, 'w', encoding='utf-8') as f:  
            for key in flag_list:
                value = flag_list[key]
                print(type(value))
                print(value)
                if value[0]:
                    f.write(key + 'True' + value[1])
                elif not value[0]:
                    f.write(key + 'False' + value[1])
                else:
                    f.write(key + value[0] + value[1])
        return
        
    # 辞書のキーの長さ順でソートする
    def sort_dict(dict):
        keys = sorted(dict.keys(), key=len, reverse=True)
        for k in keys:
            dict[k] = dict.pop(k)

    
    # 音声ストップ
    if message.content == command_stop:
        message.guild.voice_client.stop()
        return


    # コマンド入力時の処理
    if message.content.startswith(command_Synthax):
        # ボイスチャンネルに接続
        if message.content == command_join:
            # messageの送信者がいるボイスチャンネルに接続
            await message.author.voice.channel.connect()
            # 接続先のチャンネル情報を記録
            TEXT_ROOM_NAME = str(message.channel)
            TEXT_ROOM_ID = message.channel.id
            VOICE_ROOM_NAME = str(message.author.voice.channel)
            VOICE_ROOM_ID = message.author.voice.channel.id
            # 接続に成功したことの報告
            print(VOICE_ROOM_NAME + 'に接続しました')
            await message.channel.send(message_join) 
            return           

        # ボイスチャンネルから切断
        elif message.content == command_leave:
            # ボイスチャンネルから切断
            await message.guild.voice_client.disconnect()
            # 切断に成功したことの報告
            print(VOICE_ROOM_NAME + 'から切断しました')
            await message.channel.send(message_leave) 
            # チャンネル情報を初期化
            TEXT_ROOM_NAME = ''
            TEXT_ROOM_ID = 0
            VOICE_ROOM_NAME = ''
            VOICE_ROOM_ID = 0
            return

        # ボイスの変更
        elif message.content.startswith(command_chg_my_voice):
            voice_tmp = message.content.split()
            if len(voice_tmp) == 3:   # エラーチェック
                if (voice_tmp[1], voice_tmp[2]) in speker_id_list:
                    voice_list[message.author.id] = speker_id_list[(voice_tmp[1], voice_tmp[2])]
                    await message.channel.send(message_chg_voice)
                    #voice_list.csvを更新する
                    output_data(vlist_fname, voice_list)
                    return
            await message.channel.send(message_err)
            return  

        # ワードリストの追加
        elif message.content.startswith(command_wlist):
            wlist_tmp = message.content.split()
            if len(wlist_tmp) > 1:
                if wlist_tmp[1] == 'add':
                    if len(wlist_tmp) == 4:  # エラーチェック
                        word_list[wlist_tmp[2]] = wlist_tmp[3]
                        await message.channel.send(comment_Synthax + wlist_tmp[2] + 'を' + wlist_tmp[3] + 'として追加しました')
                        
                        #キーの文字長順でソートする
                        sort_dict(word_list)
                        
                        #ワードリストを更新する
                        output_data(wlist_fname, word_list)
                        return
                elif wlist_tmp[1] == 'delete':
                    if len(wlist_tmp) == 3:   # エラーチェック
                        word_list.pop(wlist_tmp[2])
                        await message.channel.send(comment_Synthax + wlist_tmp[2] + 'を削除しました')
                        return
                elif wlist_tmp[1] == 'show':
                    if len(wlist_tmp) == 2:   # エラーチェック
                        await message.channel.send(file=discord.File(wlist_fname))
                        return
                # 例外処理
            await message.channel.send(message_err)     
            return       

        # 入退出通知の設定
        elif message.content == command_inform_someone_come:
            if flag_list['inform_someone_come']:
                flag_list['inform_someone_come'] = False
                await message.channel.send(message_inform_someone_come_off)
            else:
                flag_list['inform_someone_come'] = True
                await message.channel.send(message_inform_someone_come_on)
            #設定の更新
            output_data(flist_file, flag_list)

        # 時報の設定
        elif message.content == command_time_signal:
            if flag_list['time_signal']:
                flag_list['time_signal'] = False
                await message.channel.send(message_time_signal_off)
            else:
                flag_list['time_signal'] = True
                await message.channel.send(message_time_signal_on)
            #設定の更新
            output_data(flist_file, flag_list)

        # 名前読み上げの設定
        elif message.content == command_read_name:
            if flag_list['read_name']:
                flag_list['read_name'] = False
                await message.channel.send(message_read_name_off)
            else:
                flag_list['read_name'] = True
                await message.channel.send(message_read_name_on)
            #設定の更新
            output_data(flist_file, flag_list)

        # 在室人数チェックの設定
        elif message.content == command_number_of_people:
            if flag_list['number_of_people']:
                flag_list['number_of_people'] = False
                await message.channel.send(message_number_of_people_off)
            else:
                flag_list['number_of_people'] = True
                await message.channel.send(message_number_of_people_on)
            #設定の更新
            output_data(flist_file, flag_list)
                
        # 自動退出の設定
        elif message.content == command_auto_leave:
            if flag_list['auto_leave']:
                flag_list['auto_leave'] = False
                await message.channel.send(message_auto_leave_off)
            else:
                flag_list['auto_leave'] = True
                await message.channel.send(message_auto_leave_on)
            #設定の更新
            output_data(flist_file, flag_list)
            
        # 文字数制限の設定
        elif message.content.startswith(command_word_count_limit):
            command_tmp = message.content.split()
            # 要素数エラー
            if len(command_tmp) != 2:
                await message.channel.sent(message_err)
                return            
            # 2つめの要素がintでなければエラー
            try:
                flag_list['word_count_limit'] = int(command_tmp[1])
                await message.channel.send(comment_Synthax + "文字数制限を"+command_tmp[1]+'に設定したのだ')
            except ValueError:
                await message.channel.send(message_err)
                
            #設定の更新
            output_data(flist_file, flag_list)
            
        # 読み上げ時間制限の設定
        elif message.content.startswith(command_elapsed_time_limit):
            command_tmp = message.content.split()
            # 要素数エラー
            if len(command_tmp) != 2:
                await message.channel.sent(message_err)
                return
            # 2つめの要素がintでなければエラー
            try:
                flag_list['elapsed_time_limit'] = int(command_tmp[1])
                await message.channel.send(comment_Synthax + "読み上げ時間制限を"+command_tmp[1]+'に設定したのだ')
            except ValueError:
                await message.channel.send(message_err)
                
            #設定の更新
            output_data(flist_file, flag_list)

        # 現在の設定の確認
        elif message.content == command_show_setting:
            for flag in flag_name:
                await message.channel.send(comment_Synthax + flag_name[flag] +' : '+ str(flag_list[flag]))
            return

        # helpコマンド
        elif message.content == command_help:
            await message.channel.send(file=discord.File(command_list_fname))
            return
####追加コマンド################################################################################################    

        # ずん子公式サイトコマンド(テキスト貼り付けサンプル)
        elif message.content == command_zunko_HP:
            await message.channel.send('https://zunko.jp/')
            return

        # VOICEVOX公式サイト
        elif message.content == command_VOICEVOX_HP:
            await message.channel.send('https://voicevox.hiroshiba.jp/')
            return
            
        # ずんホラコマンド
        elif message.content == command_zunhora:
            await message.channel.send('https://anime.dmkt-sp.jp/animestore/ci_pc?workId=21710')
            return

        # 木シミュコマンド
        elif message.content == command_tree:
            await message.channel.send('https://store.steampowered.com/app/1591290/Tree_Simulator_2022/')
            return

###############################################################################################################      
        # 例外処理
        else:
            await message.channel.send(message_err)
            return

    else:
        # 他の音源が再生されている間スリープする
        while True:
            if message.guild.voice_client == None:
                break
            else:
                if message.guild.voice_client.is_playing():
                    await asyncio.sleep(0.1)
                else:
                    break
                
        # メッセージがコメントアウトされている場合は無視する
        if message.content.startswith(comment_Synthax):
            return

        # メッセージが接続先のチャンネル外からのものだった場合無視する
        elif str(message.channel) != TEXT_ROOM_NAME:
            return

        # URLがはられた場合
        elif ('http' in message.content) or ('https' in message.content):
            play_voice('URLが貼られたのだ')
            return
        
        # 添付ファイルがあるとき
        elif len(message.attachments) != 0:
            # extension_list.keysにある拡張子が含まれているか検索
            for extention in extension_list.keys():
                # 含まれている場合の処理
                if extention in str(message.attachments[0]):
                    play_voice(extension_list[extention] + 'が貼られたのだ')    # 音声の再生
                    return

            # 含まれていない場合の処理
            play_voice('添付ファイル')  # 音声の再生
            return

        else:
            # スタンプが含まれる可能性があるのでその処理を行う
            message_split = re.split(':', message.content)
            message_tmp = ''
            for item in message_split:
                if '> <' in item:
                    item_split = re.split('> <',item)
                    item = item_split[1]
                if '<' in item:
                    item_split = re.split('<',item)
                    item = item_split[0]
                if '>' in item:
                    item_split = re.split('>',item)
                    item = item_split[1]
                    
                # word_listに含まれる場合は置換する
                message_tmp += item

            # word_listに含まれる場合は置換する
            for item in word_list.keys():
                message_tmp = message_tmp.replace(item, word_list[item])

            # 音声の再生
            if len(message_tmp) > word_count_limit:
                message_tmp = message_tmp[0:word_count_limit-1] + "以下略"
                
            if flag_list['read_name'] and not message.author.bot:
                message_tmp = message.author.display_name + "さん。" + message_tmp
            
             # 音声の再生
            message_tmp_split = re.split('\n',message_tmp)
            for item in message_tmp_split:
                # 他の音源が再生されている間スリープする
                while True:
                    if message.guild.voice_client == None:
                        break
                    else:
                        if message.guild.voice_client.is_playing():
                            await asyncio.sleep(0.1)
                        else:
                            break
                play_voice(item)  # 音声の再生           
                ## 再生時間をはかり、上限をこえたら省略する
                while True:
                    if message.guild.voice_client.is_playing():
                        
                        elapsed_time = elapsed_time + 1
                        await asyncio.sleep(0.1)
                        if elapsed_time > elapsed_time_limit:
                            elapsed_time = 0
                            message.guild.voice_client.stop()
                            play_voice("以下略。")  # 音声の再生
                            break
                    else:
                        elapsed_time = 0
                        break
            #play_voice(message_tmp) 
            ### 再生時間をはかり、上限をこえたら省略する
            #while True:
            #    if message.guild.voice_client.is_playing():
            #        
            #        elapsed_time = elapsed_time + 1
            #        await asyncio.sleep(0.1)
            #        if elapsed_time > elapsed_time_limit:
            #            elapsed_time = 0
            #            message.guild.voice_client.stop()
            #            play_voice("以下略。")  # 音声の再生
            #            break
            #    else:
            #        elapsed_time = 0
            #        break

# チャンネル入退室時の処理
@client.event
async def on_voice_state_update(member, before, after):    
    global TEXT_ROOM_NAME 
    global TEXT_ROOM_ID 
    global VOICE_ROOM_NAME 
    global VOICE_ROOM_ID 
    text_channel = client.get_channel(TEXT_ROOM_ID)
    voice_channel = client.get_channel(VOICE_ROOM_ID)
    
    # チャットルームのIDを取得していないときにはスキップ
    if TEXT_ROOM_ID == 0:
        return
    
    # BOTだった場合はスキップ
    if member.bot:
        return

    # お知らせ機能がオフのときはスキップ
    if not flag_list['inform_someone_come'] :
        return

    # チャンネルへの入退室の確認
    if before.channel != after.channel:
        if str(before.channel) == VOICE_ROOM_NAME:
            await text_channel.send(member.display_name + 'さんが退出したのだ')
            if flag_list['number_of_people']:
                user_count = sum(1 for member in voice_channel.members if not member.bot)
                await text_channel.send('>現在'+str(user_count)+'人接続しているのだ')
                if(user_count==0 and flag_list['auto_leave']):
                    await text_channel.send('>誰もいなくなったみたいだから僕もそろそろ抜けるのだ')
                    await before.channel.guild.voice_client.disconnect()
                    # 切断に成功したことの報告
                    print(VOICE_ROOM_NAME + "から切断しました")
                    # チャンネル情報を初期化
                    TEXT_ROOM_NAME = ''
                    TEXT_ROOM_ID = 0
                    VOICE_ROOM_NAME = ''
                    VOICE_ROOM_ID = 0         
        if (after.channel is not None) and (str(after.channel) == VOICE_ROOM_NAME):
            await text_channel.send(member.display_name + 'さんが入室したのだ')
            if flag_list['number_of_people']:
                user_count = sum(1 for member in voice_channel.members if not member.bot)
                await text_channel.send('>現在'+str(user_count)+'人接続しているのだ')    

# 時報
@tasks.loop(seconds=60)
async def loop():
    # 時報機能がオフのときはスキップ
    if not time_signal:
        return

    # チャットルームのIDを取得していないときにはスキップ
    if TEXT_ROOM_ID == 0:
        return

    # 現在の時刻の取得
    now = datetime.now().strftime('%H:%M')
    # 設定されている時刻になったらテキストを送る
    if now in time_signal_list.keys():
        channel = client.get_channel(TEXT_ROOM_ID)
        await channel.send(time_signal_list[now])  


#ループ処理実行
loop.start()

# Botの起動とDiscordサーバーへの接続
    
try:
    client.run(TOKEN)
except discord.errors.PrivilegedIntentsRequired:    
    
    print(" ")
    print(" ")
    print("[エラーメッセージ(by かみみや)]")
    print("Discord BotのPrivileged Intents が有効になっていません")
    print("Discord Botの設定(https://discord.com/developers/applications)の下段にあるPrivileged Gateway Intentsの項目の")
    print("PRESENCE INTENTとSERVER MEMBERS INTENTの項目にチェックを入れて下さい。")
    print("詳しくはreadmeの起動方法3.をご覧ください")
    print(" ")
    print(" ")

    