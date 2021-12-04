# パッケージのインストール
import discord
from discord.ext import commands
from discord.ext import tasks
import os
import sys
import csv
import re
from datetime import datetime 
import asyncio
import time

# 設定ファイルの読み込み
from discordbot_setting import *

# VOICEVOX音声再生（.bat）ファイルへのパス
bat_file = 'output_voice_from_VOICEVOX.bat'   

# VOICEVOX音声ファイルへのパス
voice_file = 'tmp/tmp_voice.wav'   

#チャンネル情報保存用
TEXT_ROOM_NAME = ''  #テキストチャンネルの名前
TEXT_ROOM_ID = 0     #テキストチャンネルのID
VOICE_ROOM_NAME = '' #ボイスチャンネルの名前
VOICE_ROOM_ID = 0    #ボイスチャンネルのID

# 各種リスト
voice_list = {} # 使用ボイスの管理
word_list = {}  # 単語リストの管理
flag_list = [[inform_someone_come, '入退出の通知:'], [time_signal, '時報:']] # フラグの管理
bool_list = {True: 'オン', False: 'オフ'} # フラグオンオフ通知用

# 接続に必要なオブジェクトを生成
client = discord.Client()

        
# 起動時に動作する処理
@client.event
async def on_ready():
    print('起動しました')
    # voice_list情報を読み込む
    with open('voice_list.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            voice_list[int(row[0])] = row[1]
    # word_list情報を読み込む
    with open('word_list.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            word_list[row[0]] = row[1]

#メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    
    global TEXT_ROOM_NAME 
    global TEXT_ROOM_ID 
    global VOICE_ROOM_NAME 
    global VOICE_ROOM_ID 
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
        message.guild.voice_client.play(discord.FFmpegPCMAudio(voice_file))
        return
        
    # 音声ストップ
    if message.content == command_stop:
        message.guild.voice_client.stop()
        return

    # 他の音源が再生されている間スリープする
    while True:
        if message.guild.voice_client == None:
            break
        else:
            if message.guild.voice_client.is_playing():
                time.sleep(0.1)
            else:
                break


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
            message_tmp = comment_Synthax + '接続したのだ。よろしくなのだ。'
            await message.channel.send(message_tmp) 
            return           

        # ボイスチャンネルから切断
        elif message.content == command_leave:
            # ボイスチャンネルから切断
            await message.guild.voice_client.disconnect()
            # 切断に成功したことの報告
            print(VOICE_ROOM_NAME + 'から切断しました')
            message_tmp = comment_Synthax + '僕はこれで失礼するのだ。ばいばーい'
            await message.channel.send(message_tmp) 
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
                    await message.channel.send(comment_Synthax + 'ボイスの変更を行いました')
                    #voice_list.csvを更新する
                    with open('voice_list.csv', 'w', encoding='utf-8') as f:  
                        writer = csv.writer(f)
                        for k, v in voice_list.items():
                            writer.writerow([k, v])
                    return
                else:
                    await message.channel.send(comment_Synthax + 'まだ実装されていないです')
                    return
            else:
                await message.channel.send(comment_Synthax + 'コマンドが間違っています[!help参照]')
                return  

        # ワードリストの追加
        elif message.content.startswith(command_wlist):
            wlist_tmp = message.content.split()
            if len(wlist_tmp) > 1:
                if wlist_tmp[1] == 'add':
                    if len(wlist_tmp) == 4:  # エラーチェック
                        word_list[wlist_tmp[2]] = wlist_tmp[3]
                        await message.channel.send(comment_Synthax + wlist_tmp[2] + 'を' + wlist_tmp[3] + 'として追加しました')

                        #word_list.csvを更新する
                        with open('word_list.csv', 'w', encoding='utf-8') as f:  
                            writer = csv.writer(f)
                            for k, v in word_list.items():
                                writer.writerow([k, v])
                        return
                elif wlist_tmp[1] == 'delete':
                    if len(wlist_tmp) == 3:   # エラーチェック
                        word_list.pop(wlist_tmp[2])
                        await message.channel.send(comment_Synthax + wlist_tmp[2] + 'を削除しました')
                        return
                elif wlist_tmp[1] == 'show':
                    if len(wlist_tmp) == 2:   # エラーチェック
                        await message.channel.send(file=discord.File('word_list.csv'))
                        return
                # 例外処理
            await message.channel.send(comment_Synthax + 'コマンドが間違っています[!help参照]')            

        # 入退出通知の設定
        elif message.content == command_inform_someone_come:
            if flag_list[0][0]:
                flag_list[0][0] = False
                await message.channel.send(comment_Synthax + '入退出通知をオフにしたのだ')
            else:
                flag_list[0][0] = True
                await message.channel.send(comment_Synthax + '入退出通知をオンにしたのだ')

        # 時報の設定
        elif message.content == command_time_signal:
            if flag_list[1][0]:
                flag_list[1][0] = False
                await message.channel.send(comment_Synthax + '時報をオフにしたのだ')
            else:
                flag_list[1][0] = True
                await message.channel.send(comment_Synthax + '時報をオンにしたのだ')

        # 現在の設定の確認
        elif message.content == command_show_setting:
            for flag in flag_list:
                await message.channel.send(comment_Synthax + flag[1] + bool_list[flag[0]])
            return

        # helpコマンド
        elif message.content == command_help:
            await message.channel.send(file=discord.File('command_list.txt'))
            return
####追加コマンド################################################################################################    
        # ずんだもんコマンド(画像貼り付けサンプル)
        elif message.content == command_zundamon:
            await message.channel.send(file=discord.File('image/zundamon_pot.png'))
            return

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
            await message.channel.send(comment_Synthax + 'コマンドが間違っています[!help参照]')
            return

    else:
        
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
                message_tmp += item

            # word_listに含まれる場合は置換する
            for item in word_list.keys():
                message_tmp = message_tmp.replace(item, word_list[item])

            # 音声の再生
            if len(message_tmp) > word_count_limit:
                message_tmp = "文字数制限を超えました"
            play_voice(message_tmp)  # 音声の再生

# チャンネル入退室時の処理
@client.event
async def on_voice_state_update(member, before, after):    
    text_channel = client.get_channel(TEXT_ROOM_ID)
    voice_guild = client.get_guild(VOICE_ROOM_ID)
    # BOTだった場合はスキップ
    if member.bot:
        return

    # お知らせ機能がオフのときはスキップ
    if not flag_list[0][0] :
        return

    # チャンネルへの入退室の確認
    if before.channel != after.channel:
        if (before.channel is not None) and (str(before.channel) == VOICE_ROOM_NAME):
            message_tmp = member.display_name + 'さんが退出したのだ'
            await text_channel.send(message_tmp)
        if (after.channel is not None) and (str(after.channel) == VOICE_ROOM_NAME):
            message_tmp = member.display_name + 'さんが入室したのだ'
            await text_channel.send(message_tmp)

# 時報
@tasks.loop(seconds=60)
async def loop():
    # 時報機能がオフのときはスキップ
    if not time_signal:
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
client.run(TOKEN)
