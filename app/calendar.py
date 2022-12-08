class Calendar:
    SECONDS_IN_MINUTE = 60
    SECONDS_IN_MILI = 0.001
    SECONDS_IN_MICRO = 1e-6
    SECONDS_IN_NANO = 1e-9
    MINUTES_IN_HOUR = 60
    HOURS_IN_DAY = 24
    DAYS_IN_WEEK = 7
    ROUGH_DAYS_IN_MONTH = 30  # U
    DAYS_IN_YEAR = 356  # s
    MAX_WEEKS_IN_YEAR = 53  # In ISO week year, used for truncated dates

    SECONDS_IN_HOUR = SECONDS_IN_MINUTE * MINUTES_IN_HOUR
    SECONDS_IN_DAY = SECONDS_IN_HOUR * HOURS_IN_DAY
    MINUTES_IN_DAY = MINUTES_IN_HOUR * HOURS_IN_DAY
    ROUGH_DAYS_IN_YEAR = DAYS_IN_YEAR
    HOURS_IN_YEAR = DAYS_IN_YEAR * HOURS_IN_DAY
    MINUTES_IN_YEAR = DAYS_IN_YEAR * MINUTES_IN_DAY
    SECONDS_IN_YEAR = DAYS_IN_YEAR * SECONDS_IN_DAY
    SECONDS_IN_MONTH = ROUGH_DAYS_IN_MONTH * SECONDS_IN_DAY

    _DEFAULT = None

    @classmethod
    def default(cls):
        """Return the singleton instance. Create if necessary."""
        if cls._DEFAULT is None:
            cls._DEFAULT = cls()
        return cls._DEFAULT

    def __init__(self):
        self.set_mode()

    def set_mode(self, mode=None):
        pass

    def __repr__(self):
        return "<{0}.{1}>".format(self.__module__, self.__class__.__name__)


CALENDAR = Calendar.default()
