import csv
import sys, time, datetime
import json

# Index's for items in the CSV file
bikeID_index = 11
startTime_index = 1
stopTime_index = 2
startStationID_index = 3
endStationID_index = 7

month = 4

def waitingAnimation(n, line, total_lines):
	n = line%4
	charList = list('-\|/')     
	sys.stdout.write('\r Processing:\t'+  f'{line}/{total_lines} ' + charList[n] )
	sys.stdout.flush()
	
bikeToEventMap = {}

stationIDSet = set()

print(" Opening 201804-citibike-tripdata.csv ...")
print(" Counting rows in csv file ...")

# Count Lines in CSV file
with open('201804-citibike-tripdata.csv') as csv_file:
	total_lines = sum(1 for row in csv_file) - 1

# Extract all trips for a certain bike
with open('201804-citibike-tripdata.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0
	print(" Beginning to process data...")
	for row in csv_reader:
		waitingAnimation(line_count, line_count, total_lines)
		if line_count == 0:
			line_count += 1
		else:
			bikeID = row[bikeID_index]
			start_time, end_time = row[startTime_index], row[stopTime_index]
			
			# Process start_time from string to datetime object

			start_date_time = start_time.split(" ")
			start_date = start_date_time[0]
			start_time = start_date_time[1]
			start_date_list = start_date.split("-")
			start_time_list = start_time.split(":")
			start_year, start_month, start_day = int(start_date_list[0]), int(start_date_list[1]), int(start_date_list[2])
			start_hour, start_minute, start_second = int(start_time_list[0]), int(start_time_list[1]), int(float(start_time_list[2]))
			start_time = datetime.datetime(start_year, start_month, start_day, start_hour, start_minute, start_second)

			# Process end_time from string to datetime object
			end_date_time = end_time.split(" ")
			end_date = end_date_time[0]
			end_time = end_date_time[1]
			end_date_list = end_date.split("-")
			end_time_list = end_time.split(":")
			end_year, end_month, end_day = int(end_date_list[0]), int(end_date_list[1]), int(end_date_list[2])
			end_hour, end_minute, end_second = int(end_time_list[0]), int(end_time_list[1]), int(float(end_time_list[2]))
			end_time = datetime.datetime(end_year, end_month, end_day, end_hour, end_minute, end_second)

			startStationID = row[startStationID_index]
			endStationID = row[endStationID_index]

			if startStationID not in stationIDSet:
				stationIDSet.add(startStationID)

			if endStationID not in stationIDSet:
				stationIDSet.add(endStationID)

			event = {'start_time': start_time, 
						'stop_time': end_time, 
						'start_station_id': row[startStationID_index], 
						'end_station_id': row[endStationID_index]}
			if bikeID not in bikeToEventMap:
				bikeToEventMap[bikeID] = [event]
			else:
				bikeToEventMap[bikeID].append(event)
			line_count += 1
	print()


# Sort 
for bikeID in bikeToEventMap:
	bikeToEventMap[bikeID] = sorted(bikeToEventMap[bikeID], key = lambda i: i['start_time'])

#list of times in april for every 15 minutes
# change to 1 hour
"""
current_month_times = [datetime.datetime(2018, month, day, hour, minute) for day in range(1,31) 
					for hour in range(0,24) for minute in range(0,60,15)]
"""
current_month_times = [datetime.datetime(2018, month, day, hour) for day in range(1,31) 
					for hour in range(0,24)]
# create a lookUp with two keys (ID, time) -> numOfBikes
stationAndTimeToNumOfBikes = {}

for station in stationIDSet:
	for time in current_month_times:
		stationAndTimeToNumOfBikes[station, str(time)] = 0

def getIntervalsForTwoTimes(time1, time2, current_month_times):
	intervalsThatTime1Time2FallInto = []
	for time in current_month_times:
		if time1 < time and time2 > time:
			intervalsThatTime1Time2FallInto.append(time)
	return intervalsThatTime1Time2FallInto
# bikeToEventMap[bikeID] -> [event1, event2, event3...]
# event[i] and event[i+1] -> event[i][station] ->
# event[i][end_time], event[i+1][start_time] -> which 15 minute intervals it was at the station.


# Count how many event at a station for entire month station[id] = numOfevents per month
# hard code for the first and last times of the month.
count = 0 
totalEvents = 100000

bikeSeen = set()
# fix timing issue with bikes
for bikeID in bikeToEventMap:
	for i in range(len(bikeToEventMap[bikeID])-1):
		waitingAnimation(count, count, total_lines)
		time1 = bikeToEventMap[bikeID][i]['stop_time']
		time2 = bikeToEventMap[bikeID][i+1]['start_time']
		intervals = getIntervalsForTwoTimes(time1,time2, current_month_times)
		stationIDofBike = bikeToEventMap[bikeID][i]['start_station_id']
		for time in intervals:
			stationAndTimeToNumOfBikes[stationIDofBike, str(time)] += 1
		# get the station id from the 'stop_time' and add one for each interval.
		count += 1

stationsToBeFiltered = set([3488, 3214, 3267, 3681, 3185, 3186])
"""
with open('bikeStationCounts.csv', mode='w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    firstRow = [str(time) for time in current_month_times]
    firstRow= ['Station ID'] + firstRow
    csv_writer.writerow(firstRow)
    for stationID in stationIDSet:
    	if stationID not in stationsToBeFiltered: 
        	stationInfoLst = []
        	stationInfoLst.append(stationID)
        	for time in current_month_times:
        		stationInfoLst.append(stationAndTimeToNumOfBikes[stationID, str(time)])
        	csv_writer.writerow(stationInfoLst)
"""

with open('bikeStationCounts.csv', mode='w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    firstRow = [stationID for stationID in stationIDSet if stationID not in stationsToBeFiltered]
    firstRow = ['Time'] + firstRow
    csv_writer.writerow(firstRow)
    for time in current_month_times:
    	timeRow = [str(time)]
    	for stationID in stationIDSet:
    		if stationID not in stationsToBeFiltered:
    			timeRow.append(stationAndTimeToNumOfBikes[stationID, str(time)])
    	csv_writer.writerow(timeRow)


print(" Done")



