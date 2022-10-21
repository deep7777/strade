from nsepython import *
from datetime import date
from nsepy import get_history
from nsepy.history import get_price_list

import numpy as np
import pandas as pd
import array


mt = 10
expiry = 29
start = date(2022,mt,1)
end = date(2022,mt,4)
expiry_date = date(2022,10,27)
nifty_opt = get_history(symbol="NIFTY",
                        start=start,
                        end=end,
                        index=True,
                        option_type='PE',
                        strike_price=18000,
                        expiry_date=expiry_date)

print(nifty_opt)
