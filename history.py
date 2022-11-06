from datetime import date
from nsepy import get_history
import numpy as np
import pandas as pd
import pickle



symbol = "NIFTY"
start = date(2022, 10, 1)
end = date(2022, 11, 3)
data = get_history(symbol=symbol, start=start, end=end,index=True)
print(data)

with open('NIFTY.pickle', 'wb') as f:
    pickle.dump(data, f)