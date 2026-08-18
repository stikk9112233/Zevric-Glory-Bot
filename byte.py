import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from protobuf_decoder.protobuf_decoder import Parser
import json
import bot_invite_pb2
import bot_mode_pb2
import base64
import spam_join_pb2
import hardest_pb2
import time
from datetime import datetime

da = "f2212101"
dec = [
    "80",
    "81",
    "82",
    "83",
    "84",
    "85",
    "86",
    "87",
    "88",
    "89",
    "8a",
    "8b",
    "8c",
    "8d",
    "8e",
    "8f",
    "90",
    "91",
    "92",
    "93",
    "94",
    "95",
    "96",
    "97",
    "98",
    "99",
    "9a",
    "9b",
    "9c",
    "9d",
    "9e",
    "9f",
    "a0",
    "a1",
    "a2",
    "a3",
    "a4",
    "a5",
    "a6",
    "a7",
    "a8",
    "a9",
    "aa",
    "ab",
    "ac",
    "ad",
    "ae",
    "af",
    "b0",
    "b1",
    "b2",
    "b3",
    "b4",
    "b5",
    "b6",
    "b7",
    "b8",
    "b9",
    "ba",
    "bb",
    "bc",
    "bd",
    "be",
    "bf",
    "c0",
    "c1",
    "c2",
    "c3",
    "c4",
    "c5",
    "c6",
    "c7",
    "c8",
    "c9",
    "ca",
    "cb",
    "cc",
    "cd",
    "ce",
    "cf",
    "d0",
    "d1",
    "d2",
    "d3",
    "d4",
    "d5",
    "d6",
    "d7",
    "d8",
    "d9",
    "da",
    "db",
    "dc",
    "dd",
    "de",
    "df",
    "e0",
    "e1",
    "e2",
    "e3",
    "e4",
    "e5",
    "e6",
    "e7",
    "e8",
    "e9",
    "ea",
    "eb",
    "ec",
    "ed",
    "ee",
    "ef",
    "f0",
    "f1",
    "f2",
    "f3",
    "f4",
    "f5",
    "f6",
    "f7",
    "f8",
    "f9",
    "fa",
    "fb",
    "fc",
    "fd",
    "fe",
    "ff",
]
x = [
    "1",
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "09",
    "0a",
    "0b",
    "0c",
    "0d",
    "0e",
    "0f",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "1a",
    "1b",
    "1c",
    "1d",
    "1e",
    "1f",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
    "26",
    "27",
    "28",
    "29",
    "2a",
    "2b",
    "2c",
    "2d",
    "2e",
    "2f",
    "30",
    "31",
    "32",
    "33",
    "34",
    "35",
    "36",
    "37",
    "38",
    "39",
    "3a",
    "3b",
    "3c",
    "3d",
    "3e",
    "3f",
    "40",
    "41",
    "42",
    "43",
    "44",
    "45",
    "46",
    "47",
    "48",
    "49",
    "4a",
    "4b",
    "4c",
    "4d",
    "4e",
    "4f",
    "50",
    "51",
    "52",
    "53",
    "54",
    "55",
    "56",
    "57",
    "58",
    "59",
    "5a",
    "5b",
    "5c",
    "5d",
    "5e",
    "5f",
    "60",
    "61",
    "62",
    "63",
    "64",
    "65",
    "66",
    "67",
    "68",
    "69",
    "6a",
    "6b",
    "6c",
    "6d",
    "6e",
    "6f",
    "70",
    "71",
    "72",
    "73",
    "74",
    "75",
    "76",
    "77",
    "78",
    "79",
    "7a",
    "7b",
    "7c",
    "7d",
    "7e",
    "7f",
]


def generate_random_hex_color():
    # List of top 50 colors without #
    top_colors = [
    "902000156", "902000157", "902000172", "902000186", "902000191", 
    "902000231", "902000211", "902032018", "902032017", "902032014", 
    "902027016", "902033026", "902033027", "902042014", "902044006", 
    "902045005", "902045009", "902044003", "902042014"
]
    # Select a random color from the list
    random_color = random.choice(top_colors)
    return random_color





def encrypt_packet(plain_text, key, iv):
    plain_text = bytes.fromhex(plain_text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()


def dec_to_hex(ask):
    ask_result = hex(ask)
    final_result = str(ask_result)[2:]
    if len(final_result) == 1:
        final_result = "0" + final_result
        return final_result
    else:
        return final_result


class ParsedResult:
    def __init__(self, field, wire_type, data):
        self.field = field
        self.wire_type = wire_type
        self.data = data


class ParsedResultEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ParsedResult):
            return {"field": obj.field, "wire_type": obj.wire_type, "data": obj.data}
        return super().default(obj)







def bunner_():
    bunner_1 = "902033001"
    bunner_2 = "902033013"
    bunner_3 = "902000172"
    bunner_4 = "902000271"
    bunner_5 = "902032014"
    bunner_6 = "902045004"
    bunner_7 = "902043009"
    bunner_8 = "902000003"
    bunner_9 = "902027027"
    bunner_10 = "902000306"
    bunner_11 = "902033017"
    
    # وضع كل البنرات في قائمة
    banners = [bunner_1, bunner_2, bunner_3, bunner_4, bunner_5,
               bunner_6, bunner_7, bunner_8, bunner_9, bunner_10, bunner_11]
    
    # اختيار بنر عشوائي من القائمة
    selected_bunner = random.choice(banners)
    
    # تحويل البنر إلى عدد صحيح إذا كان المطلوب نوع int
    selected_bunner_int = int(selected_bunner)  # تحويل إلى int
    
    return selected_bunner_int




def create_varint_field(field_number, value):
    field_header = (field_number << 3) | 0  # Varint wire type is 0
    return encode_varint(field_header) + encode_varint(value)


def create_length_delimited_field(field_number, value):
    field_header = (field_number << 3) | 2  # Length-delimited wire type is 2
    encoded_value = value.encode() if isinstance(value, str) else value
    return (
        encode_varint(field_header) + encode_varint(len(encoded_value)) + encoded_value
    )


def create_protobuf_packet(fields):
    packet = bytearray()    
    for field, value in fields.items():
        if isinstance(value, dict):
            nested_packet = create_protobuf_packet(value)
            packet.extend(create_length_delimited_field(field, nested_packet))
        elif isinstance(value, int):
            packet.extend(create_varint_field(field, value))
        elif isinstance(value, str) or isinstance(value, bytes):
            packet.extend(create_length_delimited_field(field, value))
    
    return packet        


def encode_varint(number):
    # Ensure the number is non-negative
    if number < 0:
        raise ValueError("Number must be non-negative")

    # Initialize an empty list to store the varint bytes
    encoded_bytes = []

    # Continuously divide the number by 128 and store the remainder,
    # and add 128 to the remainder if there are still higher bits set
    while True:
        byte = number & 0x7F
        number >>= 7
        if number:
            byte |= 0x80
        encoded_bytes.append(byte)
        if not number:
            break

    # Return the varint bytes as bytes object
    return bytes(encoded_bytes)


# Example usage
numbers = [902000208, 902000209, 902000210, 902000211]


def Encrypt_ID(number):
    number = int(number)
    encoded_bytes = []
    while True:
        byte = number & 0x7F
        number >>= 7
        if number:
            byte |= 0x80
        encoded_bytes.append(byte)
        if not number:
            break
    return bytes(encoded_bytes).hex()


def Encrypt(number):
    number = int(number)
    encoded_bytes = []

    while True:
        byte = number & 0x7F
        number >>= 7
        if number:
            byte |= 0x80

        encoded_bytes.append(byte)
        if not number:
            break
    return bytes(encoded_bytes).hex()


print(Encrypt(11057708226))


def Decrypt(encoded_bytes):
    encoded_bytes = bytes.fromhex(encoded_bytes)
    number = 0
    shift = 0
    for byte in encoded_bytes:
        value = byte & 0x7F
        number |= value << shift
        shift += 7
        if not byte & 0x80:
            break
    return number


def Decrypt_ID(da):
    if da != None and len(da) == 10:
        w = 128
        xxx = len(da) / 2 - 1
        xxx = str(xxx)[:1]
        for i in range(int(xxx) - 1):
            w = w * 128
        x1 = da[:2]
        x2 = da[2:4]
        x3 = da[4:6]
        x4 = da[6:8]
        x5 = da[8:10]
        return str(
            w * x.index(x5)
            + (dec.index(x2) * 128)
            + dec.index(x1)
            + (dec.index(x3) * 128 * 128)
            + (dec.index(x4) * 128 * 128 * 128)
        )

    if da != None and len(da) == 8:
        w = 128
        xxx = len(da) / 2 - 1
        xxx = str(xxx)[:1]
        for i in range(int(xxx) - 1):
            w = w * 128
        x1 = da[:2]
        x2 = da[2:4]
        x3 = da[4:6]
        x4 = da[6:8]
        return str(
            w * x.index(x4)
            + (dec.index(x2) * 128)
            + dec.index(x1)
            + (dec.index(x3) * 128 * 128)
        )

    return None


def parse_results(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {}
        field_data["wire_type"] = result.wire_type
        if result.wire_type == "varint":
            field_data["data"] = result.data
        if result.wire_type == "string":
            field_data["data"] = result.data
        if result.wire_type == "bytes":
            field_data["data"] = result.data
        elif result.wire_type == "length_delimited":
            field_data["data"] = parse_results(result.data.results)
        result_dict[result.field] = field_data
    return result_dict


def get_available_room(input_text):
    try:
        parsed_results = Parser().parse(input_text)
        parsed_results_objects = parsed_results
        parsed_results_dict = parse_results(parsed_results_objects)
        json_data = json.dumps(parsed_results_dict)
        return json_data
    except Exception as e:
        print(f"error {e}")
        return None


def get_leader(packet):
    json_result = get_available_room(packet)
    parsed_data = json.loads(json_result)
    json_data = parsed_data["5"]["data"]["1"]["data"]["8"]["data"]
    return str(json_data)


def get_target(packet):
    json_result = get_available_room(packet)
    parsed_data = json.loads(json_result)
    json_data = parsed_data["5"]["data"]["1"]["data"]["1"]["data"]
    return str(json_data)


def get_player_status(packet):
    json_result = get_available_room(packet)
    parsed_data = json.loads(json_result)
    json_data = parsed_data["5"]
    keys = list(json_data.keys())
    data = keys[1]
    keys = list(json_data[data].keys())
    
    try:
        data = json_data[data]
        data = data["1"]
        data = data["data"]
        data = data["3"]
    except KeyError:
        return ["غير متصل", packet]

    if data["data"] == 1:
        target = get_target(packet)
        return ["في وضع اللعب الفردي (Solo)", target]

    if data["data"] == 2:
        target = get_target(packet)
        leader = get_leader(packet)
        group_count = parsed_data["5"]["data"]["1"]["data"]["9"]["data"]
        return ["في مجموعة داخل اللعبة (Squad)", target, leader, group_count]

    if data["data"] == 3:
        target = get_target(packet)
        return ["على وشك دخول المباراة (On the verge of joining the game)", target]

    if data["data"] == 5:
        target = get_target(packet)
        return ["على وشك دخول المباراة (On the verge of joining the game)", target]

    if data["data"] == 7 or data["data"] == 6:
        target = get_target(packet)
        return ["في جزيرة الصداقة (Friendship Island Mode)", target]
    
    return "غير موجود (Not Found)"
