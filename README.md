# Craiglist-Cli
![image](https://github.com/ASVPATM/craiglist-cli/assets/159084542/b0b201f3-28c6-45fe-abe3-211e7f111df1)

**Simple Craigslist CLI for ease of use**

**List of World Cities came from https://github.com/datasets/world-cities.git**

# Setup
Clone The Directory

**Python3**
```
cd craiglist-cli; cd craig
```
**Install Dependencies**
```
pip3 install -r requirements.txt
```
**Run Main Script**
```
python3 script.py
```
# Issues
When handling cities with duplicate names, craigslist changes its url like this:

**For Example**

Amsterdam NY - https://albany.craigslist.org/location/amsterdam-ny

  ......vs
  
Amsterdam NE - https://amsterdam.craigslist.org

The domain format is not universal and I haven't factored in the way they handle them which will need me to test city by city

**Another Example**

When dealing with smaller cities/states/countries they tend to generalize to one major city and alter distance to match the coordinates of the city you are looking for

**Portland, Maine** does not exist but rather falls under the entire state of Maine: https://maine.craigslist.org

**United Arab Emirates** falls under domain: https://dubai.craigslist.org
# Updates
Will constantly be adding updates and improvements as I can, any recommendations would be greatly appreciated
atm.melles@gmail.com

# Tested On
Python version 3.12.3 (lubuntu)
