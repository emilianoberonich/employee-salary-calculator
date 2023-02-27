from typing import Tuple

from salary_calculator import get_salary_calculator


def calculate_salary(data) -> Tuple[str, int]:
    salary_calculator = get_salary_calculator(worked_hours_data=data, payment_rates_filename="payment_rates.txt")
    return salary_calculator.calculate()


def calculate_salaries():
    with open("worked_hours.txt") as f:
        employee_worked_hours = f.readlines()
    for worked_hours in employee_worked_hours:
        (name, salary) = calculate_salary(worked_hours)
        print(f"The amount to pay {name} is: {salary} USD")


if __name__ == '__main__':
    calculate_salaries()
