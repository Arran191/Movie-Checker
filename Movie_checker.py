import urllib
import argparse
import datetime
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd


def find_platform(url):
    platforms = ["netflix", "disneyplus", "amazon", "youtube"]
    results = [element for element in platforms if (element in url)]
    # print(results)
    if results:
        return results[0]
    else:
        return "No results"


def check_movie(query):
    query = query.replace(' ', '+')
    URL = f"https://google.com/search?q={query}"
    #print("Checking: " + URL)

    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent": USER_AGENT}
    resp = requests.get(URL, headers=headers)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")

    for g in soup.find_all('div', class_='fOYFme'):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            # print(link)
    return link


def check_csv_list(compare=False):
    df = pd.read_csv('WatchingList.csv')
    for index, movie in df.Name.iteritems():
        linkResults = check_movie(movie)
        platform = find_platform(linkResults)

        if str(df.Location[index]).lower() != platform:
            print(
                f"{movie} has changed from {df.Location[index]} to {platform}")

        if compare == False:
            print(f"{movie} can be viewed on {platform}")


def main(query, readcsv, isolate):
    if readcsv == True:
        check_csv_list(isolate)
    else:
        linkResults = check_movie(query)
        platform = find_platform(linkResults)
        print(f"{movie} can be viewed on {platform}")

    #print("Link found: " + str(linkResults))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-csv', help='Pass in bool value if you want to read the csv', type=bool, required=True)
    parser.add_argument(
        '-q', help='The search term to query if you are not reading from the CSV', default="")
    parser.add_argument(
        '-o', help='Only show movies that have changed.', type=bool, required=True)
    args = parser.parse_args()
    main(args.q, args.csv, args.o)
