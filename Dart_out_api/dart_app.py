from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
 
app = Flask(__name__)
app.config["DEBUG"] = True
 
# variables (names no longer match any function name)
out_type = None
start_num = None
first_double_hit = None
second_double_hit = None
third_double_hit = None
first_straight_hit = None
second_straight_hit = None
third_straight_hit = None
left_over = None
out_path_one = []
out_path_two = []
out_path_three = []
 
 
@app.route('/', methods=['GET'])
def index():
    return render_template('dashboard.html')
 
 
@app.route('/outs-page', methods=['GET'])
def outs_page():
    return render_template('out.html')
 
 
@app.route('/statistics-page', methods=['GET'])
def statistics_page():
    return render_template('statistics.html')
 
 
@app.route("/out-type", methods=["POST"])
def select_out_type():
    global out_type
    chosen = request.form.get("out_type")
    if chosen == "straight":
        out_type = "straight"
    elif chosen == "double":
        out_type = "double"
    return render_template('out.html')
 
 

# D = double, T = triple, S = single. Paste below your imports / global variables.
 
def respond(message, route="", left=""):
    return render_template("out.html", message=message, route=route, left_over=left)
 
 
# ======================= START NUMBER =======================
 
@app.route("/first-num", methods=["POST"])   # 3 darts left
def enter_start_num():
    global start_num
    start_num = int(request.form.get("start"))
 
    if out_type == "straight":
        match start_num:
            case n if n < 1:
                return respond("Enter a number of 1 or more.", "", n)
            case 1:
                return respond("1 left. Your out:", "S1", 1)
            case 2:
                return respond("2 left. Your out:", "D1", 2)
            case 3:
                return respond("3 left. Your out:", "T1", 3)
            case 4:
                return respond("4 left. Your out:", "D2", 4)
            case 5:
                return respond("5 left. Your out:", "S5", 5)
            case 6:
                return respond("6 left. Your out:", "T2", 6)
            case 7:
                return respond("7 left. Your out:", "S7", 7)
            case 8:
                return respond("8 left. Your out:", "D4", 8)
            case 9:
                return respond("9 left. Your out:", "T3", 9)
            case 10:
                return respond("10 left. Your out:", "D5", 10)
            case 11:
                return respond("11 left. Your out:", "S11", 11)
            case 12:
                return respond("12 left. Your out:", "T4", 12)
            case 13:
                return respond("13 left. Your out:", "S13", 13)
            case 14:
                return respond("14 left. Your out:", "D7", 14)
            case 15:
                return respond("15 left. Your out:", "T5", 15)
            case 16:
                return respond("16 left. Your out:", "D8", 16)
            case 17:
                return respond("17 left. Your out:", "S17", 17)
            case 18:
                return respond("18 left. Your out:", "T6", 18)
            case 19:
                return respond("19 left. Your out:", "S19", 19)
            case 20:
                return respond("20 left. Your out:", "D10", 20)
            case 21:
                return respond("21 left. Your out:", "T7", 21)
            case 22:
                return respond("22 left. Your out:", "D11", 22)
            case 23:
                return respond("23 left. Your out:", "D11 S1", 23)
            case 24:
                return respond("24 left. Your out:", "T8", 24)
            case 25:
                return respond("25 left. Your out:", "Outer Bull", 25)
            case 26:
                return respond("26 left. Your out:", "D13", 26)
            case 27:
                return respond("27 left. Your out:", "T9", 27)
            case 28:
                return respond("28 left. Your out:", "D14", 28)
            case 29:
                return respond("29 left. Your out:", "D14 S1", 29)
            case 30:
                return respond("30 left. Your out:", "T10", 30)
            case 31:
                return respond("31 left. Your out:", "T10 S1", 31)
            case 32:
                return respond("32 left. Your out:", "D16", 32)
            case 33:
                return respond("33 left. Your out:", "T11", 33)
            case 34:
                return respond("34 left. Your out:", "D17", 34)
            case 35:
                return respond("35 left. Your out:", "D17 S1", 35)
            case 36:
                return respond("36 left. Your out:", "T12", 36)
            case 37:
                return respond("37 left. Your out:", "T12 S1", 37)
            case 38:
                return respond("38 left. Your out:", "D19", 38)
            case 39:
                return respond("39 left. Your out:", "T13", 39)
            case 40:
                return respond("40 left. Your out:", "D20", 40)
            case 41:
                return respond("41 left. Your out:", "D20 S1", 41)
            case 42:
                return respond("42 left. Your out:", "T14", 42)
            case 43:
                return respond("43 left. Your out:", "T14 S1", 43)
            case 44:
                return respond("44 left. Your out:", "T14 D1", 44)
            case 45:
                return respond("45 left. Your out:", "T15", 45)
            case 46:
                return respond("46 left. Your out:", "T15 S1", 46)
            case 47:
                return respond("47 left. Your out:", "T15 D1", 47)
            case 48:
                return respond("48 left. Your out:", "T16", 48)
            case 49:
                return respond("49 left. Your out:", "T16 S1", 49)
            case 50:
                return respond("50 left. Your out:", "Bull", 50)
            case 51:
                return respond("51 left. Your out:", "T17", 51)
            case 52:
                return respond("52 left. Your out:", "T17 S1", 52)
            case 53:
                return respond("53 left. Your out:", "T17 D1", 53)
            case 54:
                return respond("54 left. Your out:", "T18", 54)
            case 55:
                return respond("55 left. Your out:", "T18 S1", 55)
            case 56:
                return respond("56 left. Your out:", "T18 D1", 56)
            case 57:
                return respond("57 left. Your out:", "T19", 57)
            case 58:
                return respond("58 left. Your out:", "T19 S1", 58)
            case 59:
                return respond("59 left. Your out:", "T19 D1", 59)
            case 60:
                return respond("60 left. Your out:", "T20", 60)
            case 61:
                return respond("61 left. Your out:", "T20 S1", 61)
            case 62:
                return respond("62 left. Your out:", "T20 D1", 62)
            case 63:
                return respond("63 left. Your out:", "T20 T1", 63)
            case 64:
                return respond("64 left. Your out:", "T20 D2", 64)
            case 65:
                return respond("65 left. Your out:", "T20 S5", 65)
            case 66:
                return respond("66 left. Your out:", "T20 T2", 66)
            case 67:
                return respond("67 left. Your out:", "T20 S7", 67)
            case 68:
                return respond("68 left. Your out:", "T20 D4", 68)
            case 69:
                return respond("69 left. Your out:", "T20 T3", 69)
            case 70:
                return respond("70 left. Your out:", "T20 D5", 70)
            case 71:
                return respond("71 left. Your out:", "T20 S11", 71)
            case 72:
                return respond("72 left. Your out:", "T20 T4", 72)
            case 73:
                return respond("73 left. Your out:", "T20 S13", 73)
            case 74:
                return respond("74 left. Your out:", "T20 D7", 74)
            case 75:
                return respond("75 left. Your out:", "T20 T5", 75)
            case 76:
                return respond("76 left. Your out:", "T20 D8", 76)
            case 77:
                return respond("77 left. Your out:", "T20 S17", 77)
            case 78:
                return respond("78 left. Your out:", "T20 T6", 78)
            case 79:
                return respond("79 left. Your out:", "T20 S19", 79)
            case 80:
                return respond("80 left. Your out:", "T20 D10", 80)
            case 81:
                return respond("81 left. Your out:", "T20 T7", 81)
            case 82:
                return respond("82 left. Your out:", "T20 D11", 82)
            case 83:
                return respond("83 left. Your out:", "T19 D13", 83)
            case 84:
                return respond("84 left. Your out:", "T20 T8", 84)
            case 85:
                return respond("85 left. Your out:", "T20 Outer Bull", 85)
            case 86:
                return respond("86 left. Your out:", "T20 D13", 86)
            case 87:
                return respond("87 left. Your out:", "T20 T9", 87)
            case 88:
                return respond("88 left. Your out:", "T20 D14", 88)
            case 89:
                return respond("89 left. Your out:", "T19 D16", 89)
            case 90:
                return respond("90 left. Your out:", "T20 T10", 90)
            case 91:
                return respond("91 left. Your out:", "T19 D17", 91)
            case 92:
                return respond("92 left. Your out:", "T20 D16", 92)
            case 93:
                return respond("93 left. Your out:", "T20 T11", 93)
            case 94:
                return respond("94 left. Your out:", "T20 D17", 94)
            case 95:
                return respond("95 left. Your out:", "T19 D19", 95)
            case 96:
                return respond("96 left. Your out:", "T20 T12", 96)
            case 97:
                return respond("97 left. Your out:", "T19 D20", 97)
            case 98:
                return respond("98 left. Your out:", "T20 D19", 98)
            case 99:
                return respond("99 left. Your out:", "T20 T13", 99)
            case 100:
                return respond("100 left. Your out:", "T20 D20", 100)
            case 101:
                return respond("101 left. Your out:", "T17 Bull", 101)
            case 102:
                return respond("102 left. Your out:", "T20 T14", 102)
            case 103:
                return respond("103 left. Your out:", "T20 T14 S1", 103)
            case 104:
                return respond("104 left. Your out:", "T18 Bull", 104)
            case 105:
                return respond("105 left. Your out:", "T20 T15", 105)
            case 106:
                return respond("106 left. Your out:", "T20 T15 S1", 106)
            case 107:
                return respond("107 left. Your out:", "T19 Bull", 107)
            case 108:
                return respond("108 left. Your out:", "T20 T16", 108)
            case 109:
                return respond("109 left. Your out:", "T20 T16 S1", 109)
            case 110:
                return respond("110 left. Your out:", "T20 Bull", 110)
            case 111:
                return respond("111 left. Your out:", "T20 T17", 111)
            case 112:
                return respond("112 left. Your out:", "T20 T17 S1", 112)
            case 113:
                return respond("113 left. Your out:", "T20 T17 D1", 113)
            case 114:
                return respond("114 left. Your out:", "T20 T18", 114)
            case 115:
                return respond("115 left. Your out:", "T20 T18 S1", 115)
            case 116:
                return respond("116 left. Your out:", "T20 T18 D1", 116)
            case 117:
                return respond("117 left. Your out:", "T20 T19", 117)
            case 118:
                return respond("118 left. Your out:", "T20 T19 S1", 118)
            case 119:
                return respond("119 left. Your out:", "T20 T19 D1", 119)
            case 120:
                return respond("120 left. Your out:", "T20 T20", 120)
            case 121:
                return respond("121 left. Your out:", "T20 T20 S1", 121)
            case 122:
                return respond("122 left. Your out:", "T20 T20 D1", 122)
            case 123:
                return respond("123 left. Your out:", "T20 T20 T1", 123)
            case 124:
                return respond("124 left. Your out:", "T20 T20 D2", 124)
            case 125:
                return respond("125 left. Your out:", "T20 T20 S5", 125)
            case 126:
                return respond("126 left. Your out:", "T20 T20 T2", 126)
            case 127:
                return respond("127 left. Your out:", "T20 T20 S7", 127)
            case 128:
                return respond("128 left. Your out:", "T20 T20 D4", 128)
            case 129:
                return respond("129 left. Your out:", "T20 T20 T3", 129)
            case 130:
                return respond("130 left. Your out:", "T20 T20 D5", 130)
            case 131:
                return respond("131 left. Your out:", "T20 T20 S11", 131)
            case 132:
                return respond("132 left. Your out:", "T20 T20 T4", 132)
            case 133:
                return respond("133 left. Your out:", "T20 T20 S13", 133)
            case 134:
                return respond("134 left. Your out:", "T20 T20 D7", 134)
            case 135:
                return respond("135 left. Your out:", "T20 T20 T5", 135)
            case 136:
                return respond("136 left. Your out:", "T20 T20 D8", 136)
            case 137:
                return respond("137 left. Your out:", "T20 T20 S17", 137)
            case 138:
                return respond("138 left. Your out:", "T20 T20 T6", 138)
            case 139:
                return respond("139 left. Your out:", "T20 T20 S19", 139)
            case 140:
                return respond("140 left. Your out:", "T20 T20 D10", 140)
            case 141:
                return respond("141 left. Your out:", "T20 T20 T7", 141)
            case 142:
                return respond("142 left. Your out:", "T20 T20 D11", 142)
            case 143:
                return respond("143 left. Your out:", "T20 T19 D13", 143)
            case 144:
                return respond("144 left. Your out:", "T20 T20 T8", 144)
            case 145:
                return respond("145 left. Your out:", "T20 T20 Outer Bull", 145)
            case 146:
                return respond("146 left. Your out:", "T20 T20 D13", 146)
            case 147:
                return respond("147 left. Your out:", "T20 T20 T9", 147)
            case 148:
                return respond("148 left. Your out:", "T20 T20 D14", 148)
            case 149:
                return respond("149 left. Your out:", "T20 T19 D16", 149)
            case 150:
                return respond("150 left. Your out:", "T20 T20 T10", 150)
            case 151:
                return respond("151 left. Your out:", "T20 T19 D17", 151)
            case 152:
                return respond("152 left. Your out:", "T20 T20 D16", 152)
            case 153:
                return respond("153 left. Your out:", "T20 T20 T11", 153)
            case 154:
                return respond("154 left. Your out:", "T20 T20 D17", 154)
            case 155:
                return respond("155 left. Your out:", "T20 T19 D19", 155)
            case 156:
                return respond("156 left. Your out:", "T20 T20 T12", 156)
            case 157:
                return respond("157 left. Your out:", "T20 T19 D20", 157)
            case 158:
                return respond("158 left. Your out:", "T20 T20 D19", 158)
            case 159:
                return respond("159 left. Your out:", "T20 T20 T13", 159)
            case 160:
                return respond("160 left. Your out:", "T20 T20 D20", 160)
            case 161:
                return respond("161 left. Your out:", "T20 T17 Bull", 161)
            case 162:
                return respond("162 left. Your out:", "T20 T20 T14", 162)
            case 164:
                return respond("164 left. Your out:", "T20 T18 Bull", 164)
            case 165:
                return respond("165 left. Your out:", "T20 T20 T15", 165)
            case 167:
                return respond("167 left. Your out:", "T20 T19 Bull", 167)
            case 168:
                return respond("168 left. Your out:", "T20 T20 T16", 168)
            case 170:
                return respond("170 left. Your out:", "T20 T20 Bull", 170)
            case 171:
                return respond("171 left. Your out:", "T20 T20 T17", 171)
            case 174:
                return respond("174 left. Your out:", "T20 T20 T18", 174)
            case 177:
                return respond("177 left. Your out:", "T20 T20 T19", 177)
            case 180:
                return respond("180 left. Your out:", "T20 T20 T20", 180)
            case n if n > 180:
                return respond("No out possible. 180 is the highest straight out.", "", n)
            case n:
                return respond(f"{n} has no 3-dart straight out.", "", n)
 
    elif out_type == "double":
        match start_num:
            case n if n < 2:
                return respond("Enter a number of 2 or more (1 is impossible in double out).", "", n)
            case 2:
                return respond("2 left. Your out:", "D1", 2)
            case 3:
                return respond("3 left. Your out:", "S1 D1", 3)
            case 4:
                return respond("4 left. Your out:", "D2", 4)
            case 5:
                return respond("5 left. Your out:", "T1 D1", 5)
            case 6:
                return respond("6 left. Your out:", "D3", 6)
            case 7:
                return respond("7 left. Your out:", "S5 D1", 7)
            case 8:
                return respond("8 left. Your out:", "D4", 8)
            case 9:
                return respond("9 left. Your out:", "S7 D1", 9)
            case 10:
                return respond("10 left. Your out:", "D5", 10)
            case 11:
                return respond("11 left. Your out:", "T3 D1", 11)
            case 12:
                return respond("12 left. Your out:", "D6", 12)
            case 13:
                return respond("13 left. Your out:", "S11 D1", 13)
            case 14:
                return respond("14 left. Your out:", "D7", 14)
            case 15:
                return respond("15 left. Your out:", "S13 D1", 15)
            case 16:
                return respond("16 left. Your out:", "D8", 16)
            case 17:
                return respond("17 left. Your out:", "T5 D1", 17)
            case 18:
                return respond("18 left. Your out:", "D9", 18)
            case 19:
                return respond("19 left. Your out:", "S17 D1", 19)
            case 20:
                return respond("20 left. Your out:", "D10", 20)
            case 21:
                return respond("21 left. Your out:", "S19 D1", 21)
            case 22:
                return respond("22 left. Your out:", "D11", 22)
            case 23:
                return respond("23 left. Your out:", "T7 D1", 23)
            case 24:
                return respond("24 left. Your out:", "D12", 24)
            case 25:
                return respond("25 left. Your out:", "T7 D2", 25)
            case 26:
                return respond("26 left. Your out:", "D13", 26)
            case 27:
                return respond("27 left. Your out:", "Outer Bull D1", 27)
            case 28:
                return respond("28 left. Your out:", "D14", 28)
            case 29:
                return respond("29 left. Your out:", "T9 D1", 29)
            case 30:
                return respond("30 left. Your out:", "D15", 30)
            case 31:
                return respond("31 left. Your out:", "T9 D2", 31)
            case 32:
                return respond("32 left. Your out:", "D16", 32)
            case 33:
                return respond("33 left. Your out:", "T9 D3", 33)
            case 34:
                return respond("34 left. Your out:", "D17", 34)
            case 35:
                return respond("35 left. Your out:", "T11 D1", 35)
            case 36:
                return respond("36 left. Your out:", "D18", 36)
            case 37:
                return respond("37 left. Your out:", "T11 D2", 37)
            case 38:
                return respond("38 left. Your out:", "D19", 38)
            case 39:
                return respond("39 left. Your out:", "T11 D3", 39)
            case 40:
                return respond("40 left. Your out:", "D20", 40)
            case 41:
                return respond("41 left. Your out:", "T13 D1", 41)
            case 42:
                return respond("42 left. Your out:", "D20 D1", 42)
            case 43:
                return respond("43 left. Your out:", "T13 D2", 43)
            case 44:
                return respond("44 left. Your out:", "T14 D1", 44)
            case 45:
                return respond("45 left. Your out:", "T13 D3", 45)
            case 46:
                return respond("46 left. Your out:", "T14 D2", 46)
            case 47:
                return respond("47 left. Your out:", "T15 D1", 47)
            case 48:
                return respond("48 left. Your out:", "T14 D3", 48)
            case 49:
                return respond("49 left. Your out:", "T15 D2", 49)
            case 50:
                return respond("50 left. Your out:", "Bull", 50)
            case 51:
                return respond("51 left. Your out:", "T15 D3", 51)
            case 52:
                return respond("52 left. Your out:", "Bull D1", 52)
            case 53:
                return respond("53 left. Your out:", "T17 D1", 53)
            case 54:
                return respond("54 left. Your out:", "Bull D2", 54)
            case 55:
                return respond("55 left. Your out:", "T17 D2", 55)
            case 56:
                return respond("56 left. Your out:", "T18 D1", 56)
            case 57:
                return respond("57 left. Your out:", "T17 D3", 57)
            case 58:
                return respond("58 left. Your out:", "T18 D2", 58)
            case 59:
                return respond("59 left. Your out:", "T19 D1", 59)
            case 60:
                return respond("60 left. Your out:", "T18 D3", 60)
            case 61:
                return respond("61 left. Your out:", "T19 D2", 61)
            case 62:
                return respond("62 left. Your out:", "T20 D1", 62)
            case 63:
                return respond("63 left. Your out:", "T19 D3", 63)
            case 64:
                return respond("64 left. Your out:", "T20 D2", 64)
            case 65:
                return respond("65 left. Your out:", "T19 D4", 65)
            case 66:
                return respond("66 left. Your out:", "T20 D3", 66)
            case 67:
                return respond("67 left. Your out:", "T19 D5", 67)
            case 68:
                return respond("68 left. Your out:", "T20 D4", 68)
            case 69:
                return respond("69 left. Your out:", "T19 D6", 69)
            case 70:
                return respond("70 left. Your out:", "T20 D5", 70)
            case 71:
                return respond("71 left. Your out:", "T19 D7", 71)
            case 72:
                return respond("72 left. Your out:", "T20 D6", 72)
            case 73:
                return respond("73 left. Your out:", "T19 D8", 73)
            case 74:
                return respond("74 left. Your out:", "T20 D7", 74)
            case 75:
                return respond("75 left. Your out:", "T19 D9", 75)
            case 76:
                return respond("76 left. Your out:", "T20 D8", 76)
            case 77:
                return respond("77 left. Your out:", "T19 D10", 77)
            case 78:
                return respond("78 left. Your out:", "T20 D9", 78)
            case 79:
                return respond("79 left. Your out:", "T19 D11", 79)
            case 80:
                return respond("80 left. Your out:", "T20 D10", 80)
            case 81:
                return respond("81 left. Your out:", "T19 D12", 81)
            case 82:
                return respond("82 left. Your out:", "T20 D11", 82)
            case 83:
                return respond("83 left. Your out:", "T19 D13", 83)
            case 84:
                return respond("84 left. Your out:", "T20 D12", 84)
            case 85:
                return respond("85 left. Your out:", "T19 D14", 85)
            case 86:
                return respond("86 left. Your out:", "T20 D13", 86)
            case 87:
                return respond("87 left. Your out:", "T19 D15", 87)
            case 88:
                return respond("88 left. Your out:", "T20 D14", 88)
            case 89:
                return respond("89 left. Your out:", "T19 D16", 89)
            case 90:
                return respond("90 left. Your out:", "T20 D15", 90)
            case 91:
                return respond("91 left. Your out:", "T19 D17", 91)
            case 92:
                return respond("92 left. Your out:", "T20 D16", 92)
            case 93:
                return respond("93 left. Your out:", "T19 D18", 93)
            case 94:
                return respond("94 left. Your out:", "T20 D17", 94)
            case 95:
                return respond("95 left. Your out:", "T19 D19", 95)
            case 96:
                return respond("96 left. Your out:", "T20 D18", 96)
            case 97:
                return respond("97 left. Your out:", "T19 D20", 97)
            case 98:
                return respond("98 left. Your out:", "T20 D19", 98)
            case 99:
                return respond("99 left. Your out:", "T20 T11 D3", 99)
            case 100:
                return respond("100 left. Your out:", "T20 D20", 100)
            case 101:
                return respond("101 left. Your out:", "T17 Bull", 101)
            case 102:
                return respond("102 left. Your out:", "T20 D20 D1", 102)
            case 103:
                return respond("103 left. Your out:", "T20 T13 D2", 103)
            case 104:
                return respond("104 left. Your out:", "T18 Bull", 104)
            case 105:
                return respond("105 left. Your out:", "T20 T13 D3", 105)
            case 106:
                return respond("106 left. Your out:", "T20 T14 D2", 106)
            case 107:
                return respond("107 left. Your out:", "T19 Bull", 107)
            case 108:
                return respond("108 left. Your out:", "T20 T14 D3", 108)
            case 109:
                return respond("109 left. Your out:", "T20 T15 D2", 109)
            case 110:
                return respond("110 left. Your out:", "T20 Bull", 110)
            case 111:
                return respond("111 left. Your out:", "T20 T15 D3", 111)
            case 112:
                return respond("112 left. Your out:", "T20 Bull D1", 112)
            case 113:
                return respond("113 left. Your out:", "T20 T17 D1", 113)
            case 114:
                return respond("114 left. Your out:", "T20 Bull D2", 114)
            case 115:
                return respond("115 left. Your out:", "T20 T17 D2", 115)
            case 116:
                return respond("116 left. Your out:", "T20 T18 D1", 116)
            case 117:
                return respond("117 left. Your out:", "T20 T17 D3", 117)
            case 118:
                return respond("118 left. Your out:", "T20 T18 D2", 118)
            case 119:
                return respond("119 left. Your out:", "T20 T19 D1", 119)
            case 120:
                return respond("120 left. Your out:", "T20 T18 D3", 120)
            case 121:
                return respond("121 left. Your out:", "T20 T19 D2", 121)
            case 122:
                return respond("122 left. Your out:", "T20 T20 D1", 122)
            case 123:
                return respond("123 left. Your out:", "T20 T19 D3", 123)
            case 124:
                return respond("124 left. Your out:", "T20 T20 D2", 124)
            case 125:
                return respond("125 left. Your out:", "T20 T19 D4", 125)
            case 126:
                return respond("126 left. Your out:", "T20 T20 D3", 126)
            case 127:
                return respond("127 left. Your out:", "T20 T19 D5", 127)
            case 128:
                return respond("128 left. Your out:", "T20 T20 D4", 128)
            case 129:
                return respond("129 left. Your out:", "T20 T19 D6", 129)
            case 130:
                return respond("130 left. Your out:", "T20 T20 D5", 130)
            case 131:
                return respond("131 left. Your out:", "T20 T19 D7", 131)
            case 132:
                return respond("132 left. Your out:", "T20 T20 D6", 132)
            case 133:
                return respond("133 left. Your out:", "T20 T19 D8", 133)
            case 134:
                return respond("134 left. Your out:", "T20 T20 D7", 134)
            case 135:
                return respond("135 left. Your out:", "T20 T19 D9", 135)
            case 136:
                return respond("136 left. Your out:", "T20 T20 D8", 136)
            case 137:
                return respond("137 left. Your out:", "T20 T19 D10", 137)
            case 138:
                return respond("138 left. Your out:", "T20 T20 D9", 138)
            case 139:
                return respond("139 left. Your out:", "T20 T19 D11", 139)
            case 140:
                return respond("140 left. Your out:", "T20 T20 D10", 140)
            case 141:
                return respond("141 left. Your out:", "T20 T19 D12", 141)
            case 142:
                return respond("142 left. Your out:", "T20 T20 D11", 142)
            case 143:
                return respond("143 left. Your out:", "T20 T19 D13", 143)
            case 144:
                return respond("144 left. Your out:", "T20 T20 D12", 144)
            case 145:
                return respond("145 left. Your out:", "T20 T19 D14", 145)
            case 146:
                return respond("146 left. Your out:", "T20 T20 D13", 146)
            case 147:
                return respond("147 left. Your out:", "T20 T19 D15", 147)
            case 148:
                return respond("148 left. Your out:", "T20 T20 D14", 148)
            case 149:
                return respond("149 left. Your out:", "T20 T19 D16", 149)
            case 150:
                return respond("150 left. Your out:", "T20 T20 D15", 150)
            case 151:
                return respond("151 left. Your out:", "T20 T19 D17", 151)
            case 152:
                return respond("152 left. Your out:", "T20 T20 D16", 152)
            case 153:
                return respond("153 left. Your out:", "T20 T19 D18", 153)
            case 154:
                return respond("154 left. Your out:", "T20 T20 D17", 154)
            case 155:
                return respond("155 left. Your out:", "T20 T19 D19", 155)
            case 156:
                return respond("156 left. Your out:", "T20 T20 D18", 156)
            case 157:
                return respond("157 left. Your out:", "T20 T19 D20", 157)
            case 158:
                return respond("158 left. Your out:", "T20 T20 D19", 158)
            case 160:
                return respond("160 left. Your out:", "T20 T20 D20", 160)
            case 161:
                return respond("161 left. Your out:", "T20 T17 Bull", 161)
            case 164:
                return respond("164 left. Your out:", "T20 T18 Bull", 164)
            case 167:
                return respond("167 left. Your out:", "T20 T19 Bull", 167)
            case 170:
                return respond("170 left. Your out:", "T20 T20 Bull", 170)
            case 159 | 162 | 163 | 165 | 166 | 168 | 169:
                return respond(f"{start_num} has no 3-dart out (one of the 7 impossible numbers).", "", start_num)
            case n if n > 170:
                return respond("No out possible. 170 is the highest double out.", "", n)
            case n:
                return respond(f"{n} has no 3-dart double out.", "", n)
 
    return render_template("out.html")
 
 
# ======================= DOUBLE OUT =======================
 
@app.route("/first-dart-double", methods=["POST"])   # 2 darts left after this
def first_dart_double():
    global first_double_hit, left_over
    first_double_hit = int(request.form.get("hitDouble1"))
    left_over = start_num - first_double_hit
    match left_over:
        case 0:
            return respond("Checked out!", "", 0)
        case n if n < 0:
            return respond("Bust! You went over.", "", n)
        case 1:
            return respond("Bust! You can't be left on 1 in double out.", "", 1)
        case 2:
            return respond("2 left. Your out:", "D1", 2)
        case 3:
            return respond("3 left. Your out:", "S1 D1", 3)
        case 4:
            return respond("4 left. Your out:", "D2", 4)
        case 5:
            return respond("5 left. Your out:", "T1 D1", 5)
        case 6:
            return respond("6 left. Your out:", "D3", 6)
        case 7:
            return respond("7 left. Your out:", "S5 D1", 7)
        case 8:
            return respond("8 left. Your out:", "D4", 8)
        case 9:
            return respond("9 left. Your out:", "S7 D1", 9)
        case 10:
            return respond("10 left. Your out:", "D5", 10)
        case 11:
            return respond("11 left. Your out:", "T3 D1", 11)
        case 12:
            return respond("12 left. Your out:", "D6", 12)
        case 13:
            return respond("13 left. Your out:", "S11 D1", 13)
        case 14:
            return respond("14 left. Your out:", "D7", 14)
        case 15:
            return respond("15 left. Your out:", "S13 D1", 15)
        case 16:
            return respond("16 left. Your out:", "D8", 16)
        case 17:
            return respond("17 left. Your out:", "T5 D1", 17)
        case 18:
            return respond("18 left. Your out:", "D9", 18)
        case 19:
            return respond("19 left. Your out:", "S17 D1", 19)
        case 20:
            return respond("20 left. Your out:", "D10", 20)
        case 21:
            return respond("21 left. Your out:", "S19 D1", 21)
        case 22:
            return respond("22 left. Your out:", "D11", 22)
        case 23:
            return respond("23 left. Your out:", "T7 D1", 23)
        case 24:
            return respond("24 left. Your out:", "D12", 24)
        case 25:
            return respond("25 left. Your out:", "T7 D2", 25)
        case 26:
            return respond("26 left. Your out:", "D13", 26)
        case 27:
            return respond("27 left. Your out:", "Outer Bull D1", 27)
        case 28:
            return respond("28 left. Your out:", "D14", 28)
        case 29:
            return respond("29 left. Your out:", "T9 D1", 29)
        case 30:
            return respond("30 left. Your out:", "D15", 30)
        case 31:
            return respond("31 left. Your out:", "T9 D2", 31)
        case 32:
            return respond("32 left. Your out:", "D16", 32)
        case 33:
            return respond("33 left. Your out:", "T9 D3", 33)
        case 34:
            return respond("34 left. Your out:", "D17", 34)
        case 35:
            return respond("35 left. Your out:", "T11 D1", 35)
        case 36:
            return respond("36 left. Your out:", "D18", 36)
        case 37:
            return respond("37 left. Your out:", "T11 D2", 37)
        case 38:
            return respond("38 left. Your out:", "D19", 38)
        case 39:
            return respond("39 left. Your out:", "T11 D3", 39)
        case 40:
            return respond("40 left. Your out:", "D20", 40)
        case 41:
            return respond("41 left. Your out:", "T13 D1", 41)
        case 42:
            return respond("42 left. Your out:", "D20 D1", 42)
        case 43:
            return respond("43 left. Your out:", "T13 D2", 43)
        case 44:
            return respond("44 left. Your out:", "T14 D1", 44)
        case 45:
            return respond("45 left. Your out:", "T13 D3", 45)
        case 46:
            return respond("46 left. Your out:", "T14 D2", 46)
        case 47:
            return respond("47 left. Your out:", "T15 D1", 47)
        case 48:
            return respond("48 left. Your out:", "T14 D3", 48)
        case 49:
            return respond("49 left. Your out:", "T15 D2", 49)
        case 50:
            return respond("50 left. Your out:", "Bull", 50)
        case 51:
            return respond("51 left. Your out:", "T15 D3", 51)
        case 52:
            return respond("52 left. Your out:", "Bull D1", 52)
        case 53:
            return respond("53 left. Your out:", "T17 D1", 53)
        case 54:
            return respond("54 left. Your out:", "Bull D2", 54)
        case 55:
            return respond("55 left. Your out:", "T17 D2", 55)
        case 56:
            return respond("56 left. Your out:", "T18 D1", 56)
        case 57:
            return respond("57 left. Your out:", "T17 D3", 57)
        case 58:
            return respond("58 left. Your out:", "T18 D2", 58)
        case 59:
            return respond("59 left. Your out:", "T19 D1", 59)
        case 60:
            return respond("60 left. Your out:", "T18 D3", 60)
        case 61:
            return respond("61 left. Your out:", "T19 D2", 61)
        case 62:
            return respond("62 left. Your out:", "T20 D1", 62)
        case 63:
            return respond("63 left. Your out:", "T19 D3", 63)
        case 64:
            return respond("64 left. Your out:", "T20 D2", 64)
        case 65:
            return respond("65 left. Your out:", "T19 D4", 65)
        case 66:
            return respond("66 left. Your out:", "T20 D3", 66)
        case 67:
            return respond("67 left. Your out:", "T19 D5", 67)
        case 68:
            return respond("68 left. Your out:", "T20 D4", 68)
        case 69:
            return respond("69 left. Your out:", "T19 D6", 69)
        case 70:
            return respond("70 left. Your out:", "T20 D5", 70)
        case 71:
            return respond("71 left. Your out:", "T19 D7", 71)
        case 72:
            return respond("72 left. Your out:", "T20 D6", 72)
        case 73:
            return respond("73 left. Your out:", "T19 D8", 73)
        case 74:
            return respond("74 left. Your out:", "T20 D7", 74)
        case 75:
            return respond("75 left. Your out:", "T19 D9", 75)
        case 76:
            return respond("76 left. Your out:", "T20 D8", 76)
        case 77:
            return respond("77 left. Your out:", "T19 D10", 77)
        case 78:
            return respond("78 left. Your out:", "T20 D9", 78)
        case 79:
            return respond("79 left. Your out:", "T19 D11", 79)
        case 80:
            return respond("80 left. Your out:", "T20 D10", 80)
        case 81:
            return respond("81 left. Your out:", "T19 D12", 81)
        case 82:
            return respond("82 left. Your out:", "T20 D11", 82)
        case 83:
            return respond("83 left. Your out:", "T19 D13", 83)
        case 84:
            return respond("84 left. Your out:", "T20 D12", 84)
        case 85:
            return respond("85 left. Your out:", "T19 D14", 85)
        case 86:
            return respond("86 left. Your out:", "T20 D13", 86)
        case 87:
            return respond("87 left. Your out:", "T19 D15", 87)
        case 88:
            return respond("88 left. Your out:", "T20 D14", 88)
        case 89:
            return respond("89 left. Your out:", "T19 D16", 89)
        case 90:
            return respond("90 left. Your out:", "T20 D15", 90)
        case 91:
            return respond("91 left. Your out:", "T19 D17", 91)
        case 92:
            return respond("92 left. Your out:", "T20 D16", 92)
        case 93:
            return respond("93 left. Your out:", "T19 D18", 93)
        case 94:
            return respond("94 left. Your out:", "T20 D17", 94)
        case 95:
            return respond("95 left. Your out:", "T19 D19", 95)
        case 96:
            return respond("96 left. Your out:", "T20 D18", 96)
        case 97:
            return respond("97 left. Your out:", "T19 D20", 97)
        case 98:
            return respond("98 left. Your out:", "T20 D19", 98)
        case 100:
            return respond("100 left. Your out:", "T20 D20", 100)
        case 101:
            return respond("101 left. Your out:", "T17 Bull", 101)
        case 104:
            return respond("104 left. Your out:", "T18 Bull", 104)
        case 107:
            return respond("107 left. Your out:", "T19 Bull", 107)
        case 110:
            return respond("110 left. Your out:", "T20 Bull", 110)
        case n if n > 110:
            return respond(f"{n} left. Too high for 2 dart(s) (max is 110).", "", n)
        case n:
            return respond(f"{n} left. No 2-dart out, set up for the next dart.", "", n)
 
@app.route("/second-dart-double", methods=["POST"])   # 1 dart left after this
def second_dart_double():
    global second_double_hit
    second_double_hit = int(request.form.get("hitDouble2"))
    left_over = start_num - first_double_hit - second_double_hit
    match left_over:
        case 0:
            return respond("Checked out!", "", 0)
        case n if n < 0:
            return respond("Bust! You went over.", "", n)
        case 1:
            return respond("Bust! You can't be left on 1 in double out.", "", 1)
        case 2:
            return respond("2 left. Your out:", "D1", 2)
        case 4:
            return respond("4 left. Your out:", "D2", 4)
        case 6:
            return respond("6 left. Your out:", "D3", 6)
        case 8:
            return respond("8 left. Your out:", "D4", 8)
        case 10:
            return respond("10 left. Your out:", "D5", 10)
        case 12:
            return respond("12 left. Your out:", "D6", 12)
        case 14:
            return respond("14 left. Your out:", "D7", 14)
        case 16:
            return respond("16 left. Your out:", "D8", 16)
        case 18:
            return respond("18 left. Your out:", "D9", 18)
        case 20:
            return respond("20 left. Your out:", "D10", 20)
        case 22:
            return respond("22 left. Your out:", "D11", 22)
        case 24:
            return respond("24 left. Your out:", "D12", 24)
        case 26:
            return respond("26 left. Your out:", "D13", 26)
        case 28:
            return respond("28 left. Your out:", "D14", 28)
        case 30:
            return respond("30 left. Your out:", "D15", 30)
        case 32:
            return respond("32 left. Your out:", "D16", 32)
        case 34:
            return respond("34 left. Your out:", "D17", 34)
        case 36:
            return respond("36 left. Your out:", "D18", 36)
        case 38:
            return respond("38 left. Your out:", "D19", 38)
        case 40:
            return respond("40 left. Your out:", "D20", 40)
        case 50:
            return respond("50 left. Your out:", "Bull", 50)
        case n if n > 50:
            return respond(f"{n} left. Too high for 1 dart(s) (max is 50).", "", n)
        case n:
            return respond(f"{n} left. No 1-dart out, set up for the next dart.", "", n)
 
@app.route("/third-dart-double", methods=["POST"])   # no darts left
def third_dart_double():
    global third_double_hit
    third_double_hit = int(request.form.get("hitDouble3"))
    left_over = start_num - first_double_hit - second_double_hit - third_double_hit
    match left_over:
        case 0:
            return respond("Checked out!", "", 0)
        case 1:
            return respond("Bust! You can't be left on 1 in double out.", "", 1)
        case n if n < 0:
            return respond("Bust! Score doesn't count.", "", n)
        case n:
            return respond(f"Out of darts. You have {n} left.", "", n)
 
 
# ======================= STRAIGHT OUT =======================
 
@app.route("/first-dart-straight", methods=["POST"])   # 2 darts left after this
def first_dart_straight():
    global first_straight_hit, left_over
    first_straight_hit = int(request.form.get("hitStraight1"))
    left_over = start_num - first_straight_hit
    match left_over:
        case 0:
            return respond("Checked out!", "", 0)
        case n if n < 0:
            return respond("Bust! You went over.", "", n)
        case 1:
            return respond("1 left. Your out:", "S1", 1)
        case 2:
            return respond("2 left. Your out:", "D1", 2)
        case 3:
            return respond("3 left. Your out:", "T1", 3)
        case 4:
            return respond("4 left. Your out:", "D2", 4)
        case 5:
            return respond("5 left. Your out:", "S5", 5)
        case 6:
            return respond("6 left. Your out:", "T2", 6)
        case 7:
            return respond("7 left. Your out:", "S7", 7)
        case 8:
            return respond("8 left. Your out:", "D4", 8)
        case 9:
            return respond("9 left. Your out:", "T3", 9)
        case 10:
            return respond("10 left. Your out:", "D5", 10)
        case 11:
            return respond("11 left. Your out:", "S11", 11)
        case 12:
            return respond("12 left. Your out:", "T4", 12)
        case 13:
            return respond("13 left. Your out:", "S13", 13)
        case 14:
            return respond("14 left. Your out:", "D7", 14)
        case 15:
            return respond("15 left. Your out:", "T5", 15)
        case 16:
            return respond("16 left. Your out:", "D8", 16)
        case 17:
            return respond("17 left. Your out:", "S17", 17)
        case 18:
            return respond("18 left. Your out:", "T6", 18)
        case 19:
            return respond("19 left. Your out:", "S19", 19)
        case 20:
            return respond("20 left. Your out:", "D10", 20)
        case 21:
            return respond("21 left. Your out:", "T7", 21)
        case 22:
            return respond("22 left. Your out:", "D11", 22)
        case 23:
            return respond("23 left. Your out:", "D11 S1", 23)
        case 24:
            return respond("24 left. Your out:", "T8", 24)
        case 25:
            return respond("25 left. Your out:", "Outer Bull", 25)
        case 26:
            return respond("26 left. Your out:", "D13", 26)
        case 27:
            return respond("27 left. Your out:", "T9", 27)
        case 28:
            return respond("28 left. Your out:", "D14", 28)
        case 29:
            return respond("29 left. Your out:", "D14 S1", 29)
        case 30:
            return respond("30 left. Your out:", "T10", 30)
        case 31:
            return respond("31 left. Your out:", "T10 S1", 31)
        case 32:
            return respond("32 left. Your out:", "D16", 32)
        case 33:
            return respond("33 left. Your out:", "T11", 33)
        case 34:
            return respond("34 left. Your out:", "D17", 34)
        case 35:
            return respond("35 left. Your out:", "D17 S1", 35)
        case 36:
            return respond("36 left. Your out:", "T12", 36)
        case 37:
            return respond("37 left. Your out:", "T12 S1", 37)
        case 38:
            return respond("38 left. Your out:", "D19", 38)
        case 39:
            return respond("39 left. Your out:", "T13", 39)
        case 40:
            return respond("40 left. Your out:", "D20", 40)
        case 41:
            return respond("41 left. Your out:", "D20 S1", 41)
        case 42:
            return respond("42 left. Your out:", "T14", 42)
        case 43:
            return respond("43 left. Your out:", "T14 S1", 43)
        case 44:
            return respond("44 left. Your out:", "T14 D1", 44)
        case 45:
            return respond("45 left. Your out:", "T15", 45)
        case 46:
            return respond("46 left. Your out:", "T15 S1", 46)
        case 47:
            return respond("47 left. Your out:", "T15 D1", 47)
        case 48:
            return respond("48 left. Your out:", "T16", 48)
        case 49:
            return respond("49 left. Your out:", "T16 S1", 49)
        case 50:
            return respond("50 left. Your out:", "Bull", 50)
        case 51:
            return respond("51 left. Your out:", "T17", 51)
        case 52:
            return respond("52 left. Your out:", "T17 S1", 52)
        case 53:
            return respond("53 left. Your out:", "T17 D1", 53)
        case 54:
            return respond("54 left. Your out:", "T18", 54)
        case 55:
            return respond("55 left. Your out:", "T18 S1", 55)
        case 56:
            return respond("56 left. Your out:", "T18 D1", 56)
        case 57:
            return respond("57 left. Your out:", "T19", 57)
        case 58:
            return respond("58 left. Your out:", "T19 S1", 58)
        case 59:
            return respond("59 left. Your out:", "T19 D1", 59)
        case 60:
            return respond("60 left. Your out:", "T20", 60)
        case 61:
            return respond("61 left. Your out:", "T20 S1", 61)
        case 62:
            return respond("62 left. Your out:", "T20 D1", 62)
        case 63:
            return respond("63 left. Your out:", "T20 T1", 63)
        case 64:
            return respond("64 left. Your out:", "T20 D2", 64)
        case 65:
            return respond("65 left. Your out:", "T20 S5", 65)
        case 66:
            return respond("66 left. Your out:", "T20 T2", 66)
        case 67:
            return respond("67 left. Your out:", "T20 S7", 67)
        case 68:
            return respond("68 left. Your out:", "T20 D4", 68)
        case 69:
            return respond("69 left. Your out:", "T20 T3", 69)
        case 70:
            return respond("70 left. Your out:", "T20 D5", 70)
        case 71:
            return respond("71 left. Your out:", "T20 S11", 71)
        case 72:
            return respond("72 left. Your out:", "T20 T4", 72)
        case 73:
            return respond("73 left. Your out:", "T20 S13", 73)
        case 74:
            return respond("74 left. Your out:", "T20 D7", 74)
        case 75:
            return respond("75 left. Your out:", "T20 T5", 75)
        case 76:
            return respond("76 left. Your out:", "T20 D8", 76)
        case 77:
            return respond("77 left. Your out:", "T20 S17", 77)
        case 78:
            return respond("78 left. Your out:", "T20 T6", 78)
        case 79:
            return respond("79 left. Your out:", "T20 S19", 79)
        case 80:
            return respond("80 left. Your out:", "T20 D10", 80)
        case 81:
            return respond("81 left. Your out:", "T20 T7", 81)
        case 82:
            return respond("82 left. Your out:", "T20 D11", 82)
        case 83:
            return respond("83 left. Your out:", "T19 D13", 83)
        case 84:
            return respond("84 left. Your out:", "T20 T8", 84)
        case 85:
            return respond("85 left. Your out:", "T20 Outer Bull", 85)
        case 86:
            return respond("86 left. Your out:", "T20 D13", 86)
        case 87:
            return respond("87 left. Your out:", "T20 T9", 87)
        case 88:
            return respond("88 left. Your out:", "T20 D14", 88)
        case 89:
            return respond("89 left. Your out:", "T19 D16", 89)
        case 90:
            return respond("90 left. Your out:", "T20 T10", 90)
        case 91:
            return respond("91 left. Your out:", "T19 D17", 91)
        case 92:
            return respond("92 left. Your out:", "T20 D16", 92)
        case 93:
            return respond("93 left. Your out:", "T20 T11", 93)
        case 94:
            return respond("94 left. Your out:", "T20 D17", 94)
        case 95:
            return respond("95 left. Your out:", "T19 D19", 95)
        case 96:
            return respond("96 left. Your out:", "T20 T12", 96)
        case 97:
            return respond("97 left. Your out:", "T19 D20", 97)
        case 98:
            return respond("98 left. Your out:", "T20 D19", 98)
        case 99:
            return respond("99 left. Your out:", "T20 T13", 99)
        case 100:
            return respond("100 left. Your out:", "T20 D20", 100)
        case 101:
            return respond("101 left. Your out:", "T17 Bull", 101)
        case 102:
            return respond("102 left. Your out:", "T20 T14", 102)
        case 104:
            return respond("104 left. Your out:", "T18 Bull", 104)
        case 105:
            return respond("105 left. Your out:", "T20 T15", 105)
        case 107:
            return respond("107 left. Your out:", "T19 Bull", 107)
        case 108:
            return respond("108 left. Your out:", "T20 T16", 108)
        case 110:
            return respond("110 left. Your out:", "T20 Bull", 110)
        case 111:
            return respond("111 left. Your out:", "T20 T17", 111)
        case 114:
            return respond("114 left. Your out:", "T20 T18", 114)
        case 117:
            return respond("117 left. Your out:", "T20 T19", 117)
        case 120:
            return respond("120 left. Your out:", "T20 T20", 120)
        case n if n > 120:
            return respond(f"{n} left. Too high for 2 dart(s) (max is 120).", "", n)
        case n:
            return respond(f"{n} left. No 2-dart out, set up for the next dart.", "", n)
 
@app.route("/second-dart-straight", methods=["POST"])   # 1 dart left after this
def second_dart_straight():
    global second_straight_hit
    second_straight_hit = int(request.form.get("hitStraight2"))
    left_over = start_num - first_straight_hit - second_straight_hit
    match left_over:
        case 0:
            return respond("Checked out!", "", 0)
        case n if n < 0:
            return respond("Bust! You went over.", "", n)
        case 1:
            return respond("1 left. Your out:", "S1", 1)
        case 2:
            return respond("2 left. Your out:", "D1", 2)
        case 3:
            return respond("3 left. Your out:", "T1", 3)
        case 4:
            return respond("4 left. Your out:", "D2", 4)
        case 5:
            return respond("5 left. Your out:", "S5", 5)
        case 6:
            return respond("6 left. Your out:", "T2", 6)
        case 7:
            return respond("7 left. Your out:", "S7", 7)
        case 8:
            return respond("8 left. Your out:", "D4", 8)
        case 9:
            return respond("9 left. Your out:", "T3", 9)
        case 10:
            return respond("10 left. Your out:", "D5", 10)
        case 11:
            return respond("11 left. Your out:", "S11", 11)
        case 12:
            return respond("12 left. Your out:", "T4", 12)
        case 13:
            return respond("13 left. Your out:", "S13", 13)
        case 14:
            return respond("14 left. Your out:", "D7", 14)
        case 15:
            return respond("15 left. Your out:", "T5", 15)
        case 16:
            return respond("16 left. Your out:", "D8", 16)
        case 17:
            return respond("17 left. Your out:", "S17", 17)
        case 18:
            return respond("18 left. Your out:", "T6", 18)
        case 19:
            return respond("19 left. Your out:", "S19", 19)
        case 20:
            return respond("20 left. Your out:", "D10", 20)
        case 21:
            return respond("21 left. Your out:", "T7", 21)
        case 22:
            return respond("22 left. Your out:", "D11", 22)
        case 24:
            return respond("24 left. Your out:", "T8", 24)
        case 25:
            return respond("25 left. Your out:", "Outer Bull", 25)
        case 26:
            return respond("26 left. Your out:", "D13", 26)
        case 27:
            return respond("27 left. Your out:", "T9", 27)
        case 28:
            return respond("28 left. Your out:", "D14", 28)
        case 30:
            return respond("30 left. Your out:", "T10", 30)
        case 32:
            return respond("32 left. Your out:", "D16", 32)
        case 33:
            return respond("33 left. Your out:", "T11", 33)
        case 34:
            return respond("34 left. Your out:", "D17", 34)
        case 36:
            return respond("36 left. Your out:", "T12", 36)
        case 38:
            return respond("38 left. Your out:", "D19", 38)
        case 39:
            return respond("39 left. Your out:", "T13", 39)
        case 40:
            return respond("40 left. Your out:", "D20", 40)
        case 42:
            return respond("42 left. Your out:", "T14", 42)
        case 45:
            return respond("45 left. Your out:", "T15", 45)
        case 48:
            return respond("48 left. Your out:", "T16", 48)
        case 50:
            return respond("50 left. Your out:", "Bull", 50)
        case 51:
            return respond("51 left. Your out:", "T17", 51)
        case 54:
            return respond("54 left. Your out:", "T18", 54)
        case 57:
            return respond("57 left. Your out:", "T19", 57)
        case 60:
            return respond("60 left. Your out:", "T20", 60)
        case n if n > 60:
            return respond(f"{n} left. Too high for 1 dart(s) (max is 60).", "", n)
        case n:
            return respond(f"{n} left. No 1-dart out, set up for the next dart.", "", n)
 
@app.route("/third-dart-straight", methods=["POST"])   # no darts left
def third_dart_straight():
    global third_straight_hit
    third_straight_hit = int(request.form.get("hitStraight3"))
    left_over = start_num - first_straight_hit - second_straight_hit - third_straight_hit
    match left_over:
        case 0:
            return respond("Checked out!", "", 0)
        case n if n < 0:
            return respond("Bust! Score doesn't count.", "", n)
        case n:
            return respond(f"Out of darts. You have {n} left.", "", n)
