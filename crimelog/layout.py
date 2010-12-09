#!/usr/bin/env python
# vim: set shiftwidth=4 tabstop=4 softtabstop=4 :
"""
Takes Crime Log output in list form (where items in list already have 
HTML stripped out) and produces an object containing relevant data.
"""

import baseslide


WEEKDAYS = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
MERIDIEMS = ('a.m.', 'p.m.')

class CrimeLog(baseslide.Baseslide):
  pass

class CrimeLogData:
    def __init__(self, content):
        self.content = content
        self.crime_dates = []
    
    def _read_data(self):
        current_date = None
        for num, line in enumerate(self.content):
            if line.startswith(WEEKDAYS):
                current_date = CrimeDate(line)
                self.crime_dates.append(current_date)
            elif line.endswith(MERIDIEMS) and len(line.split()) == 2:
                time = CrimeTime(line)
                time.text = self.content[num + 1]
                self.crime_dates[self.crime_dates.index(current_date)].times.append(time)
            else: continue

    def get_entries(self):
        self._read_data()
        return self.crime_dates

class CrimeDate:
    def __init__(self, date):
        self.date = date
        self.times = []

    def __eq__(self, other):
        if not isinstance(other, CrimeDate):
            raise NotImplementedError
        return self.date == other.date

class CrimeTime:
    def __init__(self, time):
        self.time = time
        self.text = None

"""
for date in CrimeLogData(feed).get_entries():
    for time in date.times:
        print date.date, time.time, '--', time.text, '\n'
"""
