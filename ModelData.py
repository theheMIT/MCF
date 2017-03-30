import csv
import json
import os.path

if __name__ == '__main__':

    with open('dataDir.json') as dataFile:
        dataDirFile = json.load(dataFile)

    dataDir = os.path.normpath(dataDirFile['dataDir'])  # data directory should be MCF Dropbox

    # set different output directory, so that temporary files do not upload to MCF Dropbox
    dataOutDir = os.path.normpath(dataDirFile['dataOutDir'])

    with open('FMSStops_net_mtz_timeline.json') as tl:
        timeLines = json.load(tl)

    with open('FMSStops_net_mtz_alternatives.json') as alt:
        alternatives = json.load(alt)

    with open('PostalCode_BE_measures_clusters.csv') as be:
        beMeasures = csv.reader(be)
        beLookUp = {row[0]: row for row in beMeasures}

    kIndex = beLookUp['postcode'].index('Kmeans_clust')
    lcaIndex = beLookUp['postcode'].index('LCA_clust')

    entries = []
    ID = 0

    for user in range(len(timeLines)):
        usChar = timeLines[user]['userCharacteristics']
        for episode in timeLines[user]['activities']:
            if episode['activityType'] == 'travel':

                # Determine trip purpose
                currentIndex = timeLines[user]['activities'].indexof(episode)
                purposeFound = False
                tripPurpose = ''
                for downstreamEpisode in timeLines[user]['activities'][currentIndex:]:
                    if episode['stopID'] == downstreamEpisode['stopID']:
                        tripPurpose = downstreamEpisode['activity']
                        purposeFound = True
                if not purposeFound:
                    tripPurpose = 'Not Found'

                # Create entry
                entries.append([ID, user['userID'], episode['activity'], tripPurpose, episode['startDay'],
                                episode['startTime'], episode['endTime'], episode['postalCodePrev'],
                                beLookUp[episode['postalCodePrev'][kIndex]],
                                beLookUp[episode['postalCodePrev'][lcaIndex]], episode['postalCode'],
                                beLookUp[episode['postalCode'][kIndex]], beLookUp[episode['postalCode'][lcaIndex]],
                                usChar['H2_DwellingType'], usChar['H3_Ethnic'], usChar['H4_TotalPax'],
                                usChar['H5_VehAvailable'], usChar['H8_BikeQty'], usChar['P1_Age'], usChar['P2_Gender'],
                                usChar['P3c_NoLicense'], usChar['P5_Employ'], usChar['P6Industry'], usChar['P6_Occup'],
                                usChar['P7_WorkHrs']])

                ID += 1

    with open('data.csv', 'w') as data:
        try:
            writer = csv.writer(data)
            writer.writerow(('ID', 'userID', 'mode', 'tripPurpose', 'startDay', 'startTime', 'endTime', 'postalCode',
                             'postalCodePrev', 'carTT', 'carCost', 'carEmission', 'mrtTT', 'mrtCost', 'mrtEmission',
                             'busTT', 'busCost', 'busEmission', 'walkTT', 'walkCost', 'walkEmission', 'oPostCode',
                             'oKCluster', 'oLCACluster', 'dPostCode', 'dKCluster', 'dLCACluster', 'dwellingType',
                             'ethnicity', 'HHSize', 'vehicles', 'bikes', 'age', 'gender', 'noLicense', 'employed',
                             'industry', 'occupation', 'workHrs'))  # Header row
            for row in range(len(entries)):
                writer.writerow(entries[row])  # Data rows

        finally:
            data.close
    dataFile.close()
    tl.close()
    alt.close()




