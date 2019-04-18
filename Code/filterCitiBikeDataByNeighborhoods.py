"""
map : stationID -> [[pointInTime]...] via allStatsCount.csv
map : Neighborhood -> [stations] via  bikeStationLongLat.csv
map : station ID -> (longitude, latitude) via bikeStationLongLat.csv

for neigborhood in neighborhoods:
	1. create CSV
	2. iterate

"""
import csv, sys

stationIDtoListOfPointsInTime = {}
neighborhoodToStations = {}
stationIDToLongLat = {}

def waitingAnimation(line, total_lines):
	n = line%4
	charList = list('-\|/')     
	sys.stdout.write('\r Processing:\t'+  f'{line}/{total_lines} ' + charList[n] )
	sys.stdout.flush()

print(" Opening allstats_count.csv ...")
print(" Counting rows in csv file ...")

# Count Lines in CSV file
with open('allstats_count.csv') as csv_file:
	total_lines = sum(1 for row in csv_file) - 1

#print(" %d" % (total_lines))

stationIDtoListOfPointsInTime = {}

with open('allstats_count.csv') as csv_file:
	
	stationID_index = 0
	type_index = 1
	time_index = 2
	value_index = 3

	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0

	print(" Beginning to process data...")
	for row in csv_reader:
		waitingAnimation(line_count, total_lines)
		if line_count == 0: 
			line_count += 1
		else:
			stationID = row[stationID_index]
			if stationID not in stationIDtoListOfPointsInTime:
				stationIDtoListOfPointsInTime[stationID] = []
			currPointInTime = {'type': row[type_index], 'time': row[time_index], 'val': row[value_index]}
			stationIDtoListOfPointsInTime[stationID].append(currPointInTime)
			line_count += 1

print(" Opening bikeStationLongLat.csv ...")
print(" Counting rows in csv file ...")

# Count Lines in CSV file
with open('bikeStationLongLat.csv') as csv_file:
	total_lines = sum(1 for row in csv_file) - 1

with open('bikeStationLongLat.csv') as csv_file:
	
	neigborhood_index = 0
	stationID_index = 1
	stationName_index = 2
	latitude_index = 3
	longitude_index = 4
	eventCount_index = 5


	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0

	print(" Beginning to process data...")
	for row in csv_reader:
		waitingAnimation(line_count, total_lines)
		if line_count == 0:
			line_count += 1
		else:
			neigborhood = row[neigborhood_index]
			if neigborhood not in neighborhoodToStations:
				neighborhoodToStations[neigborhood] = set()
			stationID = row[stationID_index]
			neighborhoodToStations[neigborhood].add(stationID)

			if stationID not in stationIDToLongLat:
				longitude = row[longitude_index]
				latitude = row[latitude_index]
				stationIDToLongLat[stationID] = (latitude, longitude)
			line_count += 1
print("")
for neigborhood in neighborhoodToStations:
	csvName = neigborhood.replace(' ', '')
	folderPath = 'neighborhoodCSVs'
	fullCsvNameWithPath = f'{folderPath}/{csvName}.csv'
	print(f' Creating {csvName}...')
	with open(fullCsvNameWithPath, mode='w') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		firstRow = ['StationID', 'latitude', 'longitude', 'types', 'time', 'value',] 
		csv_writer.writerow(firstRow)
		for stationID in neighborhoodToStations[neigborhood]:
			nextRow = []
			if stationID not in stationIDtoListOfPointsInTime:
				nextRow.append(stationID)
				if stationID in stationIDToLongLat:
					nextRow.append(stationIDToLongLat[stationID][0])
					nextRow.append(stationIDToLongLat[stationID][1])
				else:
					nextRow.append('')
					nextRow.append('')
				nextRow.append('')
				nextRow.append('')
				nextRow.append('')
				csv_writer.writerow(nextRow)
				nextRow = []
			else:
				for pointInTime in stationIDtoListOfPointsInTime[stationID]:
					nextRow.append(stationID)
					if stationID in stationIDToLongLat:
						nextRow.append(stationIDToLongLat[stationID][0])
						nextRow.append(stationIDToLongLat[stationID][1])
					else:
						nextRow.append('')
						nextRow.append('')
					nextRow.append(pointInTime['type'])
					nextRow.append(pointInTime['time'])
					nextRow.append(pointInTime['val'])
					csv_writer.writerow(nextRow)
					nextRow = []
	print(f' Finished {csvName}')
	print(" -")
print(" Done")


			