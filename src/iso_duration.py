import re

from duration import Duration
from util import convert_to_dict, rename


class ISODuration(object):
    date_map_dict = {"years": "Y", "months": "M", "days": "D"}

    time_map_dict = {
        "hours": "H",
        "minutes": "M",
        "seconds": "S",
        "miliseconds": "m",
        "nanoseconds": "n",
        "microseconds": "u",
    }

    def _is_character_valid(self, duration) -> bool:
        duration_symbols = ["P", "T", "Y", "M", "D", "H", "M", "S", "m", "u", "n"]
        for ch in duration:
            if ch.isalpha() and ch not in duration_symbols:
                return False
        return True

    def _parse_time_duration(self, duration: str) -> dict:
        if self._is_character_valid(duration):
            time_value = re.findall(r"T.*", duration)
            if time_value:
                match = re.findall(
                    r"\d*H|\d*M|\d*S|\d*m|\d*u|\d*n",
                    time_value[0],
                )
                if match:
                    return convert_to_dict(match, add_letter="t")
            return {}

    def _parse_date_duration(self, duration) -> dict:
        if self._is_character_valid(duration):
            date_value = re.match(r"^P:?(\S*)T", duration)
            if date_value:
                match = re.findall(r"\d*Y|\d*M|\d*D", date_value[0])
                if match:
                    return convert_to_dict(match, add_letter="p")
            return {}

    def pars_duration(self, duration: str) -> Duration:
        duration_dict = self._parse_date_duration(duration)
        duration_dict.update(self._parse_time_duration(duration))
        return Duration(duration_dict)

    def _generate_date(self, du: dict) -> str:
        date_duration = rename(du, self.date_map_dict)
        date_string = ""
        for key, value in date_duration.items():
            if value != 0:
                date_string = date_string + str(value) + str(key)
        return "P" + date_string

    def _generate_time(self, du: dict) -> str:
        time_duration = rename(du, self.time_map_dict)
        time_string = ""
        for key, value in time_duration.items():
            if value != 0:
                time_string = time_string + str(value) + str(key)
        return "T" + time_string

    def _remove_date(self, du: dict) -> dict:
        for key, value in self.date_map_dict.items():
            del du[key]
        return du

    def generate(self, duration: Duration) -> str:
        duration_dict = duration.__dict__
        gen_date = self._generate_date(duration_dict)
        duration_dict = self._remove_date(duration_dict)
        gen_time = self._generate_time(duration_dict)

        return gen_date + gen_time


s = "P3Y6M4DT12H24M12S10m12n80u"
s2 = "PT1n"
s3 = "P1DT"
s4 = "P3Y6M4DT12H24M12S10m12n80u"
s5 = "P3Y6M4DT12H24M12S10m12n90u"
s6 = "PT9000000u"
s7 = "PT9000000000n"
s8 = "PT90m"

f1 = "PT18n"
f2 = "PT20n"
duration_list = [s, s2, s3, s4, s5]
# duration_list = [s3]
for duration_value in duration_list:
    d = ISODuration().pars_duration(duration_value)
    print(d.get_seconds())
    assert ISODuration().generate(d) == duration_value
    # print(d.__dict__)
b1 = "P4Y6M4DT12H24M12S10m90u14n"
b2 = "P4Y6M4DT12H24M12S10m90u14n"

d = ISODuration().pars_duration(b1)
d2 = ISODuration().pars_duration(b2)
print(d == d2)
