# Crawler
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](http://mit-license.org/)
![python](https://img.shields.io/badge/python-2.7-blue.svg)

A basic implementation of a web crawler written in python.
 
 
### Usage
* Do `pip install -r requirements.txt`
* Run the crawler:

```
$ python crawler.py [url] [depth]
```

### Example
```
$ python crawler.py http://shashank.im 10
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
