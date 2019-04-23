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

stationsToBeFiltered = set([3488, 3214, 3267, 3681, 3185, 3186])

stationToEventCountMap = {}
for stationID in stationIDSet: 
	stationToEventCountMap[stationID] = 0

for bikeID in bikeToEventMap:
	for event in bikeToEventMap[bikeID]:
		stationToEventCountMap[event['start_station_id']] += 1

with open('bikeStationEventCounts.csv', mode='w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    firstRow = ['stationID', 'EventCount'] 
    csv_writer.writerow(firstRow)
    for stationID in stationIDSet:
    	print(stationID)
    	nextRow = []
    	if stationID not in stationsToBeFiltered:
    		nextRow.append(stationID)
    		nextRow.append(stationToEventCountMap[stationID])
    	csv_writer.writerow(nextRow)











