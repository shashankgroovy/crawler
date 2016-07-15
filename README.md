# Crawler
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](http://mit-license.org/)
![python](https://img.shields.io/badge/python-2.7-green.svg)

A basic implementation of a web crawler written in python.


### Usage
* Do `pip install -r requirements.txt`
* Run the crawler:

```
$ python crawler.py --help
usage: crawler [-h] [-d DEPTH] [-v] url

A basic implementation of a web crawler written in python.

positional arguments:
  url                   the url to crawl

optional arguments:
  -h, --help            show this help message and exit
  -d DEPTH, --depth DEPTH
                        set the max_depth for crawling
  -v, --verbose         Toggle verbose on (default is off)

For more information see http://github.com/shashankgroovy/crawler

```

### Example
```
$ python crawler.py http://shashank.im -d 10
Fetching urls...
Found: 27 links

https://play.google.com/store/apps/details?id=com.jrummy.root.browserfree
http://youtu.be/ulFeUCAI5xM
http://shashank.im/bucketlist
http://www.utorrent.com/
http://shashank.im
http://shashank.im/articles/2014/05/08/gsoc-selection/
...
```

### License
[MIT License](http://mit-license.org/)

Copyright (c) 2016 Shashank Srivastav
