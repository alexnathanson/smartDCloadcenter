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
import pandas as pd
import pvlib

#this file just has a variable openweatherapi defined as the api key
from keys import *

#this should be set by users via interface
lati = '40.7128'
longi = '-74.0060'

#watts
arraySize = 100


weatherCodeFile = 'data/openweathercodes.json'
epw = 'data/USA_NY_New.York-J.F.Kennedy.Intl.AP.744860_TMY3.epw'

#energy demand (w)
energyDemand = {1:{'load':12, 'rt':12, 'pr': 1.0},
				2:{'load':20,'rt':5,'pr':0.5},
				3:{'load':5,'rt':10,'pr':0.6}}

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
# returns a solar correction factor
# API documentation https://openweathermap.org/forecast5
def getWeatherReport(gWeatherCodeFile):
	
	gForecast = {}

	with open(gWeatherCodeFile, 'r') as c:
		gWeatherCodes = json.loads(c.read())
		#print(weatherCodes)

	try:
		weather = json.loads(getRequest("https://api.openweathermap.org/data/2.5/onecall?lat=" + lati +"&lon=" + longi + "&exclude=minutely,hourly,alerts&appid=" + openweatherapi))
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
			#gForecast[str(date_time)]= dW
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
def getSunHours(df_epw):

	gSunHours = {}

	#df_epw, meta_dict = pvlib.iotools.read_epw(gEpw, coerce_year=datetime.datetime.now().year)

	#ghi is Direct and diffuse horizontal radiation recv’d during 60 minutes prior to timestamp, Wh/m^2
	#print(df_epw.iloc[0]['ghi'])
	for i in range(8):
		day = datetime.datetime.now() + datetime.timedelta(days=i)
		#print(day.day)

		#filter by day
		dayData = df_epw.loc[df_epw.index.day == day.day]
		dayData = dayData.loc[dayData.index.month == day.month]
		# print(len(dayData))
		# print(dayData)
		# print('')

		#filter by ghi value
		dayGhiData = dayData.loc[dayData['ghi'] > 300]
		#print(len(dayGhiData))
		#print(len(dayGhiData))

		#if len(dayGhiData) > 0:
		gSunHours [str(day)] = len(dayGhiData)

	return gSunHours

	#print(df_epw)

	return gSunHours



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

def runPrediction(iC):
	print('')
	pvData = getPVData()
	print(pvData)
	print('')

	if iC:
		#returns solar correction factor
		forecast = getWeatherReport(weatherCodeFile)
		print('forecast')
		print(forecast)
		print('')

	df_epw, meta_dict = pvlib.iotools.read_epw(epw, coerce_year=datetime.datetime.now().year)

	modelPOA(df_epw, meta_dict)

	# returns amount of hours
	sunHours = getSunHours(df_epw)
	print(sunHours)
	print('')

	#tomorrows prediction
	pvDerating = (forecast[list(forecast.keys())[1]]) * 0.01
	sH = sunHours[list(sunHours.keys())[1]]
	predictedOutput = arraySize * pvDerating * sH
	print(str(predictedOutput) + ' watts')

	loadControl(energyDemand, predictedOutput)

#source: https://pvsc-python-tutorials.github.io/pyData-2021-Solar-PV-Modeling/Tutorial%202%20-%20POA%20Irradiance.html
def modelPOA(data, metadata):
	# make a Location object corresponding to this TMY
	location = pvlib.location.Location(latitude=metadata['latitude'],
	                                   longitude=metadata['longitude'])

	print(location)

	# Note: TMY datasets are right-labeled hourly intervals, e.g. the
	# 10AM to 11AM interval is labeled 11.  We should calculate solar position in
	# the middle of the interval (10:30), so we subtract 30 minutes:
	times = data.index - pd.Timedelta('30min')

	solar_position = location.get_solarposition(times)
	# but remember to shift the index back to line up with the TMY data:
	solar_position.index += pd.Timedelta('30min')

	# print(solar_position.head())

	#fixed tilt POA
	df_poa = pvlib.irradiance.get_total_irradiance(
	    surface_tilt=20,  # tilted 20 degrees from horizontal
	    surface_azimuth=180,  # facing South
	    dni=data['dni'],
	    ghi=data['ghi'],
	    dhi=data['dhi'],
	    solar_zenith=solar_position['apparent_zenith'],
	    solar_azimuth=solar_position['azimuth'],
	    model='isotropic')

	print(df_poa.head())

#  estimate run time
# returns 1 if ideals
def loadControl(loadData, supplyData):
	print(loadData)
	#for l in loadData:
	#	totEnergyDemand = totEnergyDemand + (loadData[l]['load'] * loadData[l]['rt'] )

	totEnergyDemand = getEnergyDemand(loadData, 0.0)
	print(totEnergyDemand)

	# calculate possible plans

	#check if ideal
	if(totEnergyDemand <= supplyData):
		print(True)
		return 1
	#check if priority loads can run
	elif (getEnergyDemand(loadData, 1.0) <= supplyData):
		return 2
		
def getEnergyDemand(loadData, thresh):
	totEnergyDemand = 0
	for l in loadData:
		print(loadData[l]['pr'])
		if loadData[l]['pr'] >= thresh:
			totEnergyDemand = totEnergyDemand + (loadData[l]['load'] * loadData[l]['rt'] )

	return totEnergyDemand

def checkInternet(host='http://google.com'):
	try:
		response = requests.get(host)
		#urllib.request.urlopen(host) #Python 3.x
		return True
	except:
		return False

def postJSON(dstData):
    try:
        headers = {'Content-type': 'application/json'}
        x = requests.post('http://localhost:5000/api', headers=headers,json = dstData, timeout=5)
        # if x.ok:
        #     try:
        #         print("Post successful")
        #     except:
        #         print("Malformatted response")
        #         print(x.text)
        #requests.raise_for_status()
    except json.decoder.JSONDecodeError as e:
        print("JSON decoding error", e)
    except requests.exceptions.HTTPError as errh:
        print("An Http Error occurred:" + repr(errh))
    except requests.exceptions.ConnectionError as errc:
        print("An Error Connecting to the API occurred:" + repr(errc))
    except requests.exceptions.Timeout as errt:
        print("A Timeout Error occurred:" + repr(errt))
    except requests.exceptions.RequestException as err:
        print("An Unknown Error occurred" + repr(err))

def setup():
	print( "connected" if checkInternet() else "no internet!" )

if __name__ == '__main__':

	#setup()
	internetConnection = checkInternet()
	print( "connected" if internetConnection else "no internet!" )

	runPrediction(internetConnection)
 