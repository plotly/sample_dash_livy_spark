# Sample Dash app with Livy and Spark
Example Dash app running against Spark cluster via Apache Livy

Tested against an AWS EMS 3-node cluster running Hadoop, Spark and Livy. Livy can be accessed by SSH port mapping port 8998.

Livy provides an HTTP REST interface for managing Spark sessions and initiating and monitoring jobs in Spark. 
The Dash Application uses this REST interface (using the Python `requests` library. 

A relatively large fraction of the code in this sample is devoted to monitoring Spark and printing out the status of the current session and current running job to the Dash Frontend. It monitors these processes using the Dash Interval component. Other mechanisms such as utilitizing the Task Queue system built into the [Dash Deployment Server](https://plot.ly/dash/pricing/) are recommended for production usage.

This Dash Application is POC only. 

Note that it may be worth exploring Spark Thrift Server and the ODBC driver as a means of connecting a Dash application to Spark.
