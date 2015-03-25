from subprocess import call
import os
import time
import datetime
import StringIO
    

def diffString(date1, date2):
    return "From %s to %s total time: %s" % (date1, date2, date2-date1)

def getSleepWakeData():
    result = os.system('cp uptime.log uptime_temp.log')
    # result = os.system('pmset -g log | grep -e "Wake..CDNVA" -e "Software Sleep" -e "Idle Sleep: Using AC" >> uptime_temp.log')
    result = os.system('pmset -g log | grep -e "CET Wake " -e "CET Sleep " -e " Start " >> uptime_temp.log')    
    os.system('awk \'!a[$0]++\' uptime_temp.log > uptime.log')
    return result

def t2s(date):
    if isinstance(date, datetime.datetime):
        return "%02d:%02d:%02d" % (date.hour, date .minute, date.second)
    if isinstance(date, datetime.timedelta):
        return str(date)

    return ""

def getDiffs(l):
    return map(lambda x:x[1]-x[0], l)

def breaksString(daybreaks):
    s = "s: " #streaks
    for d1, d2 in daybreaks[::2]:
        s += "%s, " % (str(d2-d1)) 
    s += "b: "
    for d1, d2 in daybreaks[1::2]:
        s += "%s, " % (str(d2-d1)) 

    return s[:-2]   

getSleepWakeData()

dates = set()
f = open("uptime.log", "r")
for line in f.readlines():
    elements = line.split(' ')
    dateString = elements[0] + " "+ elements[1]
    # date = datetime.datetime.strptime(dateString, '%d/%m/%y %H:%M:%S')
    if len(dateString) < 2:
        continue
    date = datetime.datetime.strptime(dateString, '%d.%m.%Y, %H:%M:%S')    
    # date.
    dates.add(date)
f.close()

dates = sorted(list(dates))

# day
first = dates[0]
last = dates[0]
pairs = []


# breaks
breaks = []
day_breaks = [dates[0]]

for d in dates:
    # print first, last, d
    if d.day != last.day:
        pairs.append([first, last])
        breaks.append(day_breaks)

        print diffString(first, last), "|", breaksString(zip(day_breaks[:-1], day_breaks[1:]))
        first = d
        last = d
        day_breaks = [d]
    else:
        last = d
        day_breaks.append(d)

print diffString(first, last), "|", breaksString(zip(day_breaks[:-1], day_breaks[1:]))

diffs = getDiffs(pairs)

total = diffs[0]
count = 0

for d in diffs:
    # print d
    # ignore periods shorter than 10s
    if d.seconds < 10:
        print "Skip: ", d
        continue

    total = total + d
    count = count + 1
print "Total time spent: %s in %d days" % (str(total), count)
print "Average per day: ", total / count

left = first+datetime.timedelta(0, 8.5 * 3600)
print "Suggested time for last: %s (%s left)" % (t2s(left), t2s(left - datetime.datetime.now()))