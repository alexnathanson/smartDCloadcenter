# smart DC load manager

'''
User inputs: Load definition (critical/shedable & temporal flexibility), Device info (Lat, long)
Data inputs: realtime PV data, seasonal climate  data, weather forecast
Simple load management strategy
* Determine energy demand for ideal scenario
* Compare to predicted capacity
* Calculate energy distribution plan based on user identified priorities
* Exchange is based on seasonal weather patterns, day ahead weather reports, and live production projections.
'''

'''
Data to store in advance
* regional insolation data
* sun hours
* regional rain data

Data to collect
1) historic production data from CC
2) real-time data on power available + storage status (i.e. is curtailment happening)
3) historic load data (i.e. how much power is each load drawing and when)
4) user data about load priorities
	a) which are crucial loads and which are ideal loads
	b) which are time-independent/asyncronous and which are time specific


predict w/o weather forcast:
* estimate energy availability for that day
* runs async processes when energy is plentiful and curtailment is happenings

For each load:
Get power draw over time, determine patterns of activity

If internet i.e. weather forcasts are available:
* estimate energy availabilty for coming days

Can it factor in citing???
'''

import json
import requests
import datetime
# import io
# import pandas as pd
import pvlib

#this file just has a variable openweatherapi defined as the api key
from keys import *

#this should be set by users via interface
lati = '40.7128'
longi = '-74.0060'

#watts
loadPowerDemand = 10

weatherCodeFile = 'data/openweathercodes.json'
epw = 'data/USA_NY_New.York-J.F.Kennedy.Intl.AP.744860_TMY3.epw'

# 1) get PV data
def getPVData():
	#get battery percentage
	try:
		gPvData = json.loads(getRequest("http://solarprotocol.net/api/v2/opendata.php?line=0"))
		#print(pvData['0'])
		return gPvData['0']
	except Exception as err:
		print(err)

# 2) get user inputs

# 3) get 8 day ahead weather report (starting with today's forecast)
# API documentation https://openweathermap.org/forecast5
def getWeatherReport(gWeatherCodeFile):
	
	gForecast = {}

	with open(gWeatherCodeFile, 'r') as c:
		gWeatherCodes = json.loads(c.read())
		#print(weatherCodes)

	try:
		weather = json.loads(getRequest("https://api.openweathermap.org/data/2.5/onecall?lat=" + lati +"&lon=" + longi + "&exclude=minutely,alerts&appid=" + openweatherapi))
		#print('')
		#print(weather)
		#print('')
		#eight day weather
		#switch to hourly at some point
		for d in weather['daily']:
			#print(d)
			date_time = datetime.datetime.fromtimestamp(d['dt'])  
			#print(date_time)
			dW = d['weather'][0]['id']
			#print(weatherCodes['codes'][str(dW)])
			#print(weatherCodes['codes'][str(dW)]['solar value'])
			gForecast[str(date_time)]= gWeatherCodes['codes'][str(dW)]['solar value']
		#print(eightDayWeather)
	except Exception as err:
		print(err)
		#historical weather data
		#weather =

	return gForecast

# 4) get sun hours via EPW
# examples: https://pvsc-python-tutorials.github.io/pyData-2021-Solar-PV-Modeling/Tutorial%201%20-%20TMY%20Weather%20Data.html
#this uses the pvlib library https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.iotools.read_epw.html?highlight=epw
# more reference: https://github.com/ladybug-tools/ladybug-legacy/tree/master/src

#returns typical sun hours for the next 8 days
def getSunHours(gEpw):

	gSunHours = {}

	df_epw, meta_dict = pvlib.iotools.read_epw(gEpw, coerce_year=datetime.datetime.now().year)

	#ghi is Direct and diffuse horizontal radiation recv’d during 60 minutes prior to timestamp, Wh/m^2
	print(df_epw.iloc[0]['ghi'])
	for i in range(8):
		day = datetime.datetime.now() + datetime.timedelta(days=i)
		print(day.day)

		#filter by day
		dayData = df_epw.loc[df_epw.index.day == day.day]
		dayData = dayData.loc[dayData.index.month == day.month]
		# print(len(dayData))
		# print(dayData)
		# print('')

		#filter by ghi value
		dayGhiData = dayData.loc[dayData['ghi'] > 200]
		#print(len(dayGhiData))
		#print(len(dayGhiData))

		gSunHours [str(day)] = len(dayGhiData)

	return gSunHours

 	#print(df_epw)

	return gSunHours
#  estimate run time

# calculate possible plans

def getRequest(url):
	try:			
		response = requests.get(url)
		return response.text	
	except requests.exceptions.HTTPError as err:
		print(err)
	except requests.exceptions.Timeout as err:
		print(err)
	except:
		print(err)

if __name__ == '__main__':
	'''
 	#todays date
 	print(datetime.datetime.now().year)

 	print('')
 	pvData = getPVData()
 	print(pvData)
 	print('')

 	forecast = getWeatherReport(weatherCodeFile)
 	print(forecast)
 	print('')
	'''
	sunHours = getSunHours(epw)
	print(sunHours)
	print('')