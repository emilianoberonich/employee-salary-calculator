# Employee salary calculator


### Overview

This project calculates the employee's payments provided the employee's worked hours and the payment rates.


### How to use it

To use the script for calculating the employees salaries, 
1. Clone the github repository. It doesn't require any dependency installation.
2. Edit the files payment_rates.txt for modifying the payment rates for different times of the week.
3. Edit the file worked_hours.txt to modify the hours that each employee worked.
4. Run the following command to see the results in the console:
```
python main.py
```

As a result you will see in the console the salaries that each employee should be paid.

To execute the tests, run the following command:
```
python -m unittest
```


### Approach

The approach taken was to implement the main functionality through classes and a simple script to demostrate its use, reading the data from the included text files. The classes could be used in a broader project. The solution could be extended to include other data sources by implementing new descendant classes of PaymentRateSource and WorkedHoursSource. 

For calculating the employee's salary, we convert the specified worked hours entered as a formatted string to a list of Lapse instances, where each instance is used to describe the lapse of consecutives hours worked by an employee and specifying the day of the week. Converting to an internal structure, allows to read from other data sources. Also we convert the payment rates to a list of PaymentRate instances, where each instance describe the hour rate for a given lapse of hours including the day it belongs. For the salary calculation we search for the rate of each worked hour, matching the day and starting hour, and accumulates the hours rate in an temporal variable. 

There are included tests to verify its functionality automatically. It was added enough tests to have a good coverage.


### Architecture

The proposed solution uses the class SalaryCalculator for conveying the main responsibility and coordinate the rest of the implemented classes. 

SalaryCalculator has the responsibility of calculating the employees' salaries. It has 2 inputs: the payment rates and the employee worked hours. The processing of the input data is delegated to a couple of classes and their descendants: PaymentRateSource and WorkedHoursSource. We use the Strategy pattern to allow the extension to read from other data sources. For the scope of this solution, we provide only a class for text and text files as data sources.

The payment rates are the hour rates used to pay the employees at different times on the week. SalaryCalculator uses an instance of a PaymentRateSource to import the payment rates. In the solution there is only one data source which is a string with a particular format, read by the class TextPaymentRateSource. This class allows to read both a textfile or a list of strings. 

To calculate the employee's salary, we also need to pass the employee worked hours to the class SalaryCalculator. The SalaryCalculator instance expect an instance of a WorkedHoursSource descendant. Currently the included solution only allows a formatted string as data source. 


### Improvements

As improvements for the solution, out of the scope of the exercise, we could suggest:
- The search for rate of a worked hour could be improved for example by using an OrderedDict with a key of a combination of the day and the starting hour of the payment rate.
- Other data sources as database, an API or other string formats for the worked hours and payment rates could be added by implementing new descendant classes from WorkedHoursSource and PaymentRateSource.
- Is is assumed that the input strings of the worked hours and payment rates are valid. A validation could be added to look for format and logic errors in the input strings. A logic error could be a missing lapse of hours, a range of hours with more than one payment rate.
