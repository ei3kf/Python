#!/usr/bin/python

"""
 eleven_prefix.py - displays list of 11M CB prefixes and country
 can specify prefix or country
"""

import sys
import argparse


def divisions_list():
    divisions = {
    1: "Italy",
    2: "United States of America",
    3: "Brazil",
    4: "Argentina",
    5: "Venezuela",
    6: "Colombia",
    7: "Netherlands Antilles",
    8: "Peru",
    9: "Canada",
    10: "Mexico",
    11: "Puerto Rico",
    12: "Uruguay",
    13: "Germany",
    14: "France",
    15: "Switzerland",
    16: "Belgium",
    17: "Hawaii",
    18: "Greece",
    19: "Netherlands",
    20: "Norway",
    21: "Sweden",
    22: "Guiana French",
    23: "Jamaica",
    24: "Panama",
    25: "Japan",
    26: "England",
    27: "Iceland",
    28: "Honduras",
    29: "Ireland",
    30: "Spain",
    31: "Portugal",
    32: "Chile",
    33: "Alaska",
    34: "Canary Islands",
    35: "Austria",
    36: "San Marino",
    37: "Dominican Republic",
    38: "Greenland",
    39: "Angola",
    40: "Liechtenstein",
    41: "New Zealand",
    42: "Liberia",
    43: "Australia",
    44: "South Africa",
    45: "Yugoslavia",
    46: "East Germany",
    47: "Denmark",
    48: "Saudi Arabia",
    49: "Balearic Islands",
    50: "European Russia",
    51: "Andorra",
    52: "Faroer Islands",
    53: "El Salvador",
    54: "Luxembourg",
    55: "Gibraltar",
    56: "Finland",
    57: "India",
    58: "East Malaysia",
    59: "Dodecanese Islands",
    60: "Hong Kong",
    61: "Ecuador",
    62: "Guam",
    63: "St. Helena",
    64: "Senegal",
    65: "Sierra Leone",
    66: "Mauritania",
    67: "Paraguay",
    68: "North Ireland",
    69: "Costa Rica",
    70: "Samoa American",
    71: "Midway Islands",
    72: "Guatemala",
    73: "Suriname",
    74: "Namibia",
    75: "Azores",
    76: "Morocco",
    77: "Ghana",
    78: "Zambia",
    79: "Philippines",
    80: "Bolivia",
    81: "San Andres &",
    82: "Guantanamo Bay",
    83: "Tanzania",
    84: "Ivory Coast",
    85: "Zimbabwe",
    86: "Nepal",
    87: "Yemen",
    88: "Cuba",
    89: "Nigeria",
    90: "Crete",
    91: "Indonesia",
    92: "Libya",
    93: "Malta",
    94: "United Arab Emirates",
    95: "Mongolia",
    96: "Tonga",
    97: "Israel",
    98: "Singapore",
    99: "Fiji",
    100: "Korea Republic",
    101: "Papua New Guinea",
    102: "Kuwait",
    103: "Haiti",
    104: "Corsica",
    105: "Botswana",
    106: "Ceuta + Melilla",
    107: "Monaco",
    108: "Scotland",
    109: "Hungary",
    110: "Cyprus",
    111: "Jordan",
    112: "Lebanon",
    113: "West Malaysia",
    114: "Pakistan",
    115: "Qatar",
    116: "Turkey",
    117: "Egypt",
    118: "Gambia",
    119: "Madeira",
    120: "Antigua + Barbuda",
    121: "Bahamas",
    122: "Barbados",
    123: "Bermuda",
    124: "St. Paul + Amsterdam",
    125: "Cayman Islands",
    126: "Nicaragua",
    127: "Virgin Islands American",
    128: "Virgin Islands British",
    129: "Macquarie Islands",
    130: "Norfolk Island",
    131: "Guyana",
    132: "Marshall Islands",
    133: "Northern Mariana Islands",
    134: "Republic of Belau",
    135: "Solomon Islands",
    136: "Martinique",
    137: "Isle of Man",
    138: "Vatican",
    139: "South Yemen",
    140: "Antarctica",
    141: "St. Pierre + Miquelon",
    142: "Lesotho",
    143: "St. Lucia",
    144: "Eastern Island",
    145: "Galapagos Islands",
    146: "Algeria",
    147: "Tunisia",
    148: "Ascension Island",
    149: "Laccadive Islands",
    150: "Bahrain",
    151: "Iraq",
    152: "Maldives",
    153: "Thailand",
    154: "Iran",
    155: "Taiwan",
    156: "Cameroon",
    157: "Montserrat",
    158: "Trinidad + Tobago",
    159: "Somalia",
    160: "Sudan",
    161: "Poland",
    162: "Zaire",
    163: "Wales",
    164: "Togo",
    165: "Sardinia",
    166: "St. Maarten, Saba,",
    167: "Jersey Island",
    168: "Mauritius",
    169: "Guernsey Island",
    170: "Burkina Faso",
    171: "Svalbard Islands",
    172: "New Caledonia",
    173: "Reunion",
    174: "Uganda",
    175: "Chad",
    176: "Central African Republic",
    177: "Sri Lanka",
    178: "Bulgaria",
    179: "Czechoslovakia",
    180: "Oman",
    181: "Syria",
    182: "Guinea Republic",
    183: "Benin",
    184: "Burundi",
    185: "Comoros",
    186: "Djibouti",
    187: "Kenya",
    188: "Madagascar",
    189: "Mayotte",
    190: "Seychelles",
    191: "Swaziland",
    192: "Cocos Islands",
    193: "Cocos Keeling",
    194: "Dominica",
    195: "Grenada",
    196: "Guadeloupe",
    197: "Vanuatu",
    198: "Falkland Islands",
    199: "Equatorial Guinea",
    200: "South Shetland Islands",
    201: "Polynesia French",
    202: "Bhutan",
    203: "China People's Republic",
    204: "Mozambique",
    205: "Cape Verde",
    206: "Ethiopia",
    207: "St. Martin Island",
    208: "Glorieuses Islands",
    209: "Juan de Nova",
    210: "Wallis and Futuna",
    211: "Jan Mayen Island",
    212: "Aland Islands",
    213: "Market Reef",
    214: "Congo",
    215: "Gabon",
    216: "Mali",
    217: "Christmas Island",
    218: "Belize",
    219: "Anguilla",
    220: "St. Vincent + Dependencies",
    221: "South Orkney Islands",
    222: "South Sandwich Islands",
    223: "Samoa Western",
    224: "Western Kiribati",
    225: "Brunei Darussalam",
    226: "Malawi",
    227: "Rwanda",
    228: "Chagos Islands",
    229: "Heard Island",
    230: "Micronesia",
    231: "St. Peter + St. Paul Rocks",
    232: "Aruba",
    233: "Romania",
    234: "Afghanistan",
    235: "ITU Geneva",
    236: "Bangladesh",
    237: "Myanmar",
    238: "Cambodia",
    239: "Laos",
    240: "Macao",
    241: "Spratly Island",
    242: "Vietnam",
    243: "Agalega + St. Brandon Islands",
    244: "Pagalu Island",
    245: "Niger",
    246: "Sao Tome + Principe",
    247: "Navassa Island",
    248: "Turks + Caicos Islands",
    249: "Northern Cook Islands",
    250: "Cook Islands",
    251: "Albania",
    252: "Revillagigedo Island",
    253: "Andaman + Nicobar Islands",
    254: "Mount Athos",
    255: "Kerguelen Islands",
    256: "Prince Edward + Marion Islands",
    257: "Rodriguez Island",
    258: "Tristan da Cunha + Gough Islands",
    259: "Tromelin Island",
    260: "Baker + Howland Islands",
    261: "Chatham Islands",
    262: "Johnston Island",
    263: "Kermadec Islands",
    264: "Kingman Reef",
    265: "Central Kiribati",
    266: "Eastern Kiribati",
    267: "Kure Island",
    268: "Lord Howe Island",
    269: "Mellish Reef",
    270: "Minami Torishima Island",
    271: "Nauru",
    272: "Niue",
    273: "Jarvis + Palmyra Islands",
    274: "Pitcairn Island",
    275: "Tokelau Islands",
    276: "Tuvalu",
    277: "Sable Island",
    278: "Wake Island",
    279: "Willis Islets",
    280: "Aves Island",
    281: "Ogasawara Islands",
    282: "Auckland + Campbell Islands",
    283: "St. Kitts + Nevis",
    284: "St. Paul Island",
    285: "Fernando de Noronha",
    286: "Juan Fernandez Island",
    287: "Malpelo Island",
    288: "San Felix + San Ambrosio",
    289: "South Georgia Island",
    290: "Trindade + Martim Vaz Islands",
    291: "Dhekelia + Akrotiri",
    292: "Abu-Ail + Jabal-At-Tair",
    293: "Guinea Bissau",
    294: "Peter 1st Island",
    295: "Southern Sudan",
    296: "Clipperton Island",
    297: "Bouvet Island",
    298: "Crozet Islands",
    299: "Desecheo Island",
    300: "West Sahara - Rio de Oro",
    301: "Armenia",
    302: "Asiatic Russia",
    303: "Azerbaijan",
    304: "Estonia",
    305: "Franz Josef Land",
    306: "Georgia",
    307: "Kaliningradsk",
    308: "Kazakhstan",
    309: "Kyrgyzstan",
    310: "Latvia",
    311: "Lithuania",
    312: "Moldova",
    313: "Tajikistan",
    314: "Turkmenistan",
    315: "Ukraine",
    316: "Uzbekistan",
    317: "White Russia",
    318: "Survey Military of",
    319: "United Nations - New York",
    320: "Banaba Island",
    321: "Conway Reef",
    322: "Walvis Bay",
    323: "Yemen",
    324: "Penguin Island",
    325: "Rotuma Island",
    326: "Malyj Vytsotskj",
    327: "Slovenia",
    328: "Croatia",
    329: "Czech",
    330: "Slovakia",
    331: "Bosnia Herzegovina",
    332: "Macedonia",
    333: "Eritrea",
    334: "Korea Democratic People's",
    335: "Pratas Island",
    336: "Scarborough Reef",
    337: "Austral Islands",
    338: "Marquesas Islands",
    339: "Temotu Islands",
    340: "Palestine",
    341: "East Timor",
    342: "Chesterfield Islands",
    343: "Ducie Island",
    344: "Republic of Montenegro",
    345: "Swain's Island",
    346: "St. Barthelemy",
    347: "Curacao",
    348: "St. Maarten",
    349: "St. Eustatius/Saba"}
    return divisions


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--division",
        help="11M division",
        type=int)
    parser.add_argument(
        "--country",
        help="11M country",
        type=str)
    args = parser.parse_args()

    divisions = divisions_list()

    if args.division:
        for prefix, country in divisions.items():
            if prefix == args.division:
                print prefix, country
        sys.exit(0)
    elif args.country:
        for prefix, country in divisions.items():
            if country.lower() in args.country.lower():
                print prefix, country
    else:
        for prefix, country in divisions.items():
            print prefix, country
