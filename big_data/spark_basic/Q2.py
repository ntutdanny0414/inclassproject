# -*- coding: utf-8 -*-
from pyspark.sql import SparkSession
import time
        
spark=SparkSession.builder\
    .appName('My_App')\
    .master('local')\
    .getOrCreate()
df = spark.read.csv('Brightkite_totalCheckins.csv',header=True)
df = df.na.drop()
Time_ini=time.time() 
listuser = df.rdd.map(lambda row : (row['user_id'],1)).reduceByKey(lambda x,y:x+y).sortBy(lambda a: a[1],ascending = False).collect()
Time_end=time.time() 
print('共花了'+str(Time_end-Time_ini)+'秒') 
print(listuser)
