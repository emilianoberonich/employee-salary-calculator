import unittest
from main import calculate_salary, get_salary_calculator
from payment_rate_source import TextPaymentRateSource
from salary_calculator import SalaryCalculator
from worked_hours_source import TextWorkedHoursSource


class TestCalculator(unittest.TestCase):
    def test_calculate_salary(self):
        worked_hours_data = "RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00"
        (name, salary) = calculate_salary(worked_hours_data)
        self.assertEqual(name, "RENE")
        self.assertEqual(salary, 215)

        worked_hours_data = "ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00"
        (name, salary) = calculate_salary(worked_hours_data)
        self.assertEqual(name, "ASTRID")
        self.assertEqual(salary, 85)

    def test_get_salary_calculator(self):
        worked_hours_data = "ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00"
        salary_calculator = get_salary_calculator(worked_hours_data=worked_hours_data,
                                                  payment_rates_filename="payment_rates.txt")
        self.assertIsInstance(salary_calculator, SalaryCalculator)
        (name, salary) = salary_calculator.calculate()
        self.assertEqual(name, "ASTRID")
        self.assertEqual(salary, 85)

    def test_payment_rate_source(self):
        payment_rates = ["MO|09:00|18:00|15", "MO|18:00|00:00|20"]
        payment_rate_source = TextPaymentRateSource()
        payment_rate_source.import_rates(payment_rates)
        rate = payment_rate_source.get_rates()[1]
        self.assertEqual(rate.lapse.start, 18)
        self.assertEqual(rate.lapse.end, 24)
        self.assertEqual(rate.lapse.day, "MO")
        self.assertEqual(rate.hour_rate, 20)

    def test_payment_rate_source2(self):
        payment_rates = ["MO|09:00|18:00|15", "MO|18:00|00:00|20"]
        payment_rate_source = TextPaymentRateSource(payment_rates=payment_rates)
        rate = payment_rate_source.get_rates()[1]
        self.assertEqual(rate.lapse.start, 18)
        self.assertEqual(rate.lapse.end, 24)
        self.assertEqual(rate.lapse.day, "MO")
        self.assertEqual(rate.hour_rate, 20)

    def test_set_rates(self):
        worked_hours_source = TextWorkedHoursSource()
        payment_rates = ["MO|09:00|18:00|15", "MO|18:00|00:00|20"]
        payment_rate_source = TextPaymentRateSource()
        payment_rate_source.import_rates(payment_rates)
        salary_calculator = SalaryCalculator(worked_hours_source=worked_hours_source)
        salary_calculator.set_rates(payment_rate_source.get_rates())
        rate = salary_calculator.rates[1]
        self.assertEqual(rate.lapse.start, 18)
        self.assertEqual(rate.lapse.end, 24)
        self.assertEqual(rate.lapse.day, "MO")
        self.assertEqual(rate.hour_rate, 20)

    def test_worked_hours_source(self):
        worked_hours_data = "RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00"
        source = TextWorkedHoursSource()
        source.import_data(worked_hours_data)
        worked_lapses = source.get_worked_lapses()
        name = source.get_name()
        self.assertEqual(name, "RENE")
        self.assertEqual(len(worked_lapses), 5)
        lapse = worked_lapses[3]
        self.assertEqual(lapse.day, "SA")
        self.assertEqual(lapse.start, 14)
        self.assertEqual(lapse.end, 18)

    def test_worked_hours_source2(self):
        worked_hours_data = "RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00"
        source = TextWorkedHoursSource(worked_hours_data=worked_hours_data)
        worked_lapses = source.get_worked_lapses()
        name = source.get_name()
        self.assertEqual(name, "RENE")
        self.assertEqual(len(worked_lapses), 5)
        lapse = worked_lapses[3]
        self.assertEqual(lapse.day, "SA")
        self.assertEqual(lapse.start, 14)
        self.assertEqual(lapse.end, 18)


if __name__ == '__main__':
    unittest.main()
