from typing import List, Tuple

from lapse import Lapse
from payment_rate_source import PaymentRate, PaymentRateSource, TextPaymentRateSource
from worked_hours_source import TextWorkedHoursSource, WorkedHoursSource


def get_salary_calculator(payment_rates_filename, worked_hours_data):
    worked_hours_source = TextWorkedHoursSource(worked_hours_data)
    payment_rate_source = TextPaymentRateSource(payment_rates_filename)
    salary_calculator = SalaryCalculator(worked_hours_source=worked_hours_source,
                                         payment_rate_source=payment_rate_source)
    return salary_calculator


class SalaryCalculator:
    """
    Class for calculating the employee salary given the hours worked at a given rate.

    The variable member worked_hours_source stores an instance that imports the employee's
    worked hours and convert it to a List of Lapse instances.
    The variable member payment_rate_source stores an instance that imports the payment rates used
    to calculate the hour rate.
    The variable member rates stores a list of payment rates used for calculating how much each
    hour is paid.
    """
    def __init__(self, worked_hours_source: WorkedHoursSource, payment_rate_source: PaymentRateSource = None,
                 *args, **kwargs):
        """
        Initialize the source and the rates list.
        """
        self.worked_hours_source = worked_hours_source
        self.payment_rate_source = payment_rate_source
        if self.payment_rate_source:
            self.rates = self.payment_rate_source.get_rates()

    def _calculate_lapse(self, worked_lapse: Lapse) -> int:
        """
        Calculate how much should be paid to an employee for a lapse of hours.
        """
        lapse_payment = 0
        for hour in range(worked_lapse.start, worked_lapse.end):
            found_rate = [rate for rate in self.rates
                          if worked_lapse.day == rate.lapse.day and hour >= rate.lapse.start and hour < rate.lapse.end]
            if found_rate:
                lapse_payment = lapse_payment + found_rate[0].hour_rate
        return lapse_payment

    def set_rates(self, rates: List[PaymentRate]):
        """
        Set the payment rates used to calculate how much is paid the employee by hour.
        """
        self.rates = rates

    def calculate(self) -> Tuple[str, int]:
        """
        Function to calculate how much should be paid to an employee for given worked hours.
        """
        worked_lapses = self.worked_hours_source.get_worked_lapses()
        salary = 0
        for worked_lapse in worked_lapses:
            salary = salary + self._calculate_lapse(worked_lapse)
        name = self.worked_hours_source.get_name()
        return (name, salary)
