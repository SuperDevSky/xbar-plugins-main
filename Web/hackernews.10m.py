#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# <xbar.title>Hacker News</xbar.title>
# <xbar.version>v1.0.0</xbar.version>
# <xbar.author>Liam Scalzulli</xbar.author>
# <xbar.author.github>terror</xbar.author.github>
# <xbar.desc>View top Hacker News articles in your status bar!</xbar.desc>
# <xbar.image>https://i.imgur.com/rGZzrB0.png</xbar.image>
# <xbar.dependencies>python3, requests</xbar.dependencies>

import requests
from dataclasses import dataclass

static_type = "item"

live_types = {
    "topstories":  ("Top", "https://news.ycombinator.com/"),
    "newstories":  ("New", "https://news.ycombinator.com/newest"),
    "beststories": ("Best", "https://news.ycombinator.com/best"),
    "askstories":  ("Ask", "https://news.ycombinator.com/ask"),
    "showstories": ("Show", "https://news.ycombinator.com/show"),
    "jobstories":  ("Job", "https://news.ycombinator.com/jobs"),
}


@dataclass
class Article:
    id:    str
    title: str
    by:    str
    url:   str
    time:  str

    def __str__(self):
        return "{} by: {} | href={}".format(self.title, self.by, self.url)


class Client:
    def __init__(self, type):
        self.type = type

    def fetch_data(self):
        res, ret = (
            self.__ids_to_json(requests.get(self.__live_data(self.type)).json()[:10]),
            [],
        )

        for article in res:
            if not article:
                continue

            url = article["url"] if "url" in article else ""

            if self.type == "askstories":
                url = "https://news.ycombinator.com/item?id={}".format(article["id"])

            ret.append(
                Article(
                    article["id"],
                    article["title"],
                    article["by"],
                    url,
                    article["time"],
                )
            )

        return ret

    def __ids_to_json(self, data):
        return [requests.get(self.__static_data(id, static_type)).json() for id in data]

    def __live_data(self, type):
        return "https://hacker-news.firebaseio.com/v0/{}.json?print=pretty".format(type)

    def __static_data(self, id, type):
        return "https://hacker-news.firebaseio.com/v0/{}/{}.json?print=pretty".format(
            type, id
        )


def separator(level):
    return "{}".format("-" * level)


def main():
    print("Hacker News\n---")

    for type in live_types:
        client = Client(type)
        articles = client.fetch_data()

        print(live_types[type][0])
        for article in articles:
            print("{}{}".format(separator(2), article))

        print(separator(5))

        print(
            "{}Hacker News - {} Stories | href={}".format(
                separator(2), live_types[type][0], live_types[type][1]
            )
        )

    print(separator(3))
    print(
        "Hacker News - Front Page | href={}".format("https://news.ycombinator.com/news")
    )


if __name__ == "__main__":
    main()
