#学生証からidと名前を取得するサンプル

import nfc
from nfc.tag import Tag
from nfc.tag.tt3 import BlockCode, ServiceCode, Type3Tag
from nfc.tag.tt3_sony import FelicaStandard

SYSTEM_CODE = 0xFE00
SERVICE_CODE_NUMBER = 106

STUDENT_ID_BLOCK_NUMBER = 0x0000 # 学生番号が格納されているランダムサービスのブロック番号
NAME_BLOCK_NUMBER = 0x0001 # 氏名が格納されているランダムサービスのブロック番号

STUDENT_ID_OFFSET = 2 #学生番号を含むブロックの学生番号の開始位置
STUDENT_ID_LENGTH = 8 #学生番号の長さ

#学生番号を取得
def get_student_id(tag: Tag) -> str:
    service_code = ServiceCode(SERVICE_CODE_NUMBER, 0b001011) # 0b001011:ランダムサービス、認証なし、読み取り専用
    block_code = BlockCode(STUDENT_ID_BLOCK_NUMBER)
    
    raw_id = tag.read_without_encryption([service_code], [block_code]);
    return raw_id.decode("shift_jis")[STUDENT_ID_OFFSET : STUDENT_ID_OFFSET + STUDENT_ID_LENGTH]

#氏名を取得
def get_name(tag: Tag) -> str:
    service_code = ServiceCode(SERVICE_CODE_NUMBER, 0b001011) # 0b001011:ランダムサービス、認証なし、読み取り専用
    block_code = BlockCode(NAME_BLOCK_NUMBER)
    
    raw_name = tag.read_without_encryption([service_code], [block_code]);
    return raw_name.decode("shift_jis")


def on_connect(tag: Tag) -> bool:
    if isinstance(tag, FelicaStandard) and SYSTEM_CODE in tag.request_system_code():
        tag.idm, tag.pmm, *_ = tag.polling(SYSTEM_CODE)

        id = get_student_id(tag);
        name = get_name(tag);

        print("--------------------")
        print("id:   " + id)
        print("name: " + name)
    else:
        print("Invalid card")
    return True

with nfc.ContactlessFrontend("usb") as clf:
    while True: 
        clf.connect(rdwr={"on-connect": on_connect})