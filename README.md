second-spider
=============

Another spider, powered by gevent,requests,pyquery 

### Features

1. The concurrency foundation on [gevent](http://www.gevent.org/)
2. The spider strategy highly configurable:

> 
* max depth 
* the count of urls you want fetch 
* the max concurrency of http request,avoid dos
* the http request headers and cookie can be set
* just crawl same host url
* just crawl same domain url


### Install

* python 2.7
* gevent
* requests
* pyquery


### Usage

        spider = Spider()
        spider.setRootUrl("http://www.sina.com.cn")
        spider.run()

