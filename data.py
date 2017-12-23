import datetime
import urllib2
import json
import pandas as pd

def _parse(date):
		mmddyy = date.split("/")
		return datetime.date(month=int(mmddyy[0]), day=int(mmddyy[1]), year=int(mmddyy[2]))

def load_csv(filepath):
	df = pd.read_csv(filepath, 
					names=['time', '', 'value'], 
					usecols=[0,2], 
					header=0,
					converters={"time": _parse})
	df.set_index("time",inplace=True)
	#remove NaNs/check for NaNs
	return df 
