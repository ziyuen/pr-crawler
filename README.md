# pr-crawler

A web crawler designated to crawl pull requests(PR) for the same issue from a given Github project. 

## How to run the crawler?

First, you should have [MongoDB](https://www.mongodb.com/docs/manual/installation/) and [Scrapy](https://docs.scrapy.org/en/latest/intro/install.html) installed. MongoDB is the default storage for the scraped contents. If you want to use other ways for storage, please check the [wiki](https://github.com/ziyuen/pr-crawler/wiki/Overview).

Run mongoDB from the terminal

```properties
mongod
```

Then you can run the spider

```properties
scrapy crawl githubPR
```

## How to customize the crawler?

Please check the [wiki](https://github.com/ziyuen/pr-crawler/wiki/Overview).
