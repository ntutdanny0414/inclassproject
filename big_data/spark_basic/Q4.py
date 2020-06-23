from pyspark.sql import SparkSession
import time
def checkfriend(row):
    v = list(row[1])
    count = len(v)
    for i in row[1]:
        if len(set(row[1]) & set(friendlist[i])) == 0:
            count = count - 1
    return (row[0],count)
spark=SparkSession.builder\
    .appName('My_App')\
    .master('local')\
    .getOrCreate()
df = spark.read.csv('Brightkite_totalCheckins.csv',header=True)
df = df.na.drop()
df2 = spark.read.csv('Brightkite_edges.csv',header=True)
Time_ini=time.time() 
friendlist = df2.rdd.map(lambda row : (row['user_id'],[row['user_id2']])).reduceByKey(lambda x,y:x+y).collect()
locallist = df.rdd.map(lambda row : (row['location_id'],[row['user_id']])).reduceByKey(lambda x,y:set(x)|set(y)).collect()
friendlist = dict(friendlist)
sc = spark.sparkContext
rdd = sc.parallelize(locallist)
out = rdd.map(checkfriend).sortBy(lambda a: a[1],ascending = False).collect()
Time_end=time.time() 
print('共花了'+str(Time_end-Time_ini)+'秒') 
print(out)
