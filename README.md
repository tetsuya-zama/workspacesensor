# Workspace Sensor
## 概要

Raspberry Pi上の人感センサーの値(1 = 反応あり、0 = 反応なし)をPubNub上にpublishするスクリプト

## インストール
いずれかの方法で依存モジュールをインストールする

### （事前準備）pipがインストールされていない場合は先にインストール
```bash
$ sudo apt-get install python-dev python-pip
```

### A. setuptoolsでインストールする
```bash
$ sudo python setup.py build
```

### B. pipでインストールする

```bash
$ sudo pip install pubnub
$ sudo pip install rpi.gpio
```

## 環境設定

setting.jsonを設定する
```json
{
  "group":"${グループ名}",
  "publish_key":"${PubNubのpublish key}",
  "subscribe_key":"${PubNubのsubscribe key}",
  "id":"${ワークスペースのID}",
  "floor":"${ワークスペースのフロア名}",
  "name":"${ワークスペース名}",
  "duration":${センサーを確認する間隔 int 秒},
  "on_resistance":${0から1への変わりにくさ（抵抗値） 1以上のint},
  "off_resistance":${1から0への変わりにくさ（抵抗値） 1以上のint},
  "GPIO":{
    "sensor_pin":${センサーが繋がっているGPIOのPIN番号 int}
  }
}
```

### 間隔(duration)と抵抗(resistance)について
duration=>1 , on_resistance=>1, off_resistance=>10と設定した場合、

* 1秒に1回センサーの値を確認する
* センサーの値が"0"から"1"に変わった場合、すぐに"在席"と判断する
* センサーの値が"1"から"0"に変わった場合、その後"0"が10回続いた場合に"不在"と判断する
* "0"が10回続く前にセンサーの値が"1"に変わった場合、抵抗はリセットされる。次に"0"に変わってからさらに10回"0"が続いた場合、不在と判断する

という挙動になる。

### 複数センサーの取り扱いについて
GPIOに"and"もしくは"or"を設定することで、複数センサーの合議で判断するよう設定できる。

例:GPIOの12番、13番のいずれかが"1"の場合(or)、"1"と見做す
```json
{
  "group":"${グループ名}",
  "publish_key":"${PubNubのpublish key}",
  "subscribe_key":"${PubNubのsubscribe key}",
  "id":"${ワークスペースのID}",
  "floor":"${ワークスペースのフロア名}",
  "name":"${ワークスペース名}",
  "duration":${センサーを確認する間隔 int 秒},
  "on_resistance":${0から1への変わりにくさ（抵抗値） 1以上のint},
  "off_resistance":${1から0への変わりにくさ（抵抗値） 1以上のint},
  "GPIO":{
    "or":[
    	{"sensor_pin":12},
    	{"sensor_pin":13}
    ]
  }
}
```

## スタブモードからGPIO使用モードに切り替える

~~src/workspacesensor.pyの6行目を編集~~

*変更　sensor_pinを-1に設定するとスタブモード。ソースの修正不要*

## 開始と終了

### 開始

```bash
# GPIOと接続するためにはroot権限が必要
$ sudo sh ./start.sh
```
### 終了

```bash
$ sudo sh ./stop.sh
```

## PubNubメッセージング仕様

### チャンネル：plzcast_${グループ名}
#### 方向
クライアント(Publish) => センサー(Subscribe)

#### メッセージ
任意

#### 挙動
このメッセージをセンサー側が受け取ると、下記wkstatus_${グループ名}にセンサーの状態をPublishする

### チャンネル：wkstatus_${グループ名}
#### 方向
センサー(Publish) => クライアント(Subscribe)

#### メッセージ

```json
{
  "floor":"${フロア名}",
  "id":"${ワークスペースのID}",
  "name":"${ワークスペース名}",
  "status":${0 (人がいない=> 使用可) / 1 => (人がいる=> 使用中)}
}
```

#### 挙動

上記plzcast_${グループ名}をセンサーが受け取った時及び人感センサーの値が変わったタイミングで、クライアントに向けて現在のセンサーの状態をPublishする
