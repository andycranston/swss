# swss - Selenium based Web Site Scanner

The `swss.py` Python script uses the Selenium package to visit one or more websites.

The websites can be named by either IPv4 IP address or URL.  A range of IP addresses can also be specified
in a short hand notation.

Once a website has been visited a screen shot is taken.  Also a logfile is maintained recording the
script progress and a simple CSV file is also produced which summarises the result of each site visit.

## Why is this useful?

Say you have deployed a number of network devices on a subnet.  You may want to document that each of
the devices has been successfully deployed.  A manual approach is to visit each device by entering the IP
address in a browser and once the page loads take a screenshot and save the screen shot in a file name
that indicates which device it was.

Using the `swss.py` Python script automates this process for you saving the screenshots with unique file names, creating
a progress log and putting summary information in a CSV file that can be loaded into a spreadsheet for easy viewing.

## Prerequisites

The following are prerequisites:

+ Python 3
+ Selenium Python bindings
+ Selenium Gecko Web Driver
+ FireFox web broswer

Tested on Windows 10 desktop.  Other versions of Windows may work if they support Selenium.

## Example run

Open a command prompt in Windows.

Change to the directory that contains the `swss.py` Python script.

Type:

```
python swss.py --iplist 192.168.1.1-3
```

Wait and watch! :-]

The FireFox web browswer will be automatically launched and then instructed to visit these three URLs in turn:

```
https://192.168.1.1/
https://192.168.1.2/
https://192.168.1.3/
```

At the end of the run the following files will have been created:

```
swss.log
swss.csv
swss-192-168-001-001-443.png
swss-192-168-001-002-443.png
swss-192-168-001-003-443.png
```

The `swss.log` file is a progress log.  Here is example output:

```
2018-08-06 15:35:31.711748: starting FireFox browser
2018-08-06 15:35:38.287051: FireFox started
2018-08-06 15:35:38.302682: getting  URL "https://192.168.1.1/"
2018-08-06 15:35:39.474535: error getting URL "https://192.168.1.1/" - "Message: Reached error page: about:neterror?e=connectionFailure&u=https%3A//192.168.1.1/&c=UTF-8&f=regular&d=Firefox%20can%E2%80%99t%20establish%20a%20connection%20to%20the%20server%20at%20192.168.1.1."
2018-08-06 15:35:39.474535: taking screenshot to file "swss-192-168-001-001-443.png"
2018-08-06 15:35:39.662017: getting  URL "https://192.168.1.2/"
2018-08-06 15:35:40.052689: waiting for page load to settle
2018-08-06 15:35:42.052880: taking screenshot to file "swss-192-168-001-002-443.png"
2018-08-06 15:35:42.240197: getting  URL "https://192.168.1.3/"
2018-08-06 15:35:43.333884: error getting URL "https://192.168.1.3/" - "Message: Reached error page: about:neterror?e=connectionFailure&u=https%3A//192.168.1.3/&c=UTF-8&f=regular&d=Firefox%20can%E2%80%99t%20establish%20a%20connection%20to%20the%20server%20at%20192.168.1.3."
2018-08-06 15:35:43.333884: taking screenshot to file "swss-192-168-001-003-443.png"
2018-08-06 15:35:43.505766: quiting FireFox browser
2018-08-06 15:35:44.662040: FireFox stopped
```

The `swss.csv` file is a CSV file that can be imported into a spreadsheet for easy viewing.  Here is example output:

```
"192-168-001-001","https://192.168.1.1/","get failed: Message: Reached error page: about:neterror?e=connectionFailure&u=https%3A//192.168.1.1/&c=UTF-8&f=regular&d=Firefox%20can%E2%80%99t%20establish%20a%20connection%20to%20the%20server%20at%20192.168.1.1.","n/a"
"192-168-001-002","https://192.168.1.2/","ok","Welcome to VMware ESXi"
"192-168-001-003","https://192.168.1.3/","get failed: Message: Reached error page: about:neterror?e=connectionFailure&u=https%3A//192.168.1.3/&c=UTF-8&f=regular&d=Firefox%20can%E2%80%99t%20establish%20a%20connection%20to%20the%20server%20at%20192.168.1.3.","n/a"
```

Note that the first field is a slightly modified representation of the IPv4 address.  By using padding zeros and dashes (-)
instead of dots (-) this first field can be used to sort by numerically increasing IPv4 address value.

The remaining files are PNG screenshots of the browser once each page has been visited.  For pages which did not
load the screenshot should have an error message explaining the reason why.

## Using different ports

By default the `swss.py` Python script assumes the web page is running on port 443 (https).  To specify a different port
use syntax similar to:

```
python swss.py --iplist 192.168.1.1-3 --port 80
```

## Variations on the --iplist argument

More than one --iplist argument can be specified by separating with a comma (,) as follows:

```
python swss.py --iplist 192.168.1.2,192.168.1.6,192.168.1.254
```

Names instead of IPv4 addresses can be used:

```
python swss.py --iplist www.google.co.uk,www.hpe.com,www.bbc.co.uk
```

If the argument begins with a plus sign (+) it is assumed to be a file containing
a list of IPv4 addresses and/or names.  For example if the file:

```
urlfile.txt
```

contains:

```
192.168.1.1
192.168.1.2
www.ibm.com
192.168.1.50-99
```

then this is the syntax to use:

```
python swss.py --iplist +urlfile.txt
```

All forms can be mixed up:

```
python swss.py --iplist 192.168.1.2,www.google.co.uk,10.10.10.1-254,+urlfile.txt
```

## Overriding the default names for the log file and CSV file

The default name for the log file (`swss.log`) can be overridden with this command line argument:

```
--logfile newlogfilename.txt
```

Also the default name for the CSV file (`swss.csv`) can be overridden with this command line argument:

```
--csvfile newlogfilename.csv
```



--------------------------------
End of README.md
