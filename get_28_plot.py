from matplotlib import pyplot as plt
from matplotlib.dates import DayLocator, DateFormatter
from numpy import arange
import json
import datetime
import dateutil


def draw_plot(x, y, distance):
	fig, ax = plt.subplots()
	ax.plot_date(x, y, 'r-')
	ax.set_xlim( x[0], x[-1] )

	ax.xaxis.set_major_locator( DayLocator(interval = distance) )
	ax.xaxis.set_major_formatter( DateFormatter('%d.%m.%Y') )
	fig.autofmt_xdate()

	plt.ylabel('amount')
	plt.xlabel('datetime')
	plt.grid(True)

	plt.show()

def as_point(dct):
	return [dateutil.parser.parse(dct['datetime']), dct['amount']]

def show_28_progress(distance=2):
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
