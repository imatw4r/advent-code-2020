import os

BASE_DIR = os.path.dirname(__file__)

TRANS_TABLE = {ord("F"): "0", ord("B"): "1", ord("R"): "1", ord("L"): "0"}
SEAT_ROW = slice(0, 7)
SEAT_COL = slice(7, 10)


def get_unique_seat_id(boarding_pass: str):
    boarding_pass = boarding_pass.translate(TRANS_TABLE)
    return int(boarding_pass[SEAT_ROW], 2) * 8 + int(boarding_pass[SEAT_COL], 2)


def get_missing_seat_id(seat_ids):
    seat_ids = sorted(seat_ids)
    previous_id = seat_ids[0]
    for current_id in seat_ids:
        if current_id - previous_id == 2:
            return current_id - 1
        previous_id = current_id


with open(os.path.join(BASE_DIR, "data.in"), "r") as fp:
    boarding_passes = map(str.strip, fp)
    seat_ids = list(map(get_unique_seat_id, boarding_passes))
    print("Part 1 answer:", max(seat_ids))
    print("Part 2 answer:", get_missing_seat_id(seat_ids))
