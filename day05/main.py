import os

BASE_DIR = os.path.dirname(__file__)

TRANS_TABLE = {ord("F"): "0", ord("B"): "1", ord("R"): "1", ord("L"): "0"}
SEAT_ROW = slice(0, 7)
SEAT_COL = slice(7, 10)


def get_unique_seat_id(boarding_pass):
    boarding_pass = boarding_pass.translate(TRANS_TABLE)
    return int(boarding_pass[SEAT_ROW], 2) * 8 + int(boarding_pass[SEAT_COL], 2)


with open(os.path.join(BASE_DIR, "data.in"), "r") as fp:
    boarding_passes = map(str.strip, fp)
    print("Task 1 count:", max(map(get_unique_seat_id, boarding_passes)))
