PyOnline
========
PyOnline is a Python interpreter, made with Windows' Touchdevelop platform.

This is for you, Taylor's SOCIT.

![Taylor's University School of Computing and IT](http://www.taylors.edu.my/img/TU_logo.jpg)

Details
-------
The backend (Python interpreter) is actually a web application made with [Google App Engine](https://cloud.google.com/products/app-engine/).

It can be accessed http:/www.pyonlineapi.appspot.

The user interface is built with Touchdevelop where it constantly interacts with the web application.

So basically, any application that can access the web can use this interpreter.

Usage
-----
Each user will need to access the API with a user_id, which is
generated on the client's side. 

**Example:**
`http:/www.pyonlineapi.appspot/<user_id>`

The code will be sent via a POST request in a url encoded manner.
Then, accessed at the same url with a GET request.

**Example:**
```python
>> from urllib import urlencode
>> from urllib2 import urlopen
>> # Urlencode key-value pair, where key must be 'code'
>> data = { 'code': "print 'hello world'" }
>> data = urlencode(data)
>> # Send POST request with extra data parameter in urlopen
>> urlopen('http://www.pyonline.appspot/userid', data)
>> result = urlopen('http://www.pyonline.appspot/userid')
>> result.read() # hello world
hello world
```

Authors and Contributors
------------------------
Maverick Chan, an aspiring entrepreneur, programmer.

Support or Contact
------------------
Having trouble with PyOnline? Contact Maverick at guanhao3797@gmail.com or through @guanhao97 on Twitter.
