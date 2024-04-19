#学生証からidと名前を取得するサンプル

import nfc
from nfc.tag import Tag
from nfc.tag.tt3 import BlockCode, ServiceCode, Type3Tag
from nfc.tag.tt3_sony import FelicaStandard

SYSTEM_CODE = 0xFE00

def on_connect(tag: Tag) -> bool:
    if isinstance(tag, FelicaStandard) and SYSTEM_CODE in tag.request_system_code():
        print("Felica connected.")

        tag.idm, tag.pmm, *_ = tag.polling(SYSTEM_CODE)

        service_code = ServiceCode(106, 0b001011)

        id_block_code = BlockCode(0x0000)
        name_block_code = BlockCode(0x0001)

        raw_id = tag.read_without_encryption([service_code], [id_block_code])
        raw_name = tag.read_without_encryption([service_code], [name_block_code])

        print("id:   " + raw_id.decode("shift_jis")[2:10]) #デコードした文字列から学生番号を切り出す
        print("name: " + raw_name.decode("shift_jis"))
    else:
        print("This card is not Felica.")
    return True

def on_release(tag: Tag) -> None:
    print("Card released.")

with nfc.ContactlessFrontend("usb") as clf:
    while True: 
        clf.connect(rdwr={"on-connect": on_connect, "on-release": on_release})