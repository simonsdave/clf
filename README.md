CloudFeaster is a screen scraping infrastructure that dramatically
simplifies the creation and operation of spiders that login to web
sites on behalf of consumers.

Lots of
[screen scraping utilities](https://github.com/simonsdave/clf/wiki/Other-Web-Scraping-Utilities-&-Approaches)
exist so why create another one?
Key reasons:

1. the other 
[screen scraping utilities](https://github.com/simonsdave/clf/wiki/Other-Web-Scraping-Utilities-&-Approaches)
are general purpose tools where as CloudFeaster is specialized for
the task of creating spiders that login to web
sites on behalf of consumers
1. CloudFeaster is not a single tool or utility; CloudFeaster is
a complete end-to-end infrastructure supporting the creation and
operation spiders
1. CloudFeaster thinks about the problem very differently and
leverages modern approaches to software engineering - the
end result of this different thinking is that spiders written
with CloudFeaster are super easy to create and not brittle like
spiders written in the "mimic a browser's network traffic" style

Prerequisites 
-------------
* code written and tested on Mac OS X 10.8.4 and 10.9 using:
  * [git](http://git-scm.com/) (1.7.12.14 on Mac OS X 1.8.4 and 1.8.3.4 on Mac OS X 10.0) 
  * [Python](http://www.python.org/) (2.7.2 on Mac OS X 1.8.4 and 2.7.5 on Mac OS X 10.0) 
  * [pip](http://www.pip-installer.org/en/latest/installing.html) (1.4.1 on Mac OS X 10.0)
  * [virtualenv 1.10.1](https://pypi.python.org/pypi/virtualenv)
  * [VirtualBox 4.2.18](https://www.virtualbox.org/wiki/Downloads)
  * [Vagrant 1.3.4](http://downloads.vagrantup.com/tags/v1.3.4)
  * [ChromeDriver 2.4](http://chromedriver.storage.googleapis.com/index.html?path=2.4/)
  * [command line tools for Xcode](https://developer.apple.com/downloads/index.action) - either - April 2013 for OS X Mountain Lion or late October 2013 for OS X Mavericks
* see
[requirements.txt](https://github.com/simonsdave/clf/blob/master/requirements.txt "requirements.txt")
for the complete list of python packages on which CloudFeaster depends

Development
-----------
The following (brief) instructions describe how to setup a your development environment.

> Before you start working through the instructions below make sure you
> have installed the components described above. In particular, if you don't install
> [command line tools (OS X Mountain Lion) for Xcode - April 2013](https://developer.apple.com/downloads/index.action)
> you'll find it hard to debug the error messages produced by
> [source bin/cfg4dev](https://github.com/simonsdave/clf/blob/master/bin/cfg4dev). 

* get the source code by running the following in a new terminal window

~~~~~
cd
git clone https://github.com/simonsdave/clf.git
cd clf
source bin/cfg4dev
~~~~~

* ...
