# Setting up Feast Spark on CML
High level instructions on setting up FEAST feature store with SPARK offline store
## Useful links
[feast-spark](https://docs.feast.dev/reference/offline-stores/spark)
[Quick-start](https://docs.feast.dev/getting-started/quickstart)
[Feast spark-getting-started](https://docs.feast.dev/reference/offline-stores/spark#getting-started)

## Key Notes
- This has been tested on feast version 0.30.2, so recommend using that version
- Ensure that pyspark version matches spark version, without which this installation will not succeed
- Ensure you have access to the Hive Table in a Cloudera Datawarehouse(CDW) and can access the driver_stats table in default database. if you would like to create your own table then go to section Create your own table

## Setup Instructions

### Folder Structure 
Key files and folders  to be modified/ used in this project : 

```
|- feast_project
    |- data : Online feature database 
    |- feature_repo 
        |- feature_store.yaml : Feature store configuration file for offline and online stores
        |- example_repo.py : Feature defintion file 
|- DataLoad.ipynb : Validate Spark's ability to fetch the offline store data
|- feast-ux.py : used to load the Feast UI
|- feature-store-dev.ipynb : Interactive notebook for Feast historical and online store access
    

```

### Load Dataset
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
- in this repo feast_project/feature_repo/data folder you will find a driver_hourly_stats.parquet file 
- Load this file in the hive table using hue or SPARK
- One option is to copy this in a s3 bucket and then load into the table as below
``` LOAD DATA INPATH '<s3bucket patth> driver_stats.parquet' INTO TABLE default.driver_stats; ```

### Feature Store Setup
Spin off a new session in CML ( Use ONLY **Jupyter Notebook/ Python3.8/ Spark Runtime Option**  ) and launch Terminal with the commands below<br>
``` pip install feast==0.30.2 ``` 
    pip install feast[spark]``` 
    pip install pyspark==3.2.0``` 

If you get a TypeError, check if the troubleshooting section has a solution for you.

- If the above commands compiled without error you have now setup feast successfully <br>
- Ensure that you have the dataset file copied in the data folder to a s3 bucket or ADLS bucket before you start. 
- Next, check that Spark on CML is able to read the file you have kept in a remote S3 ( or ADLS location) by running the Dataload.ipynb

### Changes to feature definition file. 

Finally, you need to change the feature_store.yaml file in $HOME/feast_project/feature_repo to the values of the datalake that you are using, so make the changes 

```
    # change this in Featurestore.yaml
    spark.sql.warehouse.dir: "s3a://< AWS datalake name>/data/warehouse/tablespace/managed/hive"
    spark.hadoop.fs.s2a.s3guard.ddb.region: "us-east-1"
    spark.yarn.access.hadoopFileSystems: "s3a://<AWS datalake name>/"   
```

Finally update the feast_project/feature_rep feature_store.yaml file with the right directory locations

If everything is set up right, 
```
    cd  $HOME/feast_project/feature_repo 
    feast apply 
``` 
should compile the feature specifications

after *feast apply* this is the output you are looking for towards creation of a feature service
``` 
    Hive Session ID = a2e4bd49-9bdf-4fa9-b74a-f0ffd1d522e6
    Created entity driver
    Created feature view driver_hourly_stats
    Created feature service driver_activity_v1
...
...
```
check the Feature-store-dev.ipynb to see how to consume the feature store for offline training and online serving example

### Running / Executing Feast

The command below executes a complete feast workflow including setting up historical feature store, online feature store, feature views and dynamic feature computations

```
    python3 testworkflow.py
```

###  Example : Inline Feature store usage using API 
Run the commands in $HOME/Feature-store-dev.ipynb to understand how to access the online and offline feature store. 

## Setting up the Feast User Interface
Create a new application in CML using feast-ux.py and resources 1 vcPU and 2 GB memory. this will ensure that you can use the Feast UI within CML to view the Feature Catalog as well as available features. 

### Troubleshooting 

if you get an error as below <br>
```TypeError: the 'package' argument is required to perform a relative import for '.ipynb_checkpoints.example-checkpoint' ```
it means that ipython notebook has created a checkpoint use the command below and again try Feast apply<br>
``` rm -fR .ipynb_checkpoints/```<br>
