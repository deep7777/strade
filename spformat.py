from datetime import date
from nsepython import *
import math

day = date.today().strftime('%d');
year = date.today().strftime('%Y');
month = date.today().strftime('%m');

print(year,month,day)
url = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'

indices = nsefetch(url)
underlyingValue = indices['records']['underlyingValue']
def roundup(x):
 	return int(math.floor(x / 100.0)) * 100

start = roundup(underlyingValue) - 1000
end = roundup(underlyingValue) + 1000
print(roundup(underlyingValue))
strf = 'python strikes.py '+str(year)+' startmonth'+' startday'+' endmonth'+' endday'+' expirymonth expirydate'+' '+str(day)+' NIFTY'+' '+str(start)+' '+str(end)+' 100'
#print(strf)
print('python strikes.py 2022 10 27 11 1 11 3 NIFTY 18000 18300 100')
#print('python strikes.py 2022 10 6 27  NIFTY 2300 2600')