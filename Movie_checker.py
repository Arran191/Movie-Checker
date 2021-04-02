import urllib
import argparse
import datetime
import requests
from bs4 import BeautifulSoup


def find_platform(url):
    platforms = ["netflix", "disneyplus", "amazon"]
    results = [element for element in platforms if (element in url)]
    print(results)
    return results[0]


def check_movie(query):
    query = query.replace(' ', '+')
    URL = f"https://google.com/search?q={query}"
    print("Checking: " + URL)

    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent": USER_AGENT}
    resp = requests.get(URL, headers=headers)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")

    for g in soup.find_all('div', class_='fOYFme'):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            print(link)

    return link


def main(query):

    linkResults = check_movie(query)
    print("Link found: " + str(linkResults))
    if linkResults == None:
        print("No results")
    else:
        platform = find_platform(linkResults)
        print(platform)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('query', help='The search term to query')
    args = parser.parse_args()
    main(args.query)


"""
Sample result: https://kgsearch.googleapis.com/v1/entities:search?query=taylor+swift&key=[]&limit=1&indent=True
{
  "@context": {
    "@vocab": "http://schema.org/",
    "goog": "http://schema.googleapis.com/",
    "EntitySearchResult": "goog:EntitySearchResult",
    "detailedDescription": "goog:detailedDescription",
    "resultScore": "goog:resultScore",
    "kg": "http://g.co/kg"
  },
  "@type": "ItemList",
  "itemListElement": [
    {
      "@type": "EntitySearchResult",
      "result": {
        "@id": "kg:/m/0dl567",
        "name": "Taylor Swift",
        "@type": [
          "Thing",
          "Person"
        ],
        "description": "Singer-songwriter",
        "image": {
          "contentUrl": "http://t1.gstatic.com/images?q=tbn:ANd9GcQmVDAhjhWnN2OWys2ZMO3PGAhupp5tN2LwF_BJmiHgi19hf8Ku",
          "url": "https://en.wikipedia.org/wiki/Taylor_Swift",
          "license": "http://creativecommons.org/licenses/by-sa/2.0"
        },
        "detailedDescription": {
          "articleBody": "Taylor Alison Swift is an American singer-songwriter.
          Raised in Wyomissing, Pennsylvania, she moved to Nashville, Tennessee, at the age of 14
          to pursue a career in country music. ",
          "url": "http://en.wikipedia.org/wiki/Taylor_Swift",
          "license": "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License"
        },
        "url": "http://www.taylorswift.com/"
      },
      "resultScore": 884.364868
    }
  ]
}
"""
