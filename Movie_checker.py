import sys
import urllib
import argparse
import datetime
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from colorama import Fore, Back, Style, init
from urllib.parse import urlparse


def printProgressBar(
    iteration,
    total,
    prefix="",
    suffix="",
    decimals=1,
    length=100,
    fill="█",
    printEnd="\r",
):

    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + "-" * (length - filledLength)
    print(Style.RESET_ALL + f"\r{prefix} |{bar}|{percent}% {suffix}", end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def strip_url(url):
    domainURL = urlparse(url).netloc
    domainURL = domainURL.replace('www.', '')
    #print(domainURL)
    domainURL = domainURL.split(".",1)
    #print(test)
    return domainURL[0]
    

def find_platform(url):
    #platforms = ["netflix", "disneyplus", "amazon", "youtube", "play.google", "prime_premium", "bbc", "channel4"]
    #print("URLS" + url)
    url = url.lower()
    
    if url == "paid" or url == "no results":
        return url
    
    striped_url = str(strip_url(url))
   #print("Strips" +striped_url + " "+  str(type(striped_url)))
   
    if striped_url == 'amazon':
        return "prime"
    elif striped_url == "channel4":
        return "channel 4"
    elif striped_url == "bbc":
        return "iplayer"
    elif striped_url == "disneyplus":
        return "disney+"

    return striped_url
    #results = [element for element in platforms if (element in url)]

def getAmazonPreimum(URL):
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    resp = requests.get(URL, headers=headers).text 
    soup = BeautifulSoup(resp, 'lxml') 
    #print(resp)
    for g in soup.find_all("div", class_="fOYFme"):
         anchors = g.find_all("span")
   
         print(anchors)
        # checkPaid = soup.select('.uiBRm')
        #checkPaid = g.find("div", {"class": "uiBRm"})
        

def check_movie(query, year="movie"):
    query = query.replace(" ", "+")
    URL = f"https://google.com/search?q={query}+{year}"
    #print("Checking: " + URL)

    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent": USER_AGENT}
    resp = requests.get(URL, headers=headers)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")

    for g in soup.find_all("div", class_="fOYFme"):
        anchors = g.find_all("a")
        # checkPaid = soup.select('.uiBRm')
        checkPaid = g.find("div", {"class": "uiBRm"})
        # print("Checkpaid" + str(checkPaid))
        if anchors and checkPaid:
            # Checks if it is a premium subscription that prime has. 
            if checkPaid.text.find("Subscription"):
                #print(f"{query} Paid movie {checkPaid.text}")
                if(checkPaid.text == "Premium subscription"):
                   getAmazonPreimum(anchors[0]['href'])
                   print(f"{query} Paid movie {checkPaid.text}")
                   
                if checkPaid.text == "Free":
                    return anchors[0]['href']
                    # domainURL = urlparse().netloc
                    # domainURL = domainURL.replace('www.', ' ')
                    # print(f"{query} from {domainURL}")
                    # return (domainURL)                             
                return "paid"
            else:
               # print(f"{query} Subscribed movie {checkPaid.text}")
                return anchors[0]["href"]

    return "No results"


def check_csv_list(compare=False, ignore=False):
    df = pd.read_csv("WatchingList.csv")
    length = len(df)
    for index, movie in df.Name.iteritems():
        # filledLength = int(50 - (index + 1) // length)
        printProgressBar(
            index + 1, length, prefix="Progress:", suffix="Complete", length=50
        )

        # Ignore the movie if already watched.
        if (
            df.Status[index] == "Complete"
            or df.Location[index] == "Tom-Paid"
        ):
            continue

        year = int(df.Year[index])
        linkResults = check_movie(movie, year)
        platform = find_platform(linkResults)
        sentence = ""

        if compare == False and platform != "no results":
            sentence = f"{movie} can be viewed on {platform.upper()}"

        if str(df.Location[index]).lower() != platform:
            if platform == "no results" and ignore == False:
                sentence = (Fore.RED + f"{movie} {year} has {platform.upper()}")
            elif platform != "no results":
                sentence = (
                    Fore.GREEN
                    + f"{movie} {year} has changed from {df.Location[index]} to {platform.upper()}"
                )
        if sentence != "":
            bar = "-" * (60 - len(sentence))
            print(sentence + Fore.RESET + bar + "\r")


def main(query, readcsv, isolate, ignore):

    if readcsv == True:
        check_csv_list(isolate, ignore)
    else:
        linkResults = check_movie(query)
        platform = find_platform(linkResults)
        print(f"'{query}' can be viewed on {platform.upper()}")

        # print("Link found: " + str(linkResults))


# For command line.
def str2bool(value):
    if value.lower() in {"false", "f", "0", "no", "n"}:
        return False
    elif value.lower() in {"true", "t", "1", "yes", "y"}:
        return True
    raise ValueError(f"{value} is not a valid boolean value")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prefix_chars="-")
    parser.add_argument(
        "-csv",
        help="Pass in false to ignore CSV file",
        type=str2bool,
        default=True,
    )
    parser.add_argument(
        "-q",
        help="The search term to query if you are not reading from the CSV",
        default="",
    )
    parser.add_argument(
        "-o", help="Only show movies that have changed.", type=str2bool, default=False
    )
    parser.add_argument("-i", help="Ignore no results", type=str2bool, default=False)
    args = parser.parse_args()
    init()
    main(args.q, args.csv, args.o, args.i)
