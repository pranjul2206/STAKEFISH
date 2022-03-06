import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

#connection
cnx = sqlite3.connect('../DATABASE/BTC.db')
df = pd.read_sql_query("select hash,block,time,count from btcDB where block in (SELECT MIN(block) as id FROM btcDB GROUP BY count)", cnx)


#graph
print('printing graph for you')
plt.plot(df["block"], df["count"])
plt.show()
