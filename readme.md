# yomiage_VOICEVOX_for_this_server__source(v20220204)

by かみみや

## 概要

DiscordのチャットをVOICEVOXで読み上げるソフトです。

python読める＆python実行できる人向けです。

コマンド一覧は[command_list.html](command_list.html)を参照してください。

## 機能紹介

1. チャットの読み上げ
2. 単語の読み仮名登録
3. ユーザー毎に使用ボイスを変える
4. ボイスチャット入室時の通知（オンオフ切り替え可能）
5. 時報機能（オンオフ切り替え可能）


## ファイル構造(重要度順)

1. **readme.md**
   - これです。使い方などかいているのでお読みください。
   - (html版も用意しています)
2. **前バージョンからの移行方法.txt**
   - 以前のバージョンを使っていた場合はこれを参考にしてデータ（単語帳など）を引き継いでください
2. **discordbot.exe**
   - 実行ファイル
3. **TOKEN.txt**
   - BOTのアクセストークンを保存するファイル
4. **command_list.html**
   - 実装されているコマンドの確認
5. **Synthax_setting.csv**
   - コマンドおよびコメントの先頭の文字を設定するファイル
7. **discordbot.py**
   - ソースファイル①
8. **for_developer.py**
   - ソースファイル②
6. **data**
   - 単語帳などが保存されるファイル。開く必要はあまりないです。
7. **output_json_from_VOICEVOX.bat**
   - VOICEVOXでjsonファイルを作成するbatファイル。
8. **output_voice_from_VOICEVOX.bat**
   - VOICEVOXで音声を作成するbatファイル。
11. **tmp**
    - 一時的に出力されるファイル（VOICEVOXで出力した音声ファイル等）が保存されます。開く必要は全くないです。

## 注意

1. このソフトはWindows10上で使われることを想定しています。LinuxやMacで使う場合はbatファイルまわりと音声のopus変換まわりをいじれば多分なんとかなります。
2. Pythonほぼ触ったことない + Discord bot作るの初めてで不慣れなところがあり一部コードが汚いかもしれないです。ごめんなさい。
2. 以前のバージョンのデータを引き継ぎたい場合は**データの引き継ぎ方.txt**をご覧ください
2. v20211208より前のバージョンを使っていた場合、discord botの設定を少し変える必要があります

## 導入が必要なソフト

このソフトを利用するために以下のソフト類のインストールが必要です。

1. python3のインストール
   [このサイト](https://www.python.jp/install/windows/install.html)を参考にしてください。
   
   **python3.8以上をおすすめします。**（3.7より古いものはライブラリがサポートしていない）
   
2. ffmpegのインストール
   [このサイト](https://jp.videoproc.com/edit-convert/how-to-download-and-install-ffmpeg.htm)の"**1. WindowsでFFmpegをダウンロード＆インストールする方法（Windows10対応）**"を参考にしてください。

3. pycord.py, PyNaClのインストール
   コマンドプロンプト(Win+Rで"ファイル名を指定して実行"をひらいて"cmd"を打ち込んだら出てくると思います）上で以下のコマンドを打ち込んで実行してください。

   ```bash
   $ pip install git+https://github.com/Pycord-Development/pycord
   $ pip install PyNaCl
   ```
   
4. googleAPI用ライブラリのインストール
   
   ``` bash
   $ pip install gspread
   $ pip install oauth2client
   ```
   
   
   
4. VOICEVOXのインストール
   [このサイト](https://voicevox.hiroshiba.jp/)から最新版をダウンロードしてください。


## 起動方法


1. 上の導入が必要なソフトをすべてインストールします。

2. このフォルダ(yomiage_VOICEVOX)をわかりやすい場所に置きます。

3. DiscordのBotを作成し、招待します。（すでにチャットルームにBotを招待している場合は省略）[このサイト](https://note.com/exteoi/n/nf1c37cb26c41)の**1. Discord上のBotの作成**にある記述を参考にしてください。

   1. https://discord.com/developers/applications を開きます。
   2. 右上にあるNew Applicationを押す。適当な名前を入れてCreateを押します。
   3. 管理画面が開かれる。左のメニューのBotを押し、Add Botを押す。→Yes, do it!を選択（開かれない場合はDeveloper Portalから作成したアプリケーションを選択する）
   4. するとBuild-A-Botのところになんか出てくる。そのTOKENのところにあるCopyを押すとBotのTOKENがコピーできる。**のちに必要となるので保存しておく。**
   5. **そのしたのPUBLIC BOT, REQUIRES OAUTH2 CODE GRANTをオフ、Presence Intent, Server Members Intentという項目をオンにする。(灰色がオフ、青色がオン）**
   6. 左のメニューのOAuth2→URL Generatorを開きます。 SCOPESでbotにチェックを入れます。
   7. BOT PERMISSIONSという項目が出てくると思うのでRead Messages/ViewChannels, Send Messages, Connect, Speakにチェックを入れてください。
   8. 一番下にあるGENERATED URLにあるリンクを開くとサーバー招待画面が出てくるので、追加したいサーバーを選択して認証します 。

3. アクセストークンを設定する（すでに設定していたら省略）

   TOKEN.txtをテキストエディタで開いて、2-4)でコピーしていたTOKENを保存してください。

4. VOICEVOXを起動します。

4. コマンドプロンプトを起動します。 (Win+Rで"ファイル名を指定して実行"をひらいて"cmd"を打ち込んだら出てくると思います）

7. チェンジディレクトリでこのフォルダの中身まで移動します。
   cd ディレクトリ名で移動できます。（https://eng-entrance.com/windows-command-cd を参照）例えば以下のようにする。

   ```bash
   $ cd C:\discord_bot\yomiage_VOICEVOX
   ```

8. コマンドプロンプトに以下を打ち込み、実行します。

   ```bash
   $ py discordbot.py
   ```

9. おつかれさまでした。

## 使用方法

1. Botを参加させたいボイスチャンネルに入室しておきます。
2. 読み上げ対象にしたいテキストチャンネル上で"!join"と打ち込みます。

## 終了方法

1. "!leave"でボイスチャンネルからBOTを退場させておきます
2. コマンドプロンプト上で"ctrl + C"をおこなって終了させます

## exeファイル化の方法

pyinstallerを使うので入ってない場合はインストールする。

```bash
$ pip install pyinstaller
```

以下のコマンドを打ち込んでexe化する(pyinstallerが使えない場合は環境変数の編集からPath[例）C:\Users\xxx\AppData\Roaming\Python\Python38\Scripts]を追加する）

```bash
$ pyinstaller for_developer/discordbot.spec --onefile
```

成功したら**dist**というファイルが生成され、そのなかにdiscordbot.exeがある。

### **注意**

追加機能を付けるなどで外部ライブラリを使うorPython以外でコーディングしたプログラムを用いる必要がある場合はspecファイルの書き換えを行う必要がでてくる可能性がある

[参考資料](https://qiita.com/takanorimutoh/items/53bf44d6d5b37190e7d1) 

## エラーが出た時

- アクセスが拒否されました

  ウイルスセキュリティソフトに引っかかっている可能性がある。許可する。

- Bot TOKENが設定されていません

  設定して下さい。[**起動方法4)**を参照]

- Discord BotのPrivileged Intents が有効になっていません云々のメッセージ

  BOTの設定に問題があるので確認する [**起動方法2-5)**を参照]

- ffmpegがインストールされていない云々のメッセージ

  ffmpegをインストールする [**導入が必要なソフト1)**を参照]

## 前バージョンからの引き継ぎ方法

前バージョンのyomiage_VOICEVOXのうち

1. data
2. SE
3. SE_list.csv

の3つをこのファイルに上書き保存する。

## SEの追加方法

例)dededeに音声を追加したい場合

1. wavファイルを用意する
2. dedede.wavという名前にして,SEフォルダの中に入れる
3. SE_list.csvをひらき（メモ帳で開ける）, 一番下にdededeを追加する。

## その他

1. ほかのBOTとコマンドが被ってしまっている場合はSynthax_setting.csvの"!", ">"を適当に変更してください。
5. 機能の追加、バグの修正などしていくつもりなのでよろしくお願いします。更新したらdiscordで報告します。


## 利用規約的なやつ

1. 本ソフトはオープンソースです。お金を払いたい場合はVOICEVOX様にどうぞ

   [VOICEVOX支援先](https://hiho.fanbox.cc/)

2. ソースコードの改変はご自由にどうぞ。
   ただし、改変したものを配布する場合は改変したことが分かるようにファイル名を変更して、更新履歴に変更点を追記してください。

3. VOICEVOX及び各キャラの利用規約をよく読んでから使用してください。<br>
   [VOICEVOX本体利用規約(非公式Wiki)](https://wikiwiki.jp/voicevox/%E6%9C%AC%E4%BD%93%E5%88%A9%E7%94%A8%E8%A6%8F%E7%B4%84) <br>
   [東北ずん子利用の手引き](https://zunko.jp/guideline.html)<br>
   [春日部つむぎHP](https://tsukushinyoki10.wixsite.com/ktsumugiofficial)<br>
   [波音リツHP](http://ritsu73.is-mine.net/aboutritsu.html)

4. 本ソフトウェアにより生じた損害・不利益について、製作者は一切の責任を負いません。

5. 改善して欲しい点などあれば言ってください。
   ある程度リクエストは受け付けたいと思っていますが、製作者に技術がないのであまり期待しないでください。

6. 何かあればTwitterかDiscordまで<br>
   Twitter: @Kamimiya_yade<br>Discord: https://discord.gg/CMrDukD8DZ

## 更新履歴

- 20211202(かみみや)

  とりあえず動くようになった

- 20211203(かみみや) 

  時報・入退室管理機能の追加

  チャットが混雑した時に読み上げがスタックする問題の解決

  イラスト動画投稿を知らせる機能の追加

  URLが貼られたときの処理を追加した

  添付ファイルがあるときの処理を追加した

  BOTが参加したチャンネル名を取得できるようにした

- 20211204(かみみや)    

  ソースコードを整理した

  設定ファイル（discordbot_setting.py）を作成した

  一時的に出力されるファイルをtmpフォルダに保存するようにした

  単語リストまわりの改善をおこなった

- 20211205(かみみや)

  !wlist_showでword_list.csvをdiscord上で表示すると文字化けしていたのでencoding=utf-8に変更した。

  voice_list.csvの更新がうまくできていなかったので修正した

  読み上げ文字数制限を加えた

  command_list.txtの内容を修正した

- 20211206(かみみや)

  readme.mdの更新。(機能紹介とかなしみ欄を追加した）

  ボイスチャンネルの接続人数の確認

  ボイスチャンネルから人がいなくなったら自動!leaveするようにした

  名前読み上げモードを実装した

  word_listについて, キーの文字列長さ順にソートするようにした。

- 20211207(かみみや)

  文字数制限を超えた時、（文字数制限までのセリフ）＋（超えました）で返すようにする

  再生時間に対する制限も加えた。

  音声再生中もコマンドに反応できるようにした

- 20211208(かみみや)

  exeファイル化に成功した。

  TOKENの指定方法を変えた。

  各種設定について、変更が保存されるようにした。

  SEが再生できるようになった。

- 20211211(かみみや)

  すこしコードの整理をした。

  メッセージ付きで添付ファイルを送った際にメッセージが読み上げられるようにした。

  改行が入ったメッセージをちゃんと読み上げられるようにした。

- 20211214(かみみや)

  自分以外のbotのメッセージを読み上げないようにした。

  SE付きのメッセージについて、読みを改善した

  素材置き場に素材が置かれた時にメッセージを出すようにした。

  ソースコードの整理を行った。

  TOKENの設定をTOKEN.txtから行うようにした。

- 20211231(かみみや)

  readmeをhtml化した。
  雨晴はうのボイスを使えるようにした
  現在入室しているチャンネルの名前をステータス上に表示するようにした
  コードブロック、スポイラーを読み飛ばすようにした
  メンション付きメッセージも読むようにした

- 20220130

  コード内容の刷新
  使用ライブラリをpycordに変えた。
  !helpコマンドの挙動を変えた。
  ミュート機能を削除した。
  
- 20220313

  read_nameが機能しない問題を解決
  
  0.11.1で追加されたボイスを使えるようにした
  
  
