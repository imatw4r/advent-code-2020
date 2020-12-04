from typing import TypedDict, Optional
from itertools import takewhile
from functools import partial


class Passport(TypedDict):
    byr: str
    iyr: str
    eyr: str
    hgt: str
    hcl: str
    ecl: str
    pid: str
    cid: Optional[str]


class PassportFileReader(object):
    def __init__(self, fp):
        self.fp = fp

    def _to_passport(self, line: str) -> Passport:
        to_key_value_pair = partial(str.split, sep=":")
        return dict(map(to_key_value_pair, line.split(" ")))

    def _build_passport_line(self, fp) -> str:
        return " ".join(map(str.strip, takewhile(lambda line: line != "\n", fp)))

    def __iter__(self):
        return self

    def __next__(self) -> Passport:
        line = self._build_passport_line(self.fp)
        try:
            return self._to_passport(line)
        except ValueError:
            raise StopIteration