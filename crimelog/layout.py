#!/usr/bin/env python
# vim: set shiftwidth=4 tabstop=4 softtabstop=4 :
"""
Takes Crime Log output in list form (where items in list already have 
HTML stripped out) and produces an object containing relevant data.
"""

#import baseslide
import re


WEEKDAYS = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
TIMES = re.compile('a\.*m\.*$|p\.*m\.*$|[nN]oon\.*$')

"""
class CrimeLog(baseslide.Baseslide):
  pass
"""

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
            elif re.search(TIMES, line) and len(line.split()) <= 2:
                time = CrimeTime(line)
                time.text = self.content[num + 1]
                self.crime_dates[-1].times.append(time)
            else: continue

    def get_entries(self):
        self._read_data()
        return self.crime_dates

class CrimeDate:
    def __init__(self, date):
        self.date = date
        self.times = []

class CrimeTime:
    def __init__(self, time):
        self.time = time
        self.text = None
"""
#For testing purposes
feed = ['Tuesday, Oct. 19', '8 a.m.', 'A student reported that her planner, containing personal information, was missing from the Curry Student Center where she left it unattended.', 'Noon', 'The Student Financial Services office contacted the Northeastern University Division of Public Safety (NUPD) to inform officers of payments made by a stolen credit card on a students account. NUPD is investigating.', 'Wednesday, Oct. 20', '9 p.m.', 'Officers responded to a call reporting the smell of marijuana at 122 St. Stephen St. The officers found three students smoking and confiscated an undisclosed amount of marijuana from their room. All three students have been reported to the Office of Student Conduct and Conflict Resolution (OSCCR).', 'Thursday, Oct. 21', '1 a.m.', 'An NUPD officer on Massachusetts Avenue saw a man exit a car and threaten two students in another car with a baseball bat. Boston Police Department (BPD) officers arrested the man for assault with a dangerous weapon.', '4 p.m.', 'A student reported a suspicious man had been following her for several days. NUPD is investigating the matter.', '4:30 p.m.', 'A student reported his iPod missing from Snell Library, where he left it unattended.', '5 p.m.', 'An NUPD officer stopped three high school students outside Cahners Hall after he saw them smoking marijuana.', 'Friday, Oct. 22', '12:30 a.m.', 'Officers responded to a call from 118 Hemenway St. about water balloons being thrown off the roof. When they arrived, officers found five students and two non-students with wet clothes and water balloons. The students have been reported to OSCCR.', 'Entry of the Week', '2 a.m.', 'Officers responded to a call from the Renaissance Parking Garage about a student who appeared to be assaulted. Upon arrival, the officers found a drunk 19-year-old student in one of the stairwells. NUPD officers are uncertain how the student became injured. He was reported to OSCCR.', '5 p.m.', 'Officers responded to a call from a student reporting someone broke into her apartment at 109 St. Stephen St. When officers arrived, they found someone attempted to break down the door.', '6 pm.', 'Officers broke up an argument between two students outside Davenport Commons B. Both students were reported to OSCCR.', u'Officers searched a student\u2019s room in White Hall as part of an ongoing drug investigation. They found small amounts of marijuana. The student was reported to OSCCR.', '6:30 p.m.', 'A student in Speare Hall reported she suspects her roommate has been stealing her gift cards and clothes from her. NUPD is investigating.', 'Saturday, Oct. 23', '1 a.m.', 'Officers responded to a call about a loud party at 407 Huntington Ave. When officers arrived they found eight students, six of whom were underage. All of the students have been reported to OSCCR.', '2:30 a.m.', 'An officer saw Giorgio Parise and Michael Lehmann, both 19, fighting on Camden Street. Both students were arrested for disorderly conduct.', '2 p.m.', 'A student reported that her bicycle was stolen from outside Stetson East, where she left it Oct. 15.', '11 p.m.', 'Officers responded to a call about a loud party at Smith Hall. When officers arrived, they found five underaged students with alcohol. The students were reported to OSCCR.', 'Sunday, Oct. 24', '10 a.m.', 'Officers responded to two separate calls about possible burglaries at 204 Hemenway St. Officers found no one in the apartments and were unsure if anything was missing. BPD is investigating the matter.', '6 p.m.', 'A students family reported a man on Huntington Avenue threatened them. NUPD has not yet found the man.', '8 p.m.', 'An officer saw two 13-year-old boys dragging a woman across Columbus Avenue. The officer chased and eventually caught the teens. The boys admitted they were trying to rob the woman who refused to give up her purse.']

for date in CrimeLogData(feed).get_entries():
    for time in date.times:
        print date.date, time.time, '--', time.text, '\n'
"""
