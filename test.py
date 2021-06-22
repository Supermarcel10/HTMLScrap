from datetime import datetime, timedelta
from calendar import monthrange

week = ['21', 'Jun', '2021']
rel = 10

if monthrange(int(week[2]), int(datetime.strptime(week[1], "%b").month))[1] >= int(week[0]) + rel:
    print(datetime.strptime("%s %s %s" % ((int(week[0]) + rel), week[1], week[2]), "%d %b %Y"))
else:
    print(datetime.strptime("%s %s %s" % ((int(week[0]) + rel) - monthrange(int(week[2]), int(datetime.strptime(week[1], "%b").month))[1], datetime.strptime(week[1], "%b").month + 1,
                                          week[2]), "%d %m %Y"))
