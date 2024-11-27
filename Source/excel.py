import gspread
import json

PRIVATE_KEY_PATH = 'google_key.json'
SHEET_PATH = 'sheet.json'

PLAYER_SHEET = None
MATCH_SHEET = None
PLAYER_LIST = None
ELO_DICT = {}

def init():
    gc = gspread.oauth()
    # gc = gspread.service_account(filename=PRIVATE_KEY_PATH)
    # with open(SHEET_PATH, 'r') as f:
    #     data = json.load(f)

    global PLAYER_SHEET, MATCH_SHEET, PLAYER_LIST, ELO_DICT
    # excel = gc.open_by_key(data['sheet1'])
    excel = gc.open_by_url("https://docs.google.com/spreadsheets/d/1vNtmx8LGlo6H4p48o_07YIqqXXLixgM3X9yomMNCwsE/edit?usp=sharing")
    PLAYER_SHEET = excel.worksheet('Player List')
    MATCH_SHEET = excel.worksheet('Match Records')
    PLAYER_LIST = list(filter(None, PLAYER_SHEET.col_values(1)[1:]))

def get_player_list():
    return PLAYER_LIST

def get_elo(name):
    if name in ELO_DICT:
        return ELO_DICT[name]

    row = PLAYER_LIST.index(name) + 2
    elo = int(PLAYER_SHEET.cell(row, 2).value)
    ELO_DICT[name] = elo
    return elo

def add_new_player(name, elo):
    if name in PLAYER_LIST:
        return False

    row = len(PLAYER_LIST) + 2
    PLAYER_SHEET.update_cell(row, 1, name)
    PLAYER_SHEET.update_cell(row, 2, elo)
    
    PLAYER_LIST.append(name)
    return True

init()