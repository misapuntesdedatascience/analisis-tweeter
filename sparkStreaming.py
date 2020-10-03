from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import desc

# Sólo se puede ejecutar una vez, reinicia el kernel si te da error.
sc = SparkContext()

ssc = StreamingContext(sc, 10)
sqlContext = SQLContext(sc)

socket_stream = ssc.socketTextStream("localhost", 9999)

lines = socket_stream.window(20)

from collections import namedtuple
fields = ("tag", "count")
Tweet = namedtuple('Tweet', fields)

# Usamos parentesis para varias lineas
(lines.flatMap(lambda text: text.split(" ")) 
             .filter(lambda word: word.lower().startswith("#")) 
             .map(lambda word: (word.lower(), 1)) 
             .reduceByKey(lambda a, b: a + b) 
             .map(lambda rec: Tweet(rec[0], rec[1]))             
             .foreachRDD(lambda rdd: rdd.toDF().sort("count")      
             .limit(50).registerTempTable("tweets"))) 

ssc.start()   

#ssc.stop()