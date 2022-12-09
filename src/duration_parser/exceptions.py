class DurationParsingException(ValueError):
    ...


class IncorrectDesignator(DurationParsingException):
    def __init__(self, designator):
        super().__init__(f"The {designator} token is invalid")


class IncorrectPattern(DurationParsingException):
    def __init__(self):
        super().__init__("The pattern is incorrect")
