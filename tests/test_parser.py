from src.iso_duration import ISODuration

ISODuration()


def test_parser():
    s = "P3Y6M4DT12H24M12S10m12n80u"
    s2 = "PT1n"
    s3 = "P1DT"
    s4 = "P3Y6M4DT12H24M12S10m12n80u"
    s5 = "P3Y6M4DT12H24M12S10m12n90u"

    duration_list = [s, s2, s3, s4, s5]
    for duration_value in duration_list:
        d = ISODuration().parse(duration_value)
        assert ISODuration().generate(d) == duration_value
