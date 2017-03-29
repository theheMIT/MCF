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

                # Create trip information
                origin = str(episode['latPrev']) + ',' + str(episode['lonPrev'])
                destination = str(episode['lat']) + ',' + str(episode['lon'])

                # Create entry
                entries.append([ID, user['userID'], episode['activity'], tripPurpose, episode['startDay'],
                                episode['startTime'], episode['endTime'], episode['postCodePrev'],
                                beLookUp[episode['postCodePrev'][kIndex]], beLookUp[episode['postCodePrev'][lcaIndex]],
                                episode['postCode'], beLookUp[episode['postCode'][kIndex]],
                                beLookUp[episode['postCode'][lcaIndex]], episode['emissionsKg']])

                # Associate with socio-demographic variables

                ID += 1

    with open('data.csv', 'w') as data:
        try:
            writer = csv.writer(data)
            writer.writerow(('ID', 'userID', 'mode', 'tripPurpose', 'startDay', 'startTime', 'endTime', 'postalCode',
                             'postalCodePrev', 'carTT', 'carCost', 'carEmission', 'mrtTT', 'mrtCost', 'mrtEmission',
                             'busTT', 'busCost', 'busEmission', 'walkTT', 'walkCost', 'walkEmission', 'emissionsKg',
                             'oPostCode', 'oKCluster', 'oLCACluster', 'dPostCode', 'dKCluster', 'dLCACluster'))  # Header row
            for row in range(len(entries)):
                writer.writerow(entries[row])  # Data rows

        finally:
            data.close
    dataFile.close()
    tl.close()
    alt.close()




