from pyspark.sql import SparkSession
import time
def printdata(listout):
    for i in range(len(listout)):
        print(listout[i])

def timef(row):
    x = row['checkin_time'].split(':')[0]
    x = int(x.split('T')[-1])
    return (str(x)+':00-'+str(x+1)+':00',1)

spark=SparkSession.builder\
    .appName('My_App')\
    .master('local')\
    .getOrCreate()
df = spark.read.csv('Brightkite_totalCheckins.csv',header=True)
df = df.na.drop()
Time_ini=time.time() 
listpoptime = df.rdd.map(timef).reduceByKey(lambda x,y:x+y).sortBy(lambda a: a[1],ascending = False).collect()
Time_end=time.time() 
print('共花了'+str(Time_end-Time_ini)+'秒') 
printdata(listpoptime)