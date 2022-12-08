# Setting up Feast Spark on CML
High level instructions on setting up FEAST feature store with SPARK offline store
## Useful links
[feast-spark](https://docs.feast.dev/reference/offline-stores/spark) <br>
[Quick-start](https://docs.feast.dev/getting-started/quickstart) <br>
[Feast spark-getting-started](https://docs.feast.dev/reference/offline-stores/spark#getting-started)

## Key Notes
- Use feast version 0.21 
- Ensure that pyspark version matches spark version, without which this installation will not succeed
- Ensure you have access to the Hive Table in a Cloudera Datawarehouse(CDW) and can access the driver_stats table in default database. if you would like to create your own table then go to section Create your own table

# High level steps
Spin off a new session in CML ( Workbench ) and launch Terminal with the commands below<br>
``` pip install feast==0.21 ``` <br>
``` pip install feast[spark]``` <br>
``` pip install pyspark==3.2.0``` <br><br>

If this compiles without error you have now setup feast successfully <br>
Next, Create a new feast repo
``` feast init my_project ``` <br>
this creates a feast repository with an .yaml file and feature specification file Example.py
Next replace the .yaml file and example.py file from good_mallard director of this repo into my_project folder <br>
``` cd my_project ``` <br>
``` feast apply ``` <br>
This should compile the feature specifications and you should see an output as below

if you get an error as below <br>
```TypeError: the 'package' argument is required to perform a relative import for '.ipynb_checkpoints.example-checkpoint' ```
it means that ipython notebook has created a checkpoint use the command below and again try Feast apply<br>

``` rm -fR .ipynb_checkpoints/```<br>
after feast apply this is the output you are looking for towards creation of a feature service
``` Hive Session ID = a2e4bd49-9bdf-4fa9-b74a-f0ffd1d522e6
Created entity driver
Created feature view driver_hourly_stats
Created feature service driver_activity_v1
Created sqlite table good_mallard_driver_hourly_stats 
```
check the Feature-store-dev.ipynb to see how to consume the feature store for offline training and online serving example

### Create your own Hive Table 
- Launch Hue
- Spark ( hive) offline store works only on default database 
- make sure you are in the default database and create the table below
```
CREATE TABLE driver_stats (
    event_timestamp   bigint,
    driver_id         bigint,
    conv_rate         float,
    acc_rate          float,
    avg_daily_trips   int,
    created           bigint
)
STORED AS PARQUET;
```
- in the repo good_mallard you will find a driver_hourly_stats.parquet file 
- Load this file in the hive table using hue or SPARK
- One option is to copy this in a s3 bucket and then load into the table as below
``` LOAD DATA INPATH '<s3bucket patth> driver_stats.parquet' INTO TABLE default.driver_stats; ```
- Finally, you need to change the feature_store.yaml file in your feature store repo my_project to the values of the datalake that you are using 
```
        # change this in Featurestore.yaml
        spark.sql.warehouse.dir: "s3a://< AWS datalake name>/data/warehouse/tablespace/managed/hive"
        spark.hadoop.fs.s2a.s3guard.ddb.region: "us-east-1"
        spark.yarn.access.hadoopFileSystems: "s3a://<AWS datalake name>/"   

```
