# Fabric notebook source

# METADATA ********************

# META {
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "87075977-c1b5-45fc-a88f-2a083d6b8023",
# META       "default_lakehouse_name": "HeartFailureLakeHouse",
# META       "default_lakehouse_workspace_id": "1852166c-bd3c-4dae-a90e-39c7373a88c8",
# META       "known_lakehouses": [
# META         {
# META           "id": "87075977-c1b5-45fc-a88f-2a083d6b8023"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# ## Module 2: Perform Data Cleansing and preparation using Apache Spark

# MARKDOWN ********************

# #### Reading data from delta table

# CELL ********************

data_df = spark.read.format("delta").load("Tables/heartFailure")
display(data_df)

# MARKDOWN ********************

# #### Checking if datatypes are numerical

# CELL ********************

data_df.dtypes

# MARKDOWN ********************

# #### Summarize dataframe

# CELL ********************

display(data_df.summary())

# CELL ********************

display(data_df.select("age").summary())

# CELL ********************

display(data_df.groupBy("age").count())

# MARKDOWN ********************

# ####  Missing Observation Analysis
# 
# Checking if any column has missing value

# CELL ********************

data_is_null = {col:data_df.filter(data_df[col].isNull()).count() for col in data_df.columns}
data_is_null

# CELL ********************

display(data_df.summary())

# MARKDOWN ********************

# ## feature engineering
# from sklearn.preprocessing import LabelEncoder- changing the datatype

# CELL ********************

from sklearn.preprocessing import LabelEncoder
import pandas as pd
lab = LabelEncoder()

# CELL ********************

data_df1 = data_df.toPandas()
obj = data_df1.select_dtypes(include='object')
not_obj = data_df1.select_dtypes(exclude='object')
for i in range(0, obj.shape[1]):
  obj.iloc[:,i] = lab.fit_transform(obj.iloc[:,i])
df_new = pd.concat([obj, not_obj], axis=1)
df_new.head(10)

# CELL ********************

display(df_new)

# MARKDOWN ********************

# #### Save processed data to a Delta Table

# CELL ********************

spark.conf.set("sprk.sql.parquet.vorder.enabled", "true") # Enable Verti-Parquet write
spark.conf.set("spark.microsoft.delta.optimizeWrite.enabled", "true") # Enable automatic delta optimized write

# CELL ********************

table_name = "heartfailure_processed"
data_df_processed = spark.createDataFrame(df_new)
data_df_processed.write.mode("overwrite").format("delta").save(f"Tables/{table_name}")
print(f"Spark dataframe saved to delta table: {table_name}")

# CELL ********************

# MAGIC %%sql
# MAGIC 
# MAGIC select * from heartfailure_processed limit 100;
