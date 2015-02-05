from matplotlib import pyplot as plt
from matplotlib.dates import DayLocator, DateFormatter
from numpy import arange
import json
import datetime
import dateutil


def draw_plot(x, y, distance):
    fig, (ax1, ax2) = plt.subplots(2, 1, True)
    ax1.plot_date(x, y, 'r-')
    ax1.set_xlim( x[0], x[-1] )

    ax1.xaxis.set_major_locator( DayLocator(interval = distance) )
    ax1.xaxis.set_major_formatter( DateFormatter('%d.%m.%Y') )
    fig.autofmt_xdate()

    all_diffs = [int(t[0]) - int(t[1]) for t in zip(y, [y[0]]+y[:-1])]

    last_day = x[0]
    daily_diffs = [0]
    just_days = [datetime.datetime(x[0].year, x[0].month, x[0].day)]

    for pair in list(zip(x, all_diffs)):
        aligned_day = datetime.datetime(pair[0].year, pair[0].month, pair[0].day) + datetime.timedelta(days=1)
        if (aligned_day - last_day) < datetime.timedelta(days=1):
            daily_diffs[-1] = daily_diffs[-1] + pair[1]
        else:
            past_days = (aligned_day - last_day).days
            avg_amount = pair[1] / past_days

            for i in range(0, past_days):
                daily_diffs.append(avg_amount)
                just_days.append(just_days[-1] + datetime.timedelta(days=1))

            last_day = aligned_day

    ax2.bar(just_days, daily_diffs)

    ax1.set_ylabel('amount')
    ax2.set_ylabel('daily donation')
    plt.xlabel('datetime')
    ax1.grid(True)
    ax2.grid(True)

    plt.show()

def as_point(dct):
    return [dateutil.parser.parse(dct['datetime']), dct['amount']]

def show_28_progress(distance=3):
    money_trace_data = open('/home/ramamba/Documents/28trace.json', 'r', encoding='utf-8')
    
    x = []
    y = []
 
    for line in money_trace_data:
        point = json.loads(line, object_hook = as_point)
        x.append(point[0])
        y.append(point[1])

    if distance <= 0:
        distance = 1

    draw_plot(x, y, distance)

if __name__ == '__main__':
    show_28_progress()
