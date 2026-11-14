from flask import Flask, request, jsonify, render_template, session
from datetime import datetime, timedelta
def render_checkout(score, routes):
    # Make sure there are always three route options.
    routes = routes or ("", "", "")
    route_one, route_two, route_three = routes

    # Use the first route for the original route variable too.
    route = route_one

    # Set the message based on the remaining score.
    if score == 0:
        message = "Checked out!"

    elif score < 0:
        message = "Bust! Score doesn't count."

    elif score == 1 and session.get("out_type") == "double":
        message = "Bust! You can't be left on 1 in double out."

    elif route_one or route_two or route_three:
        message = f"{score} left. Your out:"

    else:
        message = f"{score} left. No checkout route available."

    # Send the checkout information to the HTML page.
    return render_template(
        "out.html",
        message=message,
        route=route,
        route_one=route_one,
        route_two=route_two,
        route_three=route_three,
        left_over=score
    )
app = Flask(__name__)
app.secret_key = "replace-this-with-a-long-random-secret"
app.config["DEBUG"] = True

# Variables
out_path_one = []
out_path_two = []
out_path_three = []


@app.route('/', methods=['GET'])
def index():
    return render_template('dashboard.html')


@app.route('/outs-page', methods=['GET'])
def outs_page():
    return render_template('out.html', route="", route_one="", route_two="", route_three="", left_over="")


@app.route('/statistics-page', methods=['GET'])
def statistics_page():
    return render_template('statistics.html')


@app.route("/out-type", methods=["POST"])
def select_out_type():
    chosen = request.form.get("out_type")

    if chosen == "straight":
        session.clear()
        session["out_type"] = "straight"
    elif chosen == "double":
        session.clear()
        session["out_type"] = "double"

    return render_template('out.html', route="", route_one="", route_two="", route_three="", left_over="")


STRAIGHT_START_OUTS={
    1:("S1","",""),
    2:("D1","",""),
    3:("T1","S1 S1 S1",""),
    4:("D2","D1 S1 S1","S2 S1 S1"),
    5:("S5","S3 S1 S1","T1 S1 S1"),
    6:("T2","D2 S1 S1","S4 S1 S1"),
    7:("S7","S5 S1 S1","D2 D1 S1"),
    8:("D4","D3 S1 S1","S6 S1 S1"),
    9:("T3","S7 S1 S1","D3 D1 S1"),
    10:("D5","D4 S1 S1","S8 S1 S1"),
    11:("S11","S9 S1 S1","T3 S1 S1"),
    12:("T4","D5 S1 S1","S10 S1 S1"),
    13:("S13","S11 S1 S1","D5 D1 S1"),
    14:("D7","D6 S1 S1","S12 S1 S1"),
    15:("T5","S13 S1 S1","D6 D1 S1"),
    16:("D8","D7 S1 S1","S14 S1 S1"),
    17:("S17","S15 S1 S1","T5 S1 S1"),
    18:("T6","D8 S1 S1","S16 S1 S1"),
    19:("S19","S17 S1 S1","D8 D1 S1"),
    20:("D10","D9 S1 S1","S18 S1 S1"),
    21:("T7","S19 S1 S1","D9 D1 S1"),
    22:("D11","D10 S1 S1","S20 S1 S1"),
    23:("D11 S1","T7 S1 S1","D10 D1 S1"),
    24:("T8","D11 S1 S1","T7 D1 S1"),
    25:("Outer Bull","D11 D1 S1","D11 S2 S1"),
    26:("D13","D12 S1 S1","T8 S1 S1"),
    27:("T9","Outer Bull S1 S1","D12 D1 S1"),
    28:("D14","D13 S1 S1","Outer Bull D1 S1"),
    29:("D14 S1","T9 S1 S1","D13 D1 S1"),
    30:("T10","D14 S1 S1","T9 D1 S1"),
    31:("T10 S1","D14 D1 S1","D14 S2 S1"),
    32:("D16","D15 S1 S1","T10 S1 S1"),
    33:("T11","D15 D1 S1","D15 S2 S1"),
    34:("D17","D16 S1 S1","D15 S3 S1"),
    35:("D17 S1","T11 S1 S1","D16 D1 S1"),
    36:("T12","D17 S1 S1","T11 D1 S1"),
    37:("T12 S1","D17 D1 S1","D17 S2 S1"),
    38:("D19","D18 S1 S1","T12 S1 S1"),
    39:("T13","D18 D1 S1","D18 S2 S1"),
    40:("D20","D19 S1 S1","D18 S3 S1"),
    41:("D20 S1","T13 S1 S1","D19 D1 S1"),
    42:("T14","D20 S1 S1","T13 D1 S1"),
    43:("T14 S1","D20 D1 S1","D20 S2 S1"),
    44:("T14 D1","T14 S1 S1","D20 S3 S1"),
    45:("T15","T14 D1 S1","T14 S2 S1"),
    46:("T15 S1","T14 S3 S1","T14 T1 S1"),
    47:("T15 D1","T15 S1 S1","T14 D2 S1"),
    48:("T16","T15 D1 S1","T15 S2 S1"),
    49:("T16 S1","T15 S3 S1","T15 T1 S1"),
    50:("Bull","T16 S1 S1","T15 D2 S1"),
    51:("T17","T16 D1 S1","T16 S2 S1"),
    52:("T17 S1","Bull S1 S1","T16 S3 S1"),
    53:("T17 D1","T17 S1 S1","Bull D1 S1"),
    54:("T18","T17 D1 S1","T17 S2 S1"),
    55:("T18 S1","T17 S3 S1","T17 T1 S1"),
    56:("T18 D1","T18 S1 S1","T17 D2 S1"),
    57:("T19","T18 D1 S1","T18 S2 S1"),
    58:("T19 S1","T18 S3 S1","T18 T1 S1"),
    59:("T19 D1","T19 S1 S1","T18 D2 S1"),
    60:("T20","T19 D1 S1","T19 S2 S1"),
    61:("T20 S1","T19 S3 S1","T19 T1 S1"),
    62:("T20 D1","T20 S1 S1","T19 D2 S1"),
    63:("T20 T1","T20 D1 S1","T20 S2 S1"),
    64:("T20 D2","T20 S3 S1","T20 T1 S1"),
    65:("T20 S5","T20 D2 S1","T20 S4 S1"),
    66:("T20 T2","T20 S5 S1","T20 D2 D1"),
    67:("T20 S7","T20 D3 S1","T20 S6 S1"),
    68:("T20 D4","T20 S7 S1","T20 D3 D1"),
    69:("T20 T3","T20 D4 S1","T20 S8 S1"),
    70:("T20 D5","T20 S9 S1","T20 T3 S1"),
    71:("T20 S11","T20 D5 S1","T20 S10 S1"),
    72:("T20 T4","T20 S11 S1","T20 D5 D1"),
    73:("T20 S13","T20 D6 S1","T20 S12 S1"),
    74:("T20 D7","T20 S13 S1","T20 D6 D1"),
    75:("T20 T5","T20 D7 S1","T20 S14 S1"),
    76:("T20 D8","T20 S15 S1","T20 T5 S1"),
    77:("T20 S17","T20 D8 S1","T20 S16 S1"),
    78:("T20 T6","T20 S17 S1","T20 D8 D1"),
    79:("T20 S19","T20 D9 S1","T20 S18 S1"),
    80:("T20 D10","T20 S19 S1","T20 D9 D1"),
    81:("T20 T7","T20 D10 S1","T20 S20 S1"),
    82:("T20 D11","T20 T7 S1","T20 D10 D1"),
    83:("T19 D13","T20 D11 S1","T20 T7 D1"),
    84:("T20 T8","T20 D11 D1","T20 D11 S2"),
    85:("T20 Outer Bull","T20 D12 S1","T20 T8 S1"),
    86:("T20 D13","T20 Outer Bull S1","T20 D12 D1"),
    87:("T20 T9","T20 D13 S1","T20 Outer Bull D1"),
    88:("T20 D14","T20 T9 S1","T20 D13 D1"),
    89:("T19 D16","T20 D14 S1","T20 T9 D1"),
    90:("T20 T10","T20 D14 D1","T20 D14 S2"),
    91:("T19 D17","T20 D15 S1","T20 T10 S1"),
    92:("T20 D16","T20 D15 D1","T20 D15 S2"),
    93:("T20 T11","T20 D16 S1","T20 D15 S3"),
    94:("T20 D17","T20 T11 S1","T20 D16 D1"),
    95:("T19 D19","T20 D17 S1","T20 T11 D1"),
    96:("T20 T12","T20 D17 D1","T20 D17 S2"),
    97:("T19 D20","T20 D18 S1","T20 T12 S1"),
    98:("T20 D19","T20 D18 D1","T20 D18 S2"),
    99:("T20 T13","T20 D19 S1","T20 D18 S3"),
    100:("T20 D20","T20 T13 S1","T20 D19 D1"),
    101:("T17 Bull","T20 D20 S1","T20 T13 D1"),
    102:("T20 T14","T20 D20 D1","T20 D20 S2"),
    103:("T20 T14 S1","T20 D20 S3","T20 D20 T1"),
    104:("T18 Bull","T20 T14 D1","T20 T14 S2"),
    105:("T20 T15","T20 T14 S3","T20 T14 T1"),
    106:("T20 T15 S1","T20 T14 D2","T20 T14 S4"),
    107:("T19 Bull","T20 T15 D1","T20 T15 S2"),
    108:("T20 T16","T20 T15 S3","T20 T15 T1"),
    109:("T20 T16 S1","T20 T15 D2","T20 T15 S4"),
    110:("T20 Bull","T20 T16 D1","T20 T16 S2"),
    111:("T20 T17","T20 Bull S1","T20 T16 S3"),
    112:("T20 T17 S1","T20 Bull D1","T20 Bull S2"),
    113:("T20 T17 D1","T20 T17 S2","T20 Bull S3"),
    114:("T20 T18","T20 T17 S3","T20 T17 T1"),
    115:("T20 T18 S1","T20 T17 D2","T20 T17 S4"),
    116:("T20 T18 D1","T20 T18 S2","T20 T17 S5"),
    117:("T20 T19","T20 T18 S3","T20 T18 T1"),
    118:("T20 T19 S1","T20 T18 D2","T20 T18 S4"),
    119:("T20 T19 D1","T20 T19 S2","T20 T18 S5"),
    120:("T20 T20","T20 T19 S3","T20 T19 T1"),
    121:("T20 T20 S1","T20 T19 D2","T20 T19 S4"),
    122:("T20 T20 D1","T20 T20 S2","T20 T19 S5"),
    123:("T20 T20 T1","T20 T20 S3","T20 T19 D3"),
    124:("T20 T20 D2","T20 T20 S4","T20 T19 S7"),
    125:("T20 T20 S5","T20 T19 D4","T20 T19 S8"),
    126:("T20 T20 T2","T20 T20 D3","T20 T20 S6"),
    127:("T20 T20 S7","T20 T19 D5","T20 T19 S10"),
    128:("T20 T20 D4","T20 T20 S8","T20 T19 S11"),
    129:("T20 T20 T3","T20 T20 S9","T20 T19 D6"),
    130:("T20 T20 D5","T20 T20 S10","T20 T19 S13"),
    131:("T20 T20 S11","T20 T19 D7","T20 T19 S14"),
    132:("T20 T20 T4","T20 T20 D6","T20 T20 S12"),
    133:("T20 T20 S13","T20 T19 D8","T20 T19 S16"),
    134:("T20 T20 D7","T20 T20 S14","T20 T19 S17"),
    135:("T20 T20 T5","T20 T20 S15","T20 T19 D9"),
    136:("T20 T20 D8","T20 T20 S16","T20 T19 S19"),
    137:("T20 T20 S17","T20 T19 D10","T20 T19 S20"),
    138:("T20 T20 T6","T20 T20 D9","T20 T20 S18"),
    139:("T20 T20 S19","T20 T19 D11","T20 T18 Outer Bull"),
    140:("T20 T20 D10","T20 T20 S20","T20 T18 D13"),
    141:("T20 T20 T7","T20 T19 D12","T20 T19 T8"),
    142:("T20 T20 D11","T20 T19 Outer Bull","T20 T18 D14"),
    143:("T20 T19 D13","T20 T17 D16","T20 Bull T11"),
    144:("T20 T20 T8","T20 T20 D12","T20 T19 T9"),
    145:("T20 T20 Outer Bull","T20 T19 D14","T20 T17 D17"),
    146:("T20 T20 D13","T20 T18 D16","T20 Bull D18"),
    147:("T20 T20 T9","T20 T19 D15","T20 T19 T10"),
    148:("T20 T20 D14","T20 T18 D17","T20 Bull D19"),
    149:("T20 T19 D16","T20 T17 D19","T20 Bull T13"),
    150:("T20 T20 T10","T20 T20 D15","T20 T19 T11"),
    151:("T20 T19 D17","T20 T17 D20","T20 D20 T17"),
    152:("T20 T20 D16","T20 T18 D19","T20 Bull T14"),
    153:("T20 T20 T11","T20 T19 D18","T20 T19 T12"),
    154:("T20 T20 D17","T20 T18 D20","T20 D20 T18"),
    155:("T20 T19 D19","T20 Bull T15","T20 T15 Bull"),
    156:("T20 T20 T12","T20 T20 D18","T20 T19 T13"),
    157:("T20 T19 D20","T20 D20 T19","T19 T20 D20"),
    158:("T20 T20 D19","T20 Bull T16","T20 T16 Bull"),
    159:("T20 T20 T13","T20 T19 T14","T20 T18 T15"),
    160:("T20 T20 D20","T20 Bull Bull","T20 D20 T20"),
    161:("T20 T17 Bull","T20 Bull T17","T19 T18 Bull"),
    162:("T20 T20 T14","T20 T19 T15","T20 T18 T16"),
    164:("T20 T18 Bull","T20 Bull T18","T19 T19 Bull"),
    165:("T20 T20 T15","T20 T19 T16","T20 T18 T17"),
    167:("T20 T19 Bull","T20 Bull T19","T19 T20 Bull"),
    168:("T20 T20 T16","T20 T19 T17","T20 T18 T18"),
    170:("T20 T20 Bull","T20 Bull T20","Bull T20 T20"),
    171:("T20 T20 T17","T20 T19 T18","T20 T18 T19"),
    174:("T20 T20 T18","T20 T19 T19","T20 T18 T20"),
    177:("T20 T20 T19","T20 T19 T20","T19 T20 T20"),
    180:("T20 T20 T20","",""),
}

DOUBLE_START_OUTS={
    2:("D1","",""),
    3:("S1 D1","",""),
    4:("D2","S1 S1 D1",""),
    5:("T1 D1","D1 S1 D1","S2 S1 D1"),
    6:("D3","S3 S1 D1","T1 S1 D1"),
    7:("S5 D1","D2 S1 D1","S4 S1 D1"),
    8:("D4","S5 S1 D1","D2 D1 D1"),
    9:("S7 D1","D3 S1 D1","S6 S1 D1"),
    10:("D5","S7 S1 D1","D3 D1 D1"),
    11:("T3 D1","D4 S1 D1","S8 S1 D1"),
    12:("D6","S9 S1 D1","T3 S1 D1"),
    13:("S11 D1","D5 S1 D1","S10 S1 D1"),
    14:("D7","S11 S1 D1","D5 D1 D1"),
    15:("S13 D1","D6 S1 D1","S12 S1 D1"),
    16:("D8","S13 S1 D1","D6 D1 D1"),
    17:("T5 D1","D7 S1 D1","S14 S1 D1"),
    18:("D9","S15 S1 D1","T5 S1 D1"),
    19:("S17 D1","D8 S1 D1","S16 S1 D1"),
    20:("D10","S17 S1 D1","D8 D1 D1"),
    21:("S19 D1","D9 S1 D1","S18 S1 D1"),
    22:("D11","S19 S1 D1","D9 D1 D1"),
    23:("T7 D1","D10 S1 D1","S20 S1 D1"),
    24:("D12","T7 S1 D1","D10 D1 D1"),
    25:("T7 D2","D11 S1 D1","T7 D1 D1"),
    26:("D13","D11 D1 D1","D11 S2 D1"),
    27:("Outer Bull D1","D12 S1 D1","T8 S1 D1"),
    28:("D14","Outer Bull S1 D1","D12 D1 D1"),
    29:("T9 D1","D13 S1 D1","Outer Bull D1 D1"),
    30:("D15","T9 S1 D1","D13 D1 D1"),
    31:("T9 D2","D14 S1 D1","T9 D1 D1"),
    32:("D16","D14 D1 D1","D14 S2 D1"),
    33:("T9 D3","D15 S1 D1","T10 S1 D1"),
    34:("D17","D15 D1 D1","D15 S2 D1"),
    35:("T11 D1","D16 S1 D1","D15 S3 D1"),
    36:("D18","T11 S1 D1","D16 D1 D1"),
    37:("T11 D2","D17 S1 D1","T11 D1 D1"),
    38:("D19","D17 D1 D1","D17 S2 D1"),
    39:("T11 D3","D18 S1 D1","T12 S1 D1"),
    40:("D20","D18 D1 D1","D18 S2 D1"),
    41:("T13 D1","D19 S1 D1","D18 S3 D1"),
    42:("D20 D1","T13 S1 D1","D19 D1 D1"),
    43:("T13 D2","D20 S1 D1","T13 D1 D1"),
    44:("T14 D1","D20 D1 D1","D20 S2 D1"),
    45:("T13 D3","T14 S1 D1","D20 S3 D1"),
    46:("T14 D2","T14 D1 D1","T14 S2 D1"),
    47:("T15 D1","T14 S3 D1","T14 T1 D1"),
    48:("T14 D3","T15 S1 D1","T14 D2 D1"),
    49:("T15 D2","T15 D1 D1","T15 S2 D1"),
    50:("Bull","T15 S3 D1","T15 T1 D1"),
    51:("T15 D3","T16 S1 D1","T15 D2 D1"),
    52:("Bull D1","T16 D1 D1","T16 S2 D1"),
    53:("T17 D1","Bull S1 D1","T16 S3 D1"),
    54:("Bull D2","T17 S1 D1","Bull D1 D1"),
    55:("T17 D2","T17 D1 D1","T17 S2 D1"),
    56:("T18 D1","T17 S3 D1","T17 T1 D1"),
    57:("T17 D3","T18 S1 D1","T17 D2 D1"),
    58:("T18 D2","T18 D1 D1","T18 S2 D1"),
    59:("T19 D1","T18 S3 D1","T18 T1 D1"),
    60:("T18 D3","T19 S1 D1","T18 D2 D1"),
    61:("T19 D2","T19 D1 D1","T19 S2 D1"),
    62:("T20 D1","T19 S3 D1","T19 T1 D1"),
    63:("T19 D3","T20 S1 D1","T19 D2 D1"),
    64:("T20 D2","T20 D1 D1","T20 S2 D1"),
    65:("T19 D4","T20 S3 D1","T20 T1 D1"),
    66:("T20 D3","T20 D2 D1","T20 S4 D1"),
    67:("T19 D5","T20 S5 D1","T20 S3 D2"),
    68:("T20 D4","T20 D3 D1","T20 S6 D1"),
    69:("T19 D6","T20 S7 D1","T20 S5 D2"),
    70:("T20 D5","T20 D4 D1","T20 S8 D1"),
    71:("T19 D7","T20 S9 D1","T20 T3 D1"),
    72:("T20 D6","T20 D5 D1","T20 S10 D1"),
    73:("T19 D8","T20 S11 D1","T20 S9 D2"),
    74:("T20 D7","T20 D6 D1","T20 S12 D1"),
        75:("T19 D9","T20 S13 D1","T20 S11 D2"),
    76:("T20 D8","T20 D7 D1","T20 S14 D1"),
    77:("T19 D10","T20 S15 D1","T20 T5 D1"),
    78:("T20 D9","T20 D8 D1","T20 S16 D1"),
    79:("T19 D11","T20 S17 D1","T20 S15 D2"),
    80:("T20 D10","T20 D9 D1","T20 S18 D1"),
    81:("T19 D12","T20 S19 D1","T20 S17 D2"),
    82:("T20 D11","T20 D10 D1","T20 S20 D1"),
    83:("T19 D13","T20 T7 D1","T20 S19 D2"),
    84:("T20 D12","T20 D11 D1","T20 D10 D2"),
    85:("T19 D14","T20 T7 D2","T20 S19 D3"),
    86:("T20 D13","T20 D12 D1","T20 T8 D1"),
    87:("T19 D15","T20 Outer Bull D1","T20 T7 D3"),
    88:("T20 D14","T20 D13 D1","T20 D12 D2"),
    89:("T19 D16","T20 T9 D1","T20 Outer Bull D2"),
    90:("T20 D15","T20 D14 D1","T20 D13 D2"),
    91:("T19 D17","T20 T9 D2","T20 Outer Bull D3"),
    92:("T20 D16","T20 D15 D1","T20 T10 D1"),
    93:("T19 D18","T20 T9 D3","T20 Outer Bull D4"),
    94:("T20 D17","T20 D16 D1","T20 D15 D2"),
    95:("T19 D19","T20 T11 D1","T20 T9 D4"),
    96:("T20 D18","T20 D17 D1","T20 D16 D2"),
    97:("T19 D20","T20 T11 D2","T20 T9 D5"),
    98:("T20 D19","T20 D18 D1","T20 T12 D1"),
    99:("T20 T11 D3","T20 T9 D6","T20 Outer Bull D7"),
    100:("T20 D20","T20 D19 D1","T20 D18 D2"),
    101:("T17 Bull","T20 T13 D1","T20 T11 D4"),
    102:("T20 D20 D1","T20 D19 D2","T20 D18 D3"),
    103:("T20 T13 D2","T20 T11 D5","T20 T9 D8"),
    104:("T18 Bull","T20 T14 D1","T20 D20 D2"),
    105:("T20 T13 D3","T20 T11 D6","T20 T9 D9"),
    106:("T20 T14 D2","T20 D20 D3","T20 D19 D4"),
    107:("T19 Bull","T20 T15 D1","T20 T13 D4"),
    108:("T20 T14 D3","T20 D20 D4","T20 D19 D5"),
    109:("T20 T15 D2","T20 T13 D5","T20 T11 D8"),
    110:("T20 Bull","T20 T16 D1","T20 T14 D4"),
    111:("T20 T15 D3","T20 T13 D6","T20 T11 D9"),
    112:("T20 Bull D1","T20 T16 D2","T20 T14 D5"),
    113:("T20 T17 D1","T20 T15 D4","T20 T13 D7"),
    114:("T20 Bull D2","T20 T16 D3","T20 T14 D6"),
    115:("T20 T17 D2","T20 T15 D5","T20 T13 D8"),
    116:("T20 T18 D1","T20 Bull D3","T20 T16 D4"),
    117:("T20 T17 D3","T20 T15 D6","T20 T13 D9"),
    118:("T20 T18 D2","T20 Bull D4","T20 T16 D5"),
    119:("T20 T19 D1","T20 T17 D4","T20 T15 D7"),
    120:("T20 T18 D3","T20 Bull D5","T20 T16 D6"),
    121:("T20 T19 D2","T20 T17 D5","T20 T15 D8"),
    122:("T20 T20 D1","T20 T18 D4","T20 Bull D6"),
    123:("T20 T19 D3","T20 T17 D6","T20 T15 D9"),
    124:("T20 T20 D2","T20 T18 D5","T20 Bull D7"),
    125:("T20 T19 D4","T20 T17 D7","T20 T15 D10"),
    126:("T20 T20 D3","T20 T18 D6","T20 Bull D8"),
    127:("T20 T19 D5","T20 T17 D8","T20 T15 D11"),
    128:("T20 T20 D4","T20 T18 D7","T20 Bull D9"),
    129:("T20 T19 D6","T20 T17 D9","T20 T15 D12"),
    130:("T20 T20 D5","T20 T18 D8","T20 Bull D10"),
    131:("T20 T19 D7","T20 T17 D10","T20 T15 D13"),
    132:("T20 T20 D6","T20 T18 D9","T20 Bull D11"),
    133:("T20 T19 D8","T20 T17 D11","T20 T15 D14"),
    134:("T20 T20 D7","T20 T18 D10","T20 Bull D12"),
    135:("T20 T19 D9","T20 T17 D12","T20 T15 D15"),
    136:("T20 T20 D8","T20 T18 D11","T20 Bull D13"),
    137:("T20 T19 D10","T20 T17 D13","T20 T15 D16"),
    138:("T20 T20 D9","T20 T18 D12","T20 Bull D14"),
    139:("T20 T19 D11","T20 T17 D14","T20 T15 D17"),
    140:("T20 T20 D10","T20 T18 D13","T20 Bull D15"),
    141:("T20 T19 D12","T20 T17 D15","T20 T15 D18"),
    142:("T20 T20 D11","T20 T18 D14","T20 Bull D16"),
    143:("T20 T19 D13","T20 T17 D16","T20 T15 D19"),
    144:("T20 T20 D12","T20 T18 D15","T20 Bull D17"),
    145:("T20 T19 D14","T20 T17 D17","T20 T15 D20"),
    146:("T20 T20 D13","T20 T18 D16","T20 Bull D18"),
    147:("T20 T19 D15","T20 T17 D18","T19 T20 D15"),
    148:("T20 T20 D14","T20 T18 D17","T20 Bull D19"),
    149:("T20 T19 D16","T20 T17 D19","T20 T13 Bull"),
    150:("T20 T20 D15","T20 T18 D18","T20 Bull D20"),
    151:("T20 T19 D17","T20 T17 D20","T19 T20 D17"),
    152:("T20 T20 D16","T20 T18 D19","T20 T14 Bull"),
    153:("T20 T19 D18","T19 T20 D18",""),
    154:("T20 T20 D17","T20 T18 D20","T19 T19 D20"),
    155:("T20 T19 D19","T20 T15 Bull","T19 T20 D19"),
    156:("T20 T20 D18","",""),
    157:("T20 T19 D20","T19 T20 D20","T19 Bull Bull"),
    158:("T20 T20 D19","T20 T16 Bull","T19 T17 Bull"),
    160:("T20 T20 D20","T20 Bull Bull","Bull T20 Bull"),
    161:("T20 T17 Bull","T19 T18 Bull","T18 T19 Bull"),
    164:("T20 T18 Bull","T19 T19 Bull","T18 T20 Bull"),
    167:("T20 T19 Bull","T19 T20 Bull",""),
    170:("T20 T20 Bull","",""),
}

FIRST_DART_DOUBLE_OUTS={
    2:("D1","",""),
    3:("S1 D1","",""),
    4:("D2","D1 D1","S2 D1"),
    5:("T1 D1","S3 D1","S1 D2"),
    6:("D3","D2 D1","S4 D1"),
    7:("S5 D1","S3 D2","T1 D2"),
    8:("D4","D3 D1","S6 D1"),
    9:("S7 D1","S5 D2","S3 D3"),
    10:("D5","D4 D1","S8 D1"),
    11:("T3 D1","S9 D1","S7 D2"),
    12:("D6","D5 D1","S10 D1"),
    13:("S11 D1","S9 D2","T3 D2"),
    14:("D7","D6 D1","S12 D1"),
    15:("S13 D1","S11 D2","S9 D3"),
    16:("D8","D7 D1","S14 D1"),
    17:("T5 D1","S15 D1","S13 D2"),
    18:("D9","D8 D1","S16 D1"),
    19:("S17 D1","S15 D2","T5 D2"),
    20:("D10","D9 D1","S18 D1"),
    21:("S19 D1","S17 D2","S15 D3"),
    22:("D11","D10 D1","S20 D1"),
    23:("T7 D1","S19 D2","S17 D3"),
    24:("D12","D11 D1","D10 D2"),
    25:("T7 D2","S19 D3","S17 D4"),
    26:("D13","D12 D1","T8 D1"),
    27:("Outer Bull D1","T7 D3","S19 D4"),
    28:("D14","D13 D1","D12 D2"),
    29:("T9 D1","Outer Bull D2","T7 D4"),
    30:("D15","D14 D1","D13 D2"),
    31:("T9 D2","Outer Bull D3","T7 D5"),
    32:("D16","D15 D1","T10 D1"),
    33:("T9 D3","Outer Bull D4","T7 D6"),
    34:("D17","D16 D1","D15 D2"),
    35:("T11 D1","T9 D4","Outer Bull D5"),
    36:("D18","D17 D1","D16 D2"),
    37:("T11 D2","T9 D5","Outer Bull D6"),
    38:("D19","D18 D1","T12 D1"),
    39:("T11 D3","T9 D6","Outer Bull D7"),
    40:("D20","D19 D1","D18 D2"),
    41:("T13 D1","T11 D4","T9 D7"),
    42:("D20 D1","D19 D2","D18 D3"),
    43:("T13 D2","T11 D5","T9 D8"),
    44:("T14 D1","D20 D2","D19 D3"),
    45:("T13 D3","T11 D6","T9 D9"),
    46:("T14 D2","D20 D3","D19 D4"),
    47:("T15 D1","T13 D4","T11 D7"),
    48:("T14 D3","D20 D4","D19 D5"),
    49:("T15 D2","T13 D5","T11 D8"),
    50:("Bull","T16 D1","T14 D4"),
    51:("T15 D3","T13 D6","T11 D9"),
    52:("Bull D1","T16 D2","T14 D5"),
    53:("T17 D1","T15 D4","T13 D7"),
    54:("Bull D2","T16 D3","T14 D6"),
    55:("T17 D2","T15 D5","T13 D8"),
    56:("T18 D1","Bull D3","T16 D4"),
    57:("T17 D3","T15 D6","T13 D9"),
    58:("T18 D2","Bull D4","T16 D5"),
    59:("T19 D1","T17 D4","T15 D7"),
    60:("T18 D3","Bull D5","T16 D6"),
    61:("T19 D2","T17 D5","T15 D8"),
    62:("T20 D1","T18 D4","Bull D6"),
    63:("T19 D3","T17 D6","T15 D9"),
    64:("T20 D2","T18 D5","Bull D7"),
    65:("T19 D4","T17 D7","T15 D10"),
    66:("T20 D3","T18 D6","Bull D8"),
    67:("T19 D5","T17 D8","T15 D11"),
    68:("T20 D4","T18 D7","Bull D9"),
    69:("T19 D6","T17 D9","T15 D12"),
    70:("T20 D5","T18 D8","Bull D10"),
    71:("T19 D7","T17 D10","T15 D13"),
    72:("T20 D6","T18 D9","Bull D11"),
    73:("T19 D8","T17 D11","T15 D14"),
    74:("T20 D7","T18 D10","Bull D12"),
    75:("T19 D9","T17 D12","T15 D15"),
    76:("T20 D8","T18 D11","Bull D13"),
    77:("T19 D10","T17 D13","T15 D16"),
    78:("T20 D9","T18 D12","Bull D14"),
    79:("T19 D11","T17 D14","T15 D17"),
    80:("T20 D10","T18 D13","Bull D15"),
    81:("T19 D12","T17 D15","T15 D18"),
    82:("T20 D11","T18 D14","Bull D16"),
    83:("T19 D13","T17 D16","T15 D19"),
    84:("T20 D12","T18 D15","Bull D17"),
    85:("T19 D14","T17 D17","T15 D20"),
    86:("T20 D13","T18 D16","Bull D18"),
    87:("T19 D15","T17 D18",""),
    88:("T20 D14","T18 D17","Bull D19"),
    89:("T19 D16","T17 D19","T13 Bull"),
    90:("T20 D15","T18 D18","Bull D20"),
    91:("T19 D17","T17 D20",""),
    92:("T20 D16","T18 D19","T14 Bull"),
    93:("T19 D18","",""),
    94:("T20 D17","T18 D20",""),
    95:("T19 D19","T15 Bull",""),
    96:("T20 D18","",""),
    97:("T19 D20","",""),
    98:("T20 D19","T16 Bull",""),
    100:("T20 D20","Bull Bull",""),
    101:("T17 Bull","",""),
    104:("T18 Bull","",""),
    107:("T19 Bull","",""),
    110:("T20 Bull","",""),
}

SECOND_DART_DOUBLE_OUTS={
    2:("D1","",""),
    4:("D2","",""),
    6:("D3","",""),
    8:("D4","",""),
    10:("D5","",""),
    12:("D6","",""),
    14:("D7","",""),
    16:("D8","",""),
    18:("D9","",""),
    20:("D10","",""),
    22:("D11","",""),
    24:("D12","",""),
    26:("D13","",""),
    28:("D14","",""),
    30:("D15","",""),
    32:("D16","",""),
    34:("D17","",""),
    36:("D18","",""),
    38:("D19","",""),
    40:("D20","",""),
    50:("Bull","",""),
}

FIRST_DART_STRAIGHT_OUTS={
    1:("S1","",""),
    2:("D1","S1 S1",""),
    3:("T1","D1 S1","S2 S1"),
    4:("D2","S3 S1","T1 S1"),
    5:("S5","D2 S1","S4 S1"),
    6:("T2","S5 S1","D2 D1"),
    7:("S7","D3 S1","S6 S1"),
    8:("D4","S7 S1","D3 D1"),
    9:("T3","D4 S1","S8 S1"),
    10:("D5","S9 S1","T3 S1"),
    11:("S11","D5 S1","S10 S1"),
    12:("T4","S11 S1","D5 D1"),
    13:("S13","D6 S1","S12 S1"),
    14:("D7","S13 S1","D6 D1"),
    15:("T5","D7 S1","S14 S1"),
    16:("D8","S15 S1","T5 S1"),
    17:("S17","D8 S1","S16 S1"),
    18:("T6","S17 S1","D8 D1"),
    19:("S19","D9 S1","S18 S1"),
    20:("D10","S19 S1","D9 D1"),
    21:("T7","D10 S1","S20 S1"),
    22:("D11","T7 S1","D10 D1"),
    23:("D11 S1","T7 D1","T7 S2"),
    24:("T8","D11 D1","D11 S2"),
    25:("Outer Bull","D12 S1","T8 S1"),
    26:("D13","Outer Bull S1","D12 D1"),
    27:("T9","D13 S1","Outer Bull D1"),
    28:("D14","T9 S1","D13 D1"),
    29:("D14 S1","T9 D1","T9 S2"),
    30:("T10","D14 D1","D14 S2"),
    31:("T10 S1","D15 S1","D14 S3"),
    32:("D16","D15 D1","D15 S2"),
    33:("T11","D16 S1","D15 S3"),
    34:("D17","T11 S1","D16 D1"),
    35:("D17 S1","T11 D1","T11 S2"),
    36:("T12","D17 D1","D17 S2"),
    37:("T12 S1","D18 S1","D17 S3"),
    38:("D19","D18 D1","D18 S2"),
    39:("T13","D19 S1","D18 S3"),
    40:("D20","T13 S1","D19 D1"),
    41:("D20 S1","T13 D1","T13 S2"),
    42:("T14","D20 D1","D20 S2"),
    43:("T14 S1","D20 S3","D20 T1"),
    44:("T14 D1","T14 S2","D20 D2"),
    45:("T15","T14 S3","T14 T1"),
    46:("T15 S1","T14 D2","T14 S4"),
    47:("T15 D1","T15 S2","T14 S5"),
    48:("T16","T15 S3","T15 T1"),
    49:("T16 S1","T15 D2","T15 S4"),
    50:("Bull","T16 D1","T16 S2"),
    51:("T17","Bull S1","T16 S3"),
    52:("T17 S1","Bull D1","Bull S2"),
    53:("T17 D1","T17 S2","Bull S3"),
    54:("T18","T17 S3","T17 T1"),
    55:("T18 S1","T17 D2","T17 S4"),
    56:("T18 D1","T18 S2","T17 S5"),
    57:("T19","T18 S3","T18 T1"),
    58:("T19 S1","T18 D2","T18 S4"),
    59:("T19 D1","T19 S2","T18 S5"),
    60:("T20","T19 S3","T19 T1"),
    61:("T20 S1","T19 D2","T19 S4"),
    62:("T20 D1","T20 S2","T19 S5"),
    63:("T20 T1","T20 S3","T19 D3"),
    64:("T20 D2","T20 S4","T19 S7"),
    65:("T20 S5","T19 D4","T19 S8"),
    66:("T20 T2","T20 D3","T20 S6"),
    67:("T20 S7","T19 D5","T19 S10"),
    68:("T20 D4","T20 S8","T19 S11"),
    69:("T20 T3","T20 S9","T19 D6"),
    70:("T20 D5","T20 S10","T19 S13"),
    71:("T20 S11","T19 D7","T19 S14"),
    72:("T20 T4","T20 D6","T20 S12"),
    73:("T20 S13","T19 D8","T19 S16"),
    74:("T20 D7","T20 S14","T19 S17"),
    75:("T20 T5","T20 S15","T19 D9"),
    76:("T20 D8","T20 S16","T19 S19"),
    77:("T20 S17","T19 D10","T19 S20"),
    78:("T20 T6","T20 D9","T20 S18"),
    79:("T20 S19","T19 D11","T18 Outer Bull"),
    80:("T20 D10","T20 S20","T18 D13"),
    81:("T20 T7","T19 D12","T19 T8"),
    82:("T20 D11","T19 Outer Bull","T18 D14"),
    83:("T19 D13","T17 D16","Bull T11"),
    84:("T20 T8","T20 D12","T19 T9"),
    85:("T20 Outer Bull","T19 D14","T17 D17"),
    86:("T20 D13","T18 D16","Bull D18"),
    87:("T20 T9","T19 D15","T19 T10"),
    88:("T20 D14","T18 D17","Bull D19"),
    89:("T19 D16","T17 D19","Bull T13"),
    90:("T20 T10","T20 D15","T19 T11"),
    91:("T19 D17","T17 D20","D20 T17"),
    92:("T20 D16","T18 D19","Bull T14"),
    93:("T20 T11","T19 D18","T19 T12"),
    94:("T20 D17","T18 D20","D20 T18"),
        95: ("T19 D19", "Bull T15", "T15 Bull"),
    96: ("T20 T12", "T20 D18", "T19 T13"),
    97: ("T19 D20", "D20 T19", ""),
    98: ("T20 D19", "Bull T16", "T16 Bull"),
    99: ("T20 T13", "T19 T14", "T18 T15"),
    100: ("T20 D20", "Bull Bull", "D20 T20"),
    101: ("T17 Bull", "Bull T17", ""),
    102: ("T20 T14", "T19 T15", "T18 T16"),
    104: ("T18 Bull", "Bull T18", ""),
    105: ("T20 T15", "T19 T16", "T18 T17"),
    107: ("T19 Bull", "Bull T19", ""),
    108: ("T20 T16", "T19 T17", "T18 T18"),
    110: ("T20 Bull", "Bull T20", ""),
    111: ("T20 T17", "T19 T18", "T18 T19"),
    114: ("T20 T18", "T19 T19", "T18 T20"),
    117: ("T20 T19", "T19 T20", ""),
    120: ("T20 T20", "", ""),
}

# ================= SECOND DART STRAIGHT OUTS =================

SECOND_DART_STRAIGHT_OUTS = {
    1: ("S1", "", ""),
    2: ("D1", "S2", ""),
    3: ("T1", "S3", ""),
    4: ("D2", "S4", ""),
    5: ("S5", "", ""),
    6: ("T2", "D3", "S6"),
    7: ("S7", "", ""),
    8: ("D4", "S8", ""),
    9: ("T3", "S9", ""),
    10: ("D5", "S10", ""),
    11: ("S11", "", ""),
    12: ("T4", "D6", "S12"),
    13: ("S13", "", ""),
    14: ("D7", "S14", ""),
    15: ("T5", "S15", ""),
    16: ("D8", "S16", ""),
    17: ("S17", "", ""),
    18: ("T6", "D9", "S18"),
    19: ("S19", "", ""),
    20: ("D10", "S20", ""),
    21: ("T7", "", ""),
    22: ("D11", "", ""),
    24: ("T8", "D12", ""),
    25: ("Outer Bull", "", ""),
    26: ("D13", "", ""),
    27: ("T9", "", ""),
    28: ("D14", "", ""),
    30: ("T10", "D15", ""),
    32: ("D16", "", ""),
    33: ("T11", "", ""),
    34: ("D17", "", ""),
    36: ("T12", "D18", ""),
    38: ("D19", "", ""),
    39: ("T13", "", ""),
    40: ("D20", "", ""),
    42: ("T14", "", ""),
    45: ("T15", "", ""),
    48: ("T16", "", ""),
    50: ("Bull", "", ""),
    51: ("T17", "", ""),
    54: ("T18", "", ""),
    57: ("T19", "", ""),
    60: ("T20", "", ""),
}

# ================= SECOND DART DOUBLE OUT =================

# The remaining route handlers use the session values
# saved by the earlier routes.

@app.route("/first-num", methods=["POST"])
def enter_start_num():
    start_num = int(request.form.get("start"))
    session["start_num"] = start_num

    out_type = session.get("out_type")

    if out_type == "straight":
        routes = STRAIGHT_START_OUTS.get(start_num)
        if routes:
            return render_checkout(start_num, routes)

        if start_num > 180:
            return render_checkout(start_num, ("", "", ""))
        return render_checkout(start_num, ("", "", ""))

    if out_type == "double":
        routes = DOUBLE_START_OUTS.get(start_num)
        if routes:
            return render_checkout(start_num, routes)

        return render_checkout(start_num, ("", "", ""))

    return render_template("out.html")


@app.route("/first-dart-double", methods=["POST"])
def first_dart_double():
    hit = int(request.form.get("hitDouble1"))
    session["first_double_hit"] = hit

    left_over = session["start_num"] - hit

    if left_over <= 0:
        return render_checkout(left_over, ("", "", ""))

    routes = FIRST_DART_DOUBLE_OUTS.get(left_over, ("", "", ""))
    return render_checkout(left_over, routes)


@app.route("/second-dart-double", methods=["POST"])
def second_dart_double():
    hit = int(request.form.get("hitDouble2"))
    session["second_double_hit"] = hit

    left_over = (
        session["start_num"]
        - session["first_double_hit"]
        - hit
    )

    if left_over <= 0:
        return render_checkout(left_over, ("", "", ""))

    routes = SECOND_DART_DOUBLE_OUTS.get(left_over, ("", "", ""))
    return render_checkout(left_over, routes)


@app.route("/third-dart-double", methods=["POST"])
def third_dart_double():
    hit = int(request.form.get("hitDouble3"))

    left_over = (
        session["start_num"]
        - session["first_double_hit"]
        - session["second_double_hit"]
        - hit
    )

    return render_checkout(left_over, ("", "", ""))


@app.route("/first-dart-straight", methods=["POST"])
def first_dart_straight():
    hit = int(request.form.get("hitStraight1"))
    session["first_straight_hit"] = hit

    left_over = session["start_num"] - hit

    if left_over <= 0:
        return render_checkout(left_over, ("", "", ""))

    routes = FIRST_DART_STRAIGHT_OUTS.get(left_over, ("", "", ""))
    return render_checkout(left_over, routes)


@app.route("/second-dart-straight", methods=["POST"])
def second_dart_straight():
    hit = int(request.form.get("hitStraight2"))
    session["second_straight_hit"] = hit

    left_over = (
        session["start_num"]
        - session["first_straight_hit"]
        - hit
    )

    if left_over <= 0:
        return render_checkout(left_over, ("", "", ""))

    routes = SECOND_DART_STRAIGHT_OUTS.get(left_over, ("", "", ""))
    return render_checkout(left_over, routes)


@app.route("/third-dart-straight", methods=["POST"])
def third_dart_straight():
    hit = int(request.form.get("hitStraight3"))

    left_over = (
        session["start_num"]
        - session["first_straight_hit"]
        - session["second_straight_hit"]
        - hit
    )

    return render_checkout(left_over, ("", "", ""))


if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)
            