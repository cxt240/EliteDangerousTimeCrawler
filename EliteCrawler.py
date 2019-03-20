import csv
import DataTransform
import datetime
import os.path
import time
import urllib.request

filename = 'history.csv'
findStartString = "it will take <strong>"
findEndString = "days</strong>"


def Load():
    history = {}
    if os.path.isfile(filename):
        # read and parse the history.csv file
        with open(filename, newline='') as csvfile:
            output = csv.reader(csvfile, delimiter=',', quotechar='|')
            history = list(output)
    return history


def Add(years, months, days):
    print("Years: ", years)
    print("Months: ", months)
    print("Days: ", days)

    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow([datetime.date.today(), years, months, days, DataTransform.TransformYears(years, months, days)])


# parses through the csv file and gets the last entry's
# date (we append to end for the latest)
def LatestEntry(csvData):
    latest = datetime.MINYEAR
    for entry in csvData:
        # logically, we append to end, so the last is the latest
        if len(entry):
            latest = entry[0]
    return latest


def ScrapeLatest():
    fp = urllib.request.urlopen("https://edsm.net")
    page = fp.read().decode("utf8")
    fp.close()
    startIndex = page.find(findStartString)
    endIndex = page.find(findEndString)

    return page[(startIndex + len(findStartString)):endIndex]


def main():
    content = Load()
    latestDate = LatestEntry(content)
    print("Latest: ", latestDate)

    while True:
        # blank csv file with no valid data
        if latestDate != str(datetime.date.today()):
            print("Updating Date and time to completion")
            latestDate = datetime.date.today()

            # format: # year # month #
            timeString = ScrapeLatest().replace(',', '').split(' ')

            Add(timeString[0], timeString[2], timeString[4])
            latestDate = datetime.date.today()
        print("Up to date. Sleeping for 2h")
        time.sleep(7200)
    return


if __name__ == "__main__":
    main()
