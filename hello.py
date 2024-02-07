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


schema = """ vhcl_id string ,
            line_code string ,
            year_number int ,
            country_code string ,
            body_style string ,
            line_name sting ,
            engine_mode_code 
            string reg_state string"

data = [
    (123, "BMW", "2020", )
]

