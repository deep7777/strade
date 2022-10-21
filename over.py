from datetime import date
from nsepy import get_history
vix = get_history(symbol="INDIAVIX",
            start=date(2022,1,1),
            end=date(2022,9,30),
            index=True)

vix['Close'].plot()
