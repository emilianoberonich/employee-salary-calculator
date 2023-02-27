from typing import List, Tuple

from lapse import Lapse


class WorkedHoursSource:
    """
    Base class for importing employee's worked hours' data.
    """
    def __init__(self, *arg, **kwargs):
        self.name = ""
        self.worked_lapses = []

    def import_data(self, *args, **kwargs) -> Tuple[str, list]:
        pass

    def get_worked_lapses(self) -> List[Lapse]:
        return self.worked_lapses

    def get_name(self) -> str:
        return self.name


class TextWorkedHoursSource(WorkedHoursSource):
    """
    Class for importing the employee's worked hours from a string.

    It receives a string with the following format:
    NAME=LIST_OF_WORKED_HOURS

    NAME is a string containing the employee's name.
    LIST_OF_WORKED_HOURS is a string containing the worked hours for the employee with the following format:
    XXSS-00:EE:00,XXSS-00:EE:00,XXSS-00:EE:00,XXSS-00:EE:00
    Where XXSS-00:EE:00 is a lapse of worked hours by the employee.
        XX is the day for the lapse which can be one of the followings options: MO, TU, WE, TH, FR, SA, SU.
        Meaning:
            MO: Monday
            TU: Tuesday
            WE: Wednesday
            TH: Thursday
            FR: Friday
            SA: Saturday
            SU: Sunday
        SS represents the starting hour of the worked lapse.
        EE represents the ending hour of the worked lapse.
    Example:
        RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00
    """
    def __init__(self, worked_hours_data: str = None, *arg, **kwargs):
        WorkedHoursSource.__init__(self, *arg, **kwargs)
        if worked_hours_data:
            self.import_data(worked_hours_data)

    def _process_worked_hour(self, worked_unit: str) -> Lapse:
        """
        Parse the text representing the worked hours.
        """
        if worked_unit:
            day = worked_unit[0:2]
            parts = worked_unit[2:].split("-")
            if len(parts) > 1:
                start = parts[0]
                end = parts[1]
                return Lapse(day, start, end)

    def import_data(self, data: str) -> Tuple[str, list]:
        """
        Convert the string representing the worked hours by an employee to a tuple containing the name
        and a list of Lapse instances (a Lapse instance representing a worked lapse by the employee).
        """
        splitted_data = data.split("=")
        self.name = splitted_data[0]
        days_text = splitted_data[1]
        worked_units = days_text.split(",")
        self.worked_lapses = []
        for worked_unit in worked_units:
            lapse = self._process_worked_hour(worked_unit)
            if lapse:
                self.worked_lapses.append(lapse)
