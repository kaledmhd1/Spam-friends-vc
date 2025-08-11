from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from protobuf_decoder.protobuf_decoder import Parser
import json
 
da = 'f2212101'
dec = [ '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '8a', '8b', '8c', '8d', '8e', '8f', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '9a', '9b', '9c', '9d', '9e', '9f', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'aa', 'ab', 'ac', 'ad', 'ae', 'af', 'b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'ba', 'bb', 'bc', 'bd', 'be', 'bf', 'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'da', 'db', 'dc', 'dd', 'de', 'df', 'e0', 'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'ea', 'eb', 'ec', 'ed', 'ee', 'ef', 'f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'fa', 'fb', 'fc', 'fd', 'fe', 'ff']
x= [ '1','01', '02', '03', '04', '05', '06', '07', '08', '09', '0a', '0b', '0c', '0d', '0e', '0f', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '1a', '1b', '1c', '1d', '1e', '1f', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '2a', '2b', '2c', '2d', '2e', '2f', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '3a', '3b', '3c', '3d', '3e', '3f', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '4a', '4b', '4c', '4d', '4e', '4f', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '5a', '5b', '5c', '5d', '5e', '5f', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '6a', '6b', '6c', '6d', '6e', '6f', '70', '71', 
'72', '73', '74', '75', '76', '77', '78', '79', '7a', '7b', '7c', '7d', '7e', '7f']

import random
def generate_random_hex_color():
    # List of top 50 colors without #
    top_colors = [
        "FF4500", "FFD700", "32CD32", "87CEEB", "9370DB",
        "FF69B4", "8A2BE2", "00BFFF", "1E90FF", "20B2AA",
        "00FA9A", "008000", "FFFF00", "FF8C00", "DC143C",
        "FF6347", "FFA07A", "FFDAB9", "CD853F", "D2691E",
        "BC8F8F", "F0E68C", "556B2F", "808000", "4682B4",
        "6A5ACD", "7B68EE", "8B4513", "C71585", "4B0082",
        "B22222", "228B22", "8B008B", "483D8B", "556B2F",
        "800000", "008080", "000080", "800080", "808080",
        "A9A9A9", "D3D3D3", "F0F0F0"
    ]
    # Select a random color from the list
    random_color = random.choice(top_colors)
    return random_color
def encrypt_packet(plain_text,key,iv):
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
    ra = random.randint(203, 213)
    final_num = str(ra).zfill(3)
    bunner = "902000"+final_num
    bunner = random.choice(numbers)
    return bunner
 
def create_varint_field(field_number, value):
    field_header = (field_number << 3) | 0  # Varint wire type is 0
    return encode_varint(field_header) + encode_varint(value)

def create_length_delimited_field(field_number, value):
    field_header = (field_number << 3) | 2  # Length-delimited wire type is 2
    encoded_value = value.encode() if isinstance(value, str) else value
    return encode_varint(field_header) + encode_varint(len(encoded_value)) + encoded_value

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
numbers = [
   

    902000208,
    902000209,
    902000210,
    902000211
]
 

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
    number = int(number)  # تحويل الرقم إلى عدد صحيح
    encoded_bytes = []    # إنشاء قائمة لتخزين البايتات المشفرة

    while True:  # حلقة تستمر حتى يتم تشفير الرقم بالكامل
        byte = number & 0x7F  # استخراج أقل 7 بتات من الرقم
        number >>= 7  # تحريك الرقم لليمين بمقدار 7 بتات
        if number:
            byte |= 0x80  # تعيين البت الثامن إلى 1 إذا كان الرقم لا يزال يحتوي على بتات إضافية

        encoded_bytes.append(byte)
        if not number:
            break  # التوقف إذا لم يتبقى بتات إضافية في الرقم

    return bytes(encoded_bytes).hex()  # تحويل قائمة البايتات إلى سلسلة هيكس وإرجاعها
print(Encrypt(12345678))
 
 
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
        w= 128
        xxx =len(da)/2-1
        xxx = str(xxx)[:1]
        for i in range(int(xxx)-1):
            w =w*128
        x1 =da[:2]
        x2 =da[2:4]
        x3 =da[4:6]
        x4 =da[6:8]
        x5 =da[8:10]
        return str(w*x.index(x5)+(dec.index(x2)*128)+dec.index(x1)+(dec.index(x3)*128*128)+(dec.index(x4)*128*128*128))

    if da != None and len(da) == 8:
        w= 128
        xxx =len(da)/2-1
        xxx = str(xxx)[:1]
        for i in range(int(xxx)-1):
            w =w*128
        x1 =da[:2]
        x2 =da[2:4]
        x3 =da[4:6]
        x4 =da[6:8]
        return str(w*x.index(x4)+(dec.index(x2)*128)+dec.index(x1)+(dec.index(x3)*128*128))
    
    return None

def parse_results(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {}
        field_data['wire_type'] = result.wire_type
        if result.wire_type == "varint":
            field_data['data'] = result.data
        if result.wire_type == "string":
            field_data['data'] = result.data
        if result.wire_type == "bytes":
            field_data['data'] = result.data
        elif result.wire_type == 'length_delimited':
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
        data = data['1']
        data = data['data']
        data = data['3']
    except KeyError:
        return ["OFFLINE" , packet]
    
    if data['data'] == 1:
        target = get_target(packet)
        return ["SOLO" , target]
    
    if data['data'] == 2:
        target = get_target(packet)
        leader = get_leader(packet)
        group_count = parsed_data["5"]["data"]["1"]["data"]["9"]["data"]
        return ["INSQUAD" , target , leader , group_count]
    
    if data['data'] == 3:
        target = get_target(packet)
        return ["INGAME" , target]
    
    if data['data'] == 5:
        target = get_target(packet)
        return ["INGAME" , target]
    
    if data['data'] == 7 or data['data'] == 6:
        target = get_target(packet)
        return ["IN SOCIAL ISLAND MODE .." , target]
    return "NOTFOUND"

def    get_packet(Msg   ):
 
    fields = {
        1: 1,
        2:{
            1: 9280892890,
            2: 3045484556,
            3: 1,
            4: Msg,
            5: 1721662811,
            7: 2,
            9: {
                1: "byte bot ",
                2: bunner_(),
                4: 228,
                7: 1,
            },
            10: "en",
            13: {
                2: 1,
                3: 1
            },
          
            

        }

    }
    packet = create_protobuf_packet(fields)
    packet =packet.hex()+"7200"
    header_lenth = len(encrypt_packet(packet))//2
    header_lenth = dec_to_hex(header_lenth)
    if len(header_lenth) ==2:
        #print(header_lenth)
       # print('len of headr == 2')
        final_packet = "1215000000"+header_lenth+encrypt_packet(packet)
       # print(final_packet)
        return bytes.fromhex(final_packet)
    
    if len(header_lenth) ==3:
      #  print(header_lenth)
      #  print('len of headr == 3')
        final_packet = "121500000"+header_lenth+encrypt_packet(packet)
       # print("121500000"+header_lenth)
        return bytes.fromhex(final_packet)
    if len(header_lenth) ==4:
      #  print('len of headr == 4')
        final_packet = "12150000"+header_lenth+encrypt_packet(packet)
        return bytes.fromhex(final_packet)
    if len(header_lenth) ==5:
        final_packet = "12150000"+header_lenth+encrypt_packet(packet)
        return bytes.fromhex(final_packet)
    
def    invite(   ):
 
    fields = {
        1: 17,
        2:{
            1: 9280892890,
            2: 1,
            3: 4,
            4: 62,
            5: "",
            7: 2,
            8:  5,
            9: 1,
            10: "0;0",
            13 :20
            

        }

    }
    packet = create_protobuf_packet(fields)
    packet =packet.hex()
    header_lenth = len(encrypt_packet(packet))//2
    header_lenth = dec_to_hex(header_lenth)
    if len(header_lenth) ==2:
        #print(header_lenth)
       # print('len of headr == 2')
        final_packet = "0515000000"+header_lenth+encrypt_packet(packet)
       # print(final_packet)
        return bytes.fromhex(final_packet)
    
    if len(header_lenth) ==3:
      #  print(header_lenth)
      #  print('len of headr == 3')
        final_packet = "051500000"+header_lenth+encrypt_packet(packet)
       # print("121500000"+header_lenth)
        return bytes.fromhex(final_packet)
    if len(header_lenth) ==4:
      #  print('len of headr == 4')
        final_packet = "05150000"+header_lenth+encrypt_packet(packet)
        return bytes.fromhex(final_packet)
    if len(header_lenth) ==5:
        final_packet = "05150000"+header_lenth+encrypt_packet(packet)
        return bytes.fromhex(final_packet)
def    invite1( id  ):
 
    fields = {
        1: 2,
        2:{
            1: id,
            2: "ME",
            4:1 ,

        }

    }
    packet = create_protobuf_packet(fields)
    packet =packet.hex()
    header_lenth = len(encrypt_packet(packet))//2
    header_lenth = dec_to_hex(header_lenth)
    if len(header_lenth) ==2:
        #print(header_lenth)
       # print('len of headr == 2')
        final_packet = "0515000000"+header_lenth+encrypt_packet(packet)
       # print(final_packet)
        return bytes.fromhex(final_packet)
    
    if len(header_lenth) ==3:
      #  print(header_lenth)
      #  print('len of headr == 3')
        final_packet = "051500000"+header_lenth+encrypt_packet(packet)
       # print("121500000"+header_lenth)
        return bytes.fromhex(final_packet)
    if len(header_lenth) ==4:
      #  print('len of headr == 4')
        final_packet = "05150000"+header_lenth+encrypt_packet(packet)
        return bytes.fromhex(final_packet)
    if len(header_lenth) ==5:
        final_packet = "05150000"+header_lenth+encrypt_packet(packet)
        return bytes.fromhex(final_packet)
def decrypt_api(cipher_text):
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plain_text = unpad(cipher.decrypt(bytes.fromhex(cipher_text)), AES.block_size)
    return plain_text.hex()

def encrypt_api(plain_text):
    plain_text = bytes.fromhex(plain_text)
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
    return cipher_text.hex()

    
packet='05 00 00 04 f3 08 85 d6 da 8d 08 10 05 20 06 2a e6 09 08 fd a2 cb ed 13 12 02 4d 45 18 01 20 03 32 c0 04 08 fd a2 cb ed 13 12 18 e1 b5 97 e2 81 b1 e1 b5 8f e3 85 a4 54 57 58 e3 85 a4 e2 9c bf ef b8 8e 1a 02 4d 45 20 b6 8f e4 b4 06 28 3b 30 84 cb d1 30 38 62 42 18 e3 b6 ce 64 e9 96 a3 61 e9 9f e0 61 a0 a3 e8 60 b5 c3 85 66 bb c7 d0 64 48 01 50 dd 01 58 ed 1f 7a 05 97 9a c5 b0 03 82 01 1d 08 a9 da f1 eb 04 12 03 4d 31 36 18 05 20 ab 87 d4 f0 04 2a 08 08 c8 9d 85 f3 04 10 03 92 01 0a 01 07 09 0a 0b 12 19 1a 1e 20 98 01 de 01 a0 01 c1 01 ba 01 0b 08 b2 aa a0 80 09 10 01 18 ac 02 c0 01 01 e8 01 01 88 02 03 92 02 08 be 17 ba 29 c2 05 b6 09 aa 02 05 08 01 10 97 3b aa 02 05 08 02 10 a6 36 aa 02 08 08 0f 10 d4 7a 18 90 4e aa 02 05 08 17 10 c3 33 aa 02 05 08 2b 10 88 31 aa 02 05 08 31 10 e3 32 aa 02 05 08 39 10 f2 56 aa 02 05 08 18 10 d4 7a aa 02 05 08 1a 10 d4 7a aa 02 05 08 1c 10 d4 7a aa 02 05 08 20 10 d4 7a aa 02 05 08 22 10 d4 7a aa 02 05 08 21 10 d4 7a aa 02 05 08 23 10 d4 7a aa 02 05 08 3d 10 d4 7a aa 02 05 08 41 10 d4 7a aa 02 05 08 49 10 e4 32 aa 02 05 08 4d 10 e4 32 aa 02 05 08 1b 10 d4 7a aa 02 05 08 34 10 d4 7a aa 02 05 08 28 10 e4 32 aa 02 05 08 29 10 e4 32 c2 02 27 12 03 1a 01 01 1a 05 08 50 12 01 63 1a 06 08 51 12 02 65 66 1a 0f 08 48 12 0b 01 04 05 06 07 f1 a8 02 f4 a8 02 22 00 d0 02 01 d8 02 e6 e5 ab af 03 ea 02 04 10 01 18 01 f2 02 08 08 88 ca b5 ee 01 10 1c 8a 03 00 92 03 00 98 03 d6 ed d2 b3 0b a2 03 23 c6 81 e2 92 93 e9 be b4 ef bc a1 ef bc ac ef bc a7 ef bc a5 ef bc b2 ef bc a9 ef bc ae ef bc b3 e2 9c 93 b0 03 02 c2 03 08 08 28 10 01 18 01 20 0d c2 03 08 08 1a 10 0f 18 02 20 08 ca 03 0a 08 02 10 c7 db f3 b4 06 18 01 ca 03 0a 08 01 10 fb f0 f3 b4 06 18 01 ca 03 0a 08 04 10 eb b3 eb b4 06 18 03 ca 03 0a 08 06 10 92 cf eb b4 06 18 01 ca 03 0a 08 09 10 aa ce f3 b4 06 18 01 d0 03 01 e2 03 01 52 32 a1 04 08 85 d6 da 8d 08 12 11 e0 a6 8c cd 9c cd a1 e1 b4 8d e3 85 a4 42 59 54 45 1a 02 4d 45 20 d5 8f e4 b4 06 28 38 30 a9 cb d1 30 38 32 42 14 8e bf ce 64 8b be ce 64 ce 96 e6 60 a2 9c a3 61 83 a0 e0 61 48 01 50 d5 01 58 e0 12 60 c9 d8 d0 ad 03 68 d1 ba 90 ae 03 7a 05 87 ff c4 b0 03 82 01 18 08 e5 da f1 eb 04 18 04 20 e5 87 d4 f0 04 2a 08 08 d1 9d 85 f3 04 10 03 92 01 09 01 07 09 0a 0b 12 19 1e 20 98 01 dd 01 a0 01 91 01 a8 01 b2 e9 f7 b1 03 c0 01 01 c8 01 01 d0 01 a5 e4 87 af 03 e8 01 01 88 02 08 92 02 08 b9 30 8c 0e f9 23 d3 28 aa 02 05 08 01 10 b6 39 aa 02 0b 08 0f 10 fa 91 01 18 88 27 20 02 aa 02 05 08 17 10 b0 4e aa 02 05 08 18 10 b5 31 aa 02 06 08 1b 10 fa 91 01 aa 02 05 08 1c 10 8a 32 aa 02 05 08 20 10 a1 32 aa 02 05 08 21 10 9e 32 aa 02 05 08 2b 10 ac 2f aa 02 05 08 02 10 e4 32 aa 02 06 08 1a 10 fa 91 01 aa 02 06 08 22 10 fa 91 01 aa 02 06 08 23 10 fa 91 01 aa 02 05 08 31 10 ac 2f aa 02 06 08 39 10 fa 91 01 aa 02 06 08 3d 10 fa 91 01 aa 02 06 08 41 10 fa 91 01 aa 02 05 08 49 10 e4 32 aa 02 05 08 4d 10 e4 32 aa 02 06 08 34 10 fa 91 01 aa 02 05 08 28 10 e4 32 aa 02 05 08 29 10 e4 32 b0 02 01 c2 02 31 12 03 1a 01 01 1a 19 08 48 12 0b 01 04 05 06 07 f1 a8 02 f4 a8 02 1a 08 08 03 10 01 20 b4 af 01 1a 05 08 50 12 01 63 1a 06 08 51 12 02 65 66 22 00 d8 02 db b0 93 af 03 ea 02 04 10 01 18 01 f2 02 00 8a 03 00 92 03 00 98 03 d0 98 de 21 a2 03 21 ef bc b3 ef bc a1 ef bc b2 ef bc af ef bc b5 ef bc 95 e3 85 a4 ef bc b4 ef bc a5 ef bc a1 ef bc ad b0 03 01 c2 03 08 08 28 10 01 18 04 20 01 c2 03 08 08 1a 10 0f 18 04 20 0d ca 03 0a 08 06 10 a4 ce f0 b4 06 18 01 ca 03 0a 08 02 10 c0 ca f3 b4 06 18 01 d0 03 01 e2 03 01 52 3a 01 01 40 0f 50 06 60 02 68 01 72 1e 31 37 32 31 33 30 35 30 31 34 32 37 35 33 30 35 36 32 36 5f 38 7a 33 6c 6d 6f 6c 71 7a 68 78 de 01 82 01 03 30 3b 30 88 01 80 e0 ae 85 f1 c8 93 96 19 a2 01 00 b0 01 de 01 e0 01 07 ea 01 04 49 44 43 32 fa 01 1e 31 37 32 31 33 30 35 30 31 34 32 37 35 33 30 38 30 38 39 5f 73 36 6c 6f 65 73 69 34 6c 6f'
def get_squad_leader(packet):
    json_result = get_available_room(packet)
    parsed_data = json.loads(json_result)
    return(parsed_data['5']['data']['1']['data'])

def    send_msg_in_room(Msg ,room_id  ):
    fields = {
        1: 1,
        2:{
            1: 9280892890,
            2: int(room_id),
            3: 3,
            4: f'[{generate_random_hex_color()}]{Msg}',
            5: 1721662811,
            7: 2,
            9: {
                1: "byte bot ",
                2: bunner_(),
                4: 228,
                7: 1,
            },
            10: "ar",
            13: {
                2: 1,
                3: 1
            },
        }
    }
    packet = create_protobuf_packet(fields)
    packet =packet.hex()+"7200"
    header_lenth = len(encrypt_packet(packet))//2
    header_lenth = dec_to_hex(header_lenth)
    if len(header_lenth) ==2:
        #print(header_lenth)
       # print('len of headr == 2')
        final_packet = "1215000000"+header_lenth+encrypt_packet(packet)
       # print(final_packet)
        return bytes.fromhex(final_packet)
    
    if len(header_lenth) ==3:
      #  print(header_lenth)
      #  print('len of headr == 3')
        final_packet = "121500000"+header_lenth+encrypt_packet(packet)
       # print("121500000"+header_lenth)
        return bytes.fromhex(final_packet)
    if len(header_lenth) ==4:
      #  print('len of headr == 4')
        final_packet = "12150000"+header_lenth+encrypt_packet(packet)
        return bytes.fromhex(final_packet)
    if len(header_lenth) ==5:
        final_packet = "12150000"+header_lenth+encrypt_packet(packet)
        return bytes.fromhex(final_packet)

def    join_room_chanel( room_id  ):
    fields = {
        1: 3,
        2:{
            1: int(room_id),
            2: 3,
            3: "ar",
        }
    }
    packet = create_protobuf_packet(fields)
    packet =packet.hex()+"7200"
    header_lenth = len(encrypt_packet(packet))//2
    header_lenth = dec_to_hex(header_lenth)
    if len(header_lenth) ==2:
        #print(header_lenth)
       # print('len of headr == 2')
        final_packet = "1215000000"+header_lenth+encrypt_packet(packet)
       # print(final_packet)
        return bytes.fromhex(final_packet)
    
    if len(header_lenth) ==3:
      #  print(header_lenth)
      #  print('len of headr == 3')
        final_packet = "121500000"+header_lenth+encrypt_packet(packet)
       # print("121500000"+header_lenth)
        return bytes.fromhex(final_packet)
    if len(header_lenth) ==4:
      #  print('len of headr == 4')
        final_packet = "12150000"+header_lenth+encrypt_packet(packet)
        return bytes.fromhex(final_packet)
    if len(header_lenth) ==5:
        final_packet = "12150000"+header_lenth+encrypt_packet(packet)
        return bytes.fromhex(final_packet)

def    leave_room_chanel( room_id  ):
    fields = {
        1: 4,
        2:{
            1: int(room_id),
            2: 3,
            3: "ar",
        }
    }
    packet = create_protobuf_packet(fields)
    packet =packet.hex()+"7200"
    header_lenth = len(encrypt_packet(packet))//2
    header_lenth = dec_to_hex(header_lenth)
    if len(header_lenth) ==2:
        #print(header_lenth)
       # print('len of headr == 2')
        final_packet = "1215000000"+header_lenth+encrypt_packet(packet)
       # print(final_packet)
        return bytes.fromhex(final_packet)
    
    if len(header_lenth) ==3:
      #  print(header_lenth)
      #  print('len of headr == 3')
        final_packet = "121500000"+header_lenth+encrypt_packet(packet)
       # print("121500000"+header_lenth)
        return bytes.fromhex(final_packet)
    if len(header_lenth) ==4:
      #  print('len of headr == 4')
        final_packet = "12150000"+header_lenth+encrypt_packet(packet)
        return bytes.fromhex(final_packet)
    if len(header_lenth) ==5:
        final_packet = "12150000"+header_lenth+encrypt_packet(packet)
        return bytes.fromhex(final_packet)
 
 