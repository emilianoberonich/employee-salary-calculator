from typing import List

from lapse import Lapse


class PaymentRate:
    """
    Represents the payment rate for a lapse of hours in a given day.
    """
    def __init__(self, day: str, start: str, end: str, hour_rate: str):
        self.lapse = Lapse(day, start, end)
        self.hour_rate = int(hour_rate)


class PaymentRateSource:
    """
    Base class for data source classes that imports payment rates.
    """
    def __init__(self, *args, **kwargs):
        self.rates = []

    def import_rates(self, *args, **kwargs):
        pass

    def get_rates(self) -> List[PaymentRate]:
        """
        Return a list of payment rates.
        """
        return self.rates


class TextPaymentRateSource(PaymentRateSource):
    """
    Import the payment rates used for rating the employee's worked hours. The payment rates are
    represented by instances of PaymentRate, which contain a lapse of hours and the rate used for paying
    those hours.

    The format expected is:
    XX|SS:00|EE:00|RR
    Where:
        XX is the day for the lapse which can be one of the followings options: MO, TU, WE, TH, FR, SA, SU.
        Meaning:
            MO: Monday
            TU: Tuesday
            WE: Wednesday
            TH: Thursday
            FR: Friday
            SA: Saturday
            SU: Sunday
        SS represents the starting hour of the lapse.
        EE represents the ending hour of the lapse.
        RR is the payment rate used for the hours in the lapse.
    Example:
        MO|00:00|09:00|25
    """

    def __init__(self, filename=None, payment_rates: List[str] = None, *args, **kwargs):
        """
        Initialize the payment rates from a file in case the parameter filename is provided.
        """
        PaymentRateSource.__init__(self, *args, **kwargs)
        if filename or payment_rates:
            if filename and not payment_rates:
                with open(filename) as f:
                    payment_rates = f.readlines()
            self.import_rates(payment_rates)

    def import_rates(self, payment_rates: List[str]):
        """
        Import the payment rates used for rating the employee's worked hours from a list of strings.
        """
        for payment_rate in payment_rates:
            parts = payment_rate.split("|")
            if len(parts) == 4:
                self.rates.append(PaymentRate(parts[0], parts[1], parts[2], parts[3]))
