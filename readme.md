# yomiage_VOICEVOX(20211205_1)

by かみみや

## 概要

DiscordのチャットをVOICEVOXで読み上げるソフトです。

## ファイル構造(重要度順)

1. readme.md
   - これです。使い方などかいているのでお読みください。
2. command_list.txt
   - コマンドリスト。現在実装されているコマンドが記載されています。
3. discordbot_setting.py
   - 設定ファイル。各種設定はここから変更してください。
4. discordbot.py
   - メインプログラム。コマンドの追加などを行いたい場合は適宜追記してください。
5. word_list.csv
   - 単語帳。wlistで追加した単語はここに保存されます。
6. image
   - コマンド動作確認用サンプル画像が保存されているフォルダ。自作のずんだもんが入っています。いらなかったら消していただいて大丈夫です。
7. voice_list.csv
   - ボイスリスト。change_my_voiceの設定内容がここに保存されます。基本的に開く必要はないです。
8. output_voice_from_VOICEVOX.bat
   - VOICEVOXで音声ファイルを作成するbatファイル。基本的に開く必要はないです。
9. tmp
   - 一時的に出力されるファイル（VOICEVOXで出力した音声ファイル等）が保存されます。開く必要は全くないです。

## 注意

1. このソフトはWindows10上で使われることを想定しています。LinuxやMacで使う場合はbatファイルまわりをいじれば多分なんとかなります。
2. Pythonほぼ触ったことない + Discord bot作るの初めてで不慣れなところがあり一部コードが汚いかもしれないです。ごめんなさい。


## 導入が必要なソフト

このソフトを利用するために以下のソフト類のインストールが必要です。

1. python3のインストール
   [このサイト](https://www.python.jp/install/windows/install.html)を参考にしてください。

2. ffmpegのインストール
   [このサイト](https://jp.videoproc.com/edit-convert/how-to-download-and-install-ffmpeg.htm)の"**1. WindowsでFFmpegをダウンロード＆インストールする方法（Windows10対応）**"を参考にしてください。

3. discord.pyのインストール
   コマンドプロンプト(Win+Rで"ファイル名を指定して実行"をひらいて"cmd"を打ち込んだら出てくると思います）上で以下のコマンドを打ち込んで実行してください。

   ```bash
   py -m pip install -U discord.py[voice]
   ```
4. VOICEVOXのインストール
   [このサイト](https://voicevox.hiroshiba.jp/)から最新版（20211204段階でVersion 0.9.3) をダウンロードしてください。


## 起動方法


1. 上の導入が必要なソフトをすべてインストールします。
2. このフォルダ(yomiage_VOICEVOX)をわかりやすい場所に置きます。

2. DiscordのBotを作成し、招待します。（すでにチャットルームにBotを招待している場合は省略）[このサイト](https://note.com/exteoi/n/nf1c37cb26c41)の**1. Discord上のBotの作成**にある記述を参考にしてください。

   1. https://discord.com/developers/applications を開きます。
   2. 右上にあるNew Applicationを押す。適当な名前を入れてCreateを押します。
   3. 管理画面が開かれる。左のメニューのBotを押し、Add Botを押す。→Yes, do it!を選択（開かれない場合はDeveloper Portalから作成したアプリケーションを選択する）
   4. するとBuild-A-Botのところになんか出てくる。そのTOKENのところにあるCopyを押すとBotのTOKENがコピーできる。**のちに必要となるので保存しておく。**
   5. そのしたにPUBLIC BOT, REQUIRES OAUTH2 CODE GRANT, Presence Intent, Server Members Intentという項目があるが全部オフで大丈夫です。(灰色がオフ、青色がオン）
   6. 左のメニューのOAuth2→URL Generatorを開きます。 SCOPESでbotにチェックを入れます。
   7. BOT PERMISSIONSという項目が出てくると思うのでRead Messages/ViewChannels, Send Messages, Connect, Speakにチェックを入れてください。
   8. 一番下にあるGENERATED URLにあるリンクを開くとサーバー招待画面が出てくるので、追加したいサーバーを選択して認証します 。

3. discordbot_setting.pyを編集します。 （既に編集していたら省略）

   discordbot_setting.pyをテキストエディタで開いて（メモ帳でも可）、2-4)でコピーしていたTOKENを"自分のBotのアクセストークン"（1行目）のTOKEN = 'aaa'のaaaに打ち込んで保存してください。

4. VOICEVOXを起動します。

5. コマンドプロンプトを起動します。 (Win+Rで"ファイル名を指定して実行"をひらいて"cmd"を打ち込んだら出てくると思います）

6. チェンジディレクトリでこのフォルダの中身まで移動します。
   cd ディレクトリ名で移動できます。（https://eng-entrance.com/windows-command-cd を参照）例えば以下のようにする。
   
   ```bash
   cd C:\discord_bot\yomiage_VOICEVOX
   ```
   
7. コマンドプロンプトに以下を打ち込み、実行します。

   ```bash
   py discordbot.py
   ```


   コマンドプロンプト上に"起動しました"と出てきたら成功です。

8. おつかれさまでした。

## 終了方法

1. !leaveでボイスチャンネルからBOTを退場させておきます
2. コマンドプロンプト上で"ctrl + C"をおこなって終了させます

## その他

1. ほかのBOTとコマンドが被ってしまっている場合はdiscordbot_setting.pyの"シンタックス"（52行目付近）を変更してください。

2. 入退出通知と時報をデフォルトで切っておきたい場合はdiscordbot_setting.pyの"各種フラグのデフォルト値"（48行目付近）でTrueをFalseにしてください。

3. word_count_limitの数値を変えることで読み上げ文字数制限を変更できます。

4. 時報の時刻と内容は"時報のセリフリスト"（21行目付近）から変更できます。時報ボイスの変更は今のところ対応していません。


## 利用規約的なやつ

1. 本ソフトはオープンソースです。お金を払いたい場合はVOICEVOX様にどうぞ

   [VOICEVOX支援先](https://hiho.fanbox.cc/)

2. ソースコードの改変はご自由にどうぞ。再配布などもOKです。
   ただし、改変したものを配布する場合は改変したことが分かるようにファイル名を変更して、更新履歴に変更点を追記してください。

3. VOICEVOX及び各キャラの利用規約をよく読んでから使用してください。<br>
   [VOICEVOX本体利用規約(非公式Wiki)](https://wikiwiki.jp/voicevox/%E6%9C%AC%E4%BD%93%E5%88%A9%E7%94%A8%E8%A6%8F%E7%B4%84) <br>
   [東北ずん子利用の手引き](https://zunko.jp/guideline.html)<br>
   [春日部つむぎHP](https://tsukushinyoki10.wixsite.com/ktsumugiofficial)<br>
   [波音リツHP](http://ritsu73.is-mine.net/aboutritsu.html)

4. 本ソフトウェアにより生じた損害・不利益について、製作者は一切の責任を負いません。

5. 改善して欲しい点などあれば適当に実装しておいてください。
   ある程度リクエストは受け付けたいと思っていますが、製作者のスキル不足のため実装はかなり遅くなると思います。

6. 何かあればTwitterかメールまで<br>
   Twitter: @Kamimiya_yade<br>
   Gmail: kamimiya.lime@gmail.com

## 現在把握している要改善点・追加したい機能

- 各サーバーでつくられたカスタム絵文字の読み上げには対応しているが、デフォ絵文字の読み上げには対応していない。

  →ユニコード絵文字になっているみたいなので、文字コードまわりの設定をきちんとする必要があるかと思う。

- 英字が連続した時に文章を省略する機能が欲しい

- 一部コードがとても汚いので改善したい。（特にon_messageのif分岐がひどい）

- 時報ボイスの変更ができるようにしたい。
- ボイスチャンネル内に誰もいなくなったら自動に抜けるようにする。（手元のものでは実装済み）
- なんかdiscord.pyのサポートが2022年4月できれるらしい…。つくってから気がついた…。その対策を行う
  dislash.pyでスラッシュコマンドに対応させればいい？


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
  
