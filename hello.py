try:
    import os
    os.environ["SPARK_VERSION"]="3.2"
    from pyspark.sql import SparkSession, Row
    import pydeequ
    from pydeequ.analyzers import *
except Exception as e:
    print(e)

spark = (SparkSession
    .builder
    .config("spark.jars.packages", pydeequ.deequ_maven_coord)
    .config("spark.jars.excludes", pydeequ.f2j_maven_coord)
    .getOrCreate())



from pyspark.sql.types import StructType, IntegerType, StructField, StringType

schema = StructType([
    StructField("vin", StringType(), True),
    StructField("year", IntegerType(), True),
    StructField("model", StringType(), True),
    StructField("color", StringType(), True),
    StructField("mileage", IntegerType(), True),
    StructField("country_code", StringType(), True),
    StructField("body_style", StringType(), True),
    StructField("retail_state_code", StringType(), True),
    StructField("company_code", StringType(), True)
])


vehicle_data = [
    ("1N4AL2AP5CN575420", 2020, "Altima", "Silver", 25000, "JP", "Sedan", "NY", "NISSAN"),
    ("3N1AB8CV7LY265381", 2019, "Versa", "Black", 30000, "US", "Sedan", "CA", "NISSAN"),
    ("JN1EV7AR4HM000014", 2017, "Leaf", "Blue", 15000, "MEX", "Hatchback", "TX", "NISSAN"),
    ("JN8AZ1MU0CW123456", 2021, "Rogue", "White", 20000, "US", "SUV", "FL", "NISSAN"),
    ("JN1AZ4EH4EM630176", 2014, "Maxima", "Red", 50000, "US", "Sedan", "GA", "NISSAN"),
    ("5N1CR2MM5GC650002", 2016, "Murano", "Gray", 45000, "CAN", "SUV", "IL", "NISSAN"),
    ("1N6BA0ED7FN535210", 2015, "Titan", "Silver", 60000, "MEX", "Truck", "WA", "NISSAN"),
    ("5N1AA0NC7AN001234", 2018, "Pathfinder", "Black", 35000, "US", "SUV", "MI", "NISSAN"),
    ("5N3AA08A76N800000", 2010, "Armada", "Brown", 70000, "CAN", "SUV", "NY", "NISSAN"),
    ("JN8AY2NE7H9150000", 2013, "Quest", "Green", 55000, "CAN", "Minivan", "TX", "NISSAN"),
    ("JN8AY2NE7H9150000", 2013, None, "Green", 55000, "US", "Minivan", "TX", "NISSAN")
]

df = spark.createDataFrame(vehicle_data, schema)
df.show(truncate=False)
print(df.count())



from pydeequ.checks import *
from pydeequ.verification import *



check = Check(spark, CheckLevel.Warning, "Vehicle Analysis")

checkResult = VerificationSuite(spark) \
    .onData(df) \
    .addCheck(
        check.hasSize(lambda x: x >= 11) \
        .hasMin("year", lambda x: x == 2010) \
        .hasMax("year", lambda x: x == 2021)  \
        .isComplete("model")  \
        .isUnique("vin")  \
        .isComplete("country_code")  \
        .isContainedIn("country_code", ["US", "CAN", "MEX"]) \
        .isNonNegative("year") \
        .hasMaxLength("country_code", lambda x: x <=3) \
        .hasUniqueness(["model", "body_style"], lambda x: x >= 0.8) \
        .hasDataType("year",ConstrainableDataTypes('String'))) \
    .run()

print(f"Run Status: {checkResult.status}")
verify_df_results = VerificationResult.checkResultsAsDataFrame(spark, checkResult)
verify_df_results.withColumnRenamed("constraint_status", "DQ_Status").show()
#verify_df_results.printSchema()

df_dq_status = verify_df_results.withColumnRenamed("constraint_status", "DQ_Status")
df_dq_status.filter(df_dq_status.DQ_Status == 'Failure').show()

