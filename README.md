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
  "GPIO":{
    "sensor_pin":${センサーが繋がっているGPIOのPIN番号 int}
  }
}
```

## スタブモードからGPIO使用モードに切り替える

src/workspacesensor.pyの6行目を編集

編集前（スタブモード）
```python
import sensorstub as sensor
```
編集後（GPIO使用モード）
```python
import sensor
```

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
