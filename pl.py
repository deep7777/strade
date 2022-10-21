from nsepython import *
from datetime import date

import numpy as np
import pandas as pd

from nsepy.history import get_price_list
prices = get_price_list(dt=date(2022,10,20))

df = pd.DataFrame(prices)
#print(nifty_pe)

for index, row in df.iterrows():
    print(row)