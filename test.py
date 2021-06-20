from pandas import DataFrame
from datetime import datetime, timedelta
from math import ceil as math_ceil
#
#
# title = "test"
#
# df = DataFrame(columns=["title", "date", "start_time", "end_time"])
#
# df = df.append(DataFrame([["test", datetime.today(), datetime.now(), datetime.now() + timedelta(hours=2)]], columns=["title", "date", "start_time", "end_time"]), ignore_index=True)
#
# df.to_csv("%s.csv" % title, index=False, sep=";", na_rep="---")

PreviousWeeks = 8

Year, WeekYear, DayWeek = datetime.today().isocalendar()
YearDiff = math_ceil(PreviousWeeks / 52)

if YearDiff > 0:
    Year -= YearDiff
    WeekYear = (52 * YearDiff) + WeekYear - PreviousWeeks
    if WeekYear > 52:
        Year += 1
        WeekYear -= 52

del YearDiff

print(datetime.strptime('%s %s %s' % (Year, WeekYear, DayWeek), '%G %V %u'))
