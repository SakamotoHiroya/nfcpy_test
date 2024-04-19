#タッチしたNFCのデータを読み取り出力するサンプル

import nfc

#接続時(タッチした時)に呼び出されるハンドラ
def on_connect(tag: nfc.tag.Tag) -> bool:
    print("connected: ".join(tag.dump()));
    return True #Trueにすると、カードを離すまで待つ。Falseにすると、処理を停止しない

def on_release(tag: nfc.tag.Tag) -> None:
    print("released")

with nfc.ContactlessFrontend("usb") as clf:
    while True:
        clf.connect(rdwr={"on-connect": on_connect, "on-release": on_release})