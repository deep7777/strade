from nsepy import get_index_pe_history
from nsepython import *
from datetime import date
import numpy as np
import pandas as pd

nifty_pe = get_index_pe_history(symbol="NIFTY",
                                start=date(2022,1,1),
                                end=date(2022,10,20))
df = pd.DataFrame(nifty_pe)
#print(nifty_pe)

for index, row in df.iterrows():
    print(row)