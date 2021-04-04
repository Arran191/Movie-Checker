import sys
import urllib
import argparse
import datetime
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os


def find_platform(url):
    platforms = ["netflix", "disneyplus", "amazon", "youtube", "play.google"]
    #print("URLS" + url)
    results = [element for element in platforms if (element in url)]

    if results:
        if results[0] == "youtube" or results[0] == "play.google":
            results[0] = "paid"
        elif results[0] == "amazon":
            results[0] = "prime"
        elif results[0] == "disneyplus":
            results[0] = "disney+"

        return results[0]
    elif url == "paid":
        return "paid"
    else:
        return "no results"


def check_movie(query, year):
    query = query.replace(' ', '+')
    URL = f"https://google.com/search?q={query}+{year}"
    #print("Checking: " + URL)

    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent": USER_AGENT}
    resp = requests.get(URL, headers=headers)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")

    for g in soup.find_all('div', class_='fOYFme'):
        anchors = g.find_all('a')
        #checkPaid = soup.select('.uiBRm')
        checkPaid = g.find("div", {"class": "uiBRm"})
        #print("Checkpaid" + str(checkPaid))
        if anchors and checkPaid:
            if checkPaid.text.find("Subscription"):
                #print(f"{query} Paid movie {checkPaid.text}")
                return "paid"
            else:
                #print(f"{query} Subscribed movie {checkPaid.text}")
                return anchors[0]['href']

    return "No results"


def check_csv_list(compare=False):
    df = pd.read_csv('WatchingList.csv')
    for index, movie in df.Name.iteritems():

        # Ignore the movie if already watched.
        if df.Status[index] == "Complete" or df.Location[index] == "Shudder" or df.Location[index] == "Tom-Paid":
            continue

        year = int(df.Year[index])
        linkResults = check_movie(movie, year)
        platform = find_platform(linkResults)

        if compare == False:
            print(f"{movie} can be viewed on {platform}")

        if str(df.Location[index]).lower() != platform:
            if platform == "no results":
                print(f"{movie} {year} has {platform}")
            else:
                print(
                    os.system('color 4')
                    f"{movie} {year} has changed from {df.Location[index]} to {platform}")


def main(query, readcsv, isolate):

    if readcsv == True:
        check_csv_list(isolate)
    else:
        linkResults = check_movie(query)
        platform = find_platform(linkResults)
        print(f"'{query}' can be viewed on {platform.upper()}")

        # print("Link found: " + str(linkResults))


# For command line.
def str2bool(value):
    if value.lower() in {'false', 'f', '0', 'no', 'n'}:
        return False
    elif value.lower() in {'true', 't', '1', 'yes', 'y'}:
        return True
    raise ValueError(f'{value} is not a valid boolean value')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prefix_chars='-')
    parser.add_argument(
        '-csv', help='Pass in bool value if you want to read the csv', type=str2bool, default=True)
    parser.add_argument(
        '-q', help='The search term to query if you are not reading from the CSV', default="")
    parser.add_argument(
        '-o', help='Only show movies that have changed.', type=str2bool, default=False)
    args = parser.parse_args()

    main(args.q, args.csv, args.o)
