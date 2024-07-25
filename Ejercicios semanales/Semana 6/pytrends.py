import pandas as pd
from pytrends.request import TrendReq


pytrends = TrendReq()
keywords = ["Fin del mundo", "Calentamiento global", "Terremoto",'Tsunami']
pytrends.build_payload(keywords, cat=0, geo='', gprop='') # Datos de los ultimos 5 años
stop_queries = pytrends.interest_over_time()[keywords]
stop_queries.head()