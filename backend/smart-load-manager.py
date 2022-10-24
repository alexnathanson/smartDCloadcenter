# smart DC load manager


'''
Data to store in advance
* regional insolation data
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
'''


