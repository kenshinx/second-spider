second-spider
=============

Another parallel spider, powered by gevent,requests,pyquery 

### Features

1. The concurrency foundation on [gevent](http://www.gevent.org/)
2. The spider strategy highly configurable:

> 
* Max depth 
* Sum totals of urls
* Max concurrency of http request,avoid dos
* Request headers and cookies
* Only crawl same host url
* Only crawl same domain url
* Max running time


### Dependencies

* python 2.7
* gevent 1.0dev
* requests 1.0.3
* pyquery 1.2.4


### Example

        spider = Spider()
        spider.setRootUrl("http://www.sina.com.cn")
        spider.run()


### TODO

* Support Distributed , update `gevent.Queue` -> `redis.Queue`
* Storage system highly configurable
* Support Ajax url (webkit etc..)


### LICENSE

Copyright © 2013 by kenshin

Under MIT license : [rem.mit-license.org](http://rem.mit-license.org/)


