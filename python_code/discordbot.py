# パッケージのインストール
from asyncio.windows_events import NULL
import discord
from discord.ext import tasks, commands
import csv
import sys
import re
from datetime import datetime
from for_developer.discordbot_functions import *

# 接続に必要なオブジェクトを生成
intents = discord.Intents.all()
intents.typing = False  # typingは切る
#client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="$", intents=intents)
tree = bot.tree

# チャンネル情報保存用
room_info_tmp = room_information()


# 起動時の処理
@bot.event
async def on_ready():
    # 起動メッセージを出す
    print('起動しました')
            
    # bot情報の更新
    room_info_tmp.bot = bot
    
    # 各種情報の読み込み
    await room_info_tmp.reload()
    
    # statusの初期化
    game = discord.Game("待機中")
    await bot.change_presence(status=None, activity=game)

# メッセージ受信時に動作する処理
@bot.event
async def on_message(message):
    global room_info_tmp
    text_channel = bot.get_channel(room_info_tmp.text_room_id)
    guild = bot.get_guild(room_info_tmp.guild_id)
    try:
        # メッセージがコメントアウトされている場合は無視する
        if message.content.startswith(comment_Synthax):
            return
        
        # 他のボットのコマンドの場合無視
        for synthax in other_bots_Synthax:
            if message.content.startswith(synthax):
                return

        # 自分以外のボットに対しては無視
        if message.author.bot and (message.author is not message.guild.me):
            return

        # 音声ストップ
        if message.content == command_stop:
            room_info_tmp.queue_clear()
            message.guild.voice_bot.stop()
            return

        # コマンド入力時の処理
        if message.content.startswith(command_Synthax):
            await room_info_tmp.execute_commands(message)
            return
        
        # メッセージが接続先のチャンネル外からのものだった場合
        if int(message.channel.id) != room_info_tmp.text_room_id:
            return
            
    
        # すでにロード中ならスリープ
        await room_info_tmp.already_loading_plz_sleep()
        room_info_tmp.now_loading = True

        # 名前読み上げ
        if room_info_tmp.flag_valid_dict[command_read_name] and not message.author.bot:
            # word_dictに含まれる場合は置換する
            message_tmp = message.author.display_name
            for item in room_info_tmp.word_dict.keys():
                message_tmp = message_tmp.replace(item, room_info_tmp.word_dict[item])
            # キューに名前読み上げセリフを追加する
            room_info_tmp.speaking_queue.put(message_tmp + "さん。")

        # スタンプが貼られた場合
        if(len(message.stickers) != 0):
            tmp_message = str(message.stickers[0].name)
        else:
            tmp_message = message.content
            
        # word_dictに含まれるかつ';'を含む場合は置換する
        for key in room_info_tmp.word_dict.keys():
            if ';' in room_info_tmp.word_dict[key]:
                tmp_message = tmp_message.replace(key, room_info_tmp.word_dict[key])
        
        # メンションを含む場合表示名に変換する
        Members = re.findall(r'<@([0-9]*)>', tmp_message)
        for member in Members:
            tmp_message = re.sub(r'<@'+member+'>', ';'+guild.get_member(int(member)).display_name+';', tmp_message)
            
        # 部屋名に変換する
        Rooms = re.findall(r'<#([0-9]*)>', tmp_message)
        for room in Rooms:
            tmp_message = re.sub(r'<#'+room+'>', ';'+guild.get_channel(int(room)).name+';', tmp_message)
            
        # 絵文字を文字列にかえるetc
        tmp_message = re.sub(r'<:([^:]+):[0-9]*>', r';\1;', tmp_message)
        tmp_message = re.sub(r'<a:([^>]+):[0-9]*>', r';\1;', tmp_message)
        tmp_message = re.sub(r'```\n[^```]*\n```', r";コードブロック;", tmp_message)
        tmp_message = re.sub(r'```[^```]*```', r";コードブロック;", tmp_message)
        tmp_message = re.sub(r'`[^`]*`', r";コードブロック;", tmp_message)
        tmp_message = re.sub(r'\|\|[^||]*\|\|', r";ネタバレ防止;", tmp_message)
        room_info_tmp.speaking_queue.put(tmp_message)
            

        # 添付ファイルがあるとき
        if len(message.attachments) != 0:
            # 拡張子がextension_dict内に含まれている場合は変換する
            extension_tmp = "添付ファイル"
            for extention in extension_dict.keys():
                if extention in str(message.attachments[0]):
                    extension_tmp = extension_dict[extention]

            # メッセージがない (添付ファイルのみ) 場合の処理
            if message.content == '':
                await room_info_tmp.plz_speak(extension_tmp + 'が貼られたのだ', message)
                # キューの初期化
                while not room_info_tmp.speaking_queue.empty():
                    room_info_tmp.speaking_queue.get()
                room_info_tmp.now_loading = False   
                return
            else:
                room_info_tmp.speaking_queue.put("かっこ、" + extension_tmp + "をみながら。")

        await room_info_tmp.queuing(message)
        room_info_tmp.now_loading = False   
    except:
        print(sys.exc_info())

# チャンネル入退室時の処理
@bot.event
async def on_voice_state_update(member, before, after):
    text_channel = bot.get_channel(room_info_tmp.text_room_id)
    voice_channel = bot.get_channel(room_info_tmp.voice_room_id)

    # チャットルームのIDを取得していないときにはスキップ
    if not room_info_tmp.text_room_id_exist:
        return

    # BOTだった場合はスキップ
    if member.bot:
        return

    # お知らせ機能がオフのときはスキップ
    if not room_info_tmp.flag_valid_dict[command_inform_someone_come]:
        return

    # チャンネルへの入退室の確認
    if before.channel != after.channel:
        try:
            if before.channel.id == room_info_tmp.voice_room_id:
                await text_channel.send(member.display_name + 'さんが退出したのだ')
                # 人数カウント、自動退出
                if number_of_people and room_info_tmp.voice_room_id != 0:
                    await room_info_tmp.count_number_of_people(text_channel, voice_channel)
        # before.channelがNoneのときエラーをおこすので除外
        except AttributeError:
            pass
            
        try:
            if after.channel != None and after.channel.id == room_info_tmp.voice_room_id:
                await text_channel.send(member.display_name + 'さんが入室したのだ')
                    
                # 人数カウント、自動退出
                if number_of_people and room_info_tmp.voice_room_id != 0:
                    await room_info_tmp.count_number_of_people(text_channel, voice_channel)
        # after.channelがNoneのときエラーをおこすので除外
        except AttributeError:
            pass
## 時報
@tasks.loop(seconds=60)
async def time_signal_loop():
    # 時報機能がオフのときはスキップ
    if not room_info_tmp.flag_valid_dict[command_time_signal]:
        return
    
    # 現在の時刻を取得し, time_signal_dictに登録されていたら出力
    try:
        now = datetime.now().strftime('%H:%M')
        if now in time_signal_dict.keys():
            channel = bot.get_channel(room_info_tmp.text_room_id)
            await channel.send(time_signal_dict[now])
    except:
        pass

# Botの起動とDiscordサーバーへの接続
async def main():
    async with bot:
        time_signal_loop.start()
        await bot.start(TOKEN)
        
try:
    asyncio.run(main())
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
except discord.errors.LoginFailure:
    print(" ")
    print(" ")
    print("[エラーメッセージ(by かみみや)]")
    print("Discord BotのTOKENが間違っているか入力されていません")
    print("詳しくはreadmeの起動方法4.をご覧ください")
    print(" ")
    print(" ")
