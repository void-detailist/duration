class DurationParsingException(ValueError):
    ...


class IncorrectPattern(DurationParsingException):
    def __init__(self):
        super().__init__("The pattern is incorrect")
