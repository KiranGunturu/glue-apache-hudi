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
    StructField("vin", StringType()),
    StructField("make", StringType()),
    StructField("model", StringType()),
    StructField("year", IntegerType()),
    StructField("color", StringType()),
    StructField("mileage", IntegerType()),
    StructField("country_code", StringType())

])

vehicle_data = [
    ("1HGBH41JXMN109186", "Toyota", "Camry", 2018, "Blue", 45000, "US"),
    ("2HGFC2F59LH561098", "Honda", "Accord", 2019, "Red", 35000, "US"),
    ("1FTFW1EF9HFA06953", "Ford", "F-150", 2017, "White", 60000, "US"),
    ("1G1ZD5ST5KF165432", "Chevrolet", "Malibu", 2016, "Black", 55000, "CAN"),
    ("1N4AL2AP5CN575420", "Nissan", "Altima", 2020, "Silver", 25000, "CAN"),
    ("1C4BJWDG7JL863947", "Jeep", "Wrangler", 2015, "Green", 70000, "CAN"),
    ("WBABW33434PL13736", "BMW", "3 Series", 2021, "Gray", 15000, "US"),
    ("WDDWF4KB9DR274863", "Mercedes-Benz", "C-Class", 2018, "Black", 40000, "MEX"),
    ("WAUACAFR1FA018742", "Audi", "A4", 2019, "White", 30000, "MEX"),
    ("5NPD84LF6LH561234", "Hyundai", "Elantra", 2020, "Blue", 20000, "MEX"),
    ("5NPD84LF6LH561234", "Hyundai", "Elantra", 2020, "Blue", 20000, "US")
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
        .hasMin("year", lambda x: x == 2015) \
        .hasMax("year", lambda x: x == 2021)  \
        .isComplete("model")  \
        .isUnique("vin")  \
        .isComplete("country_code")  \
        .isContainedIn("country_code", ["US", "CAN", "MEX"]) \
        .isNonNegative("year") \
        .hasMaxLength("country_code", lambda x: x <=3)
        .hasDataType("year",ConstrainableDataTypes('String'))) \
    .run()

print(f"Run Status: {checkResult.status}")
verify_df_results = VerificationResult.checkResultsAsDataFrame(spark, checkResult)
verify_df_results.show()
#verify_df_results.printSchema()