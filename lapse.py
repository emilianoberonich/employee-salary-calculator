class Lapse:
    """
    Represents a lapse of hours on a given day.
    It is used to represent the hours that an employee worked.
    """
    def __init__(self, day: str, start: str, end: str):
        """
        Initialize the instance copying the values for the day, the start and end hour of the lapse.
        """
        self.day = day
        self.start = int(start.split(":")[0])
        self.end = int(end.split(":")[0])
        if self.end == 0:
            self.end = 24
