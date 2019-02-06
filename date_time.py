import datetime

# t = datetime.time(h,m,s,ms)
t = datetime.time(10, 40, 59)
print(t)
print(t.hour)
print(t.minute)
print(t.second)
print(t.microsecond)
print(t.tzinfo)

today = datetime.date.today()
print(today)

print(today.timetuple())
print(today.month)
