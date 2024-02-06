https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.PostgreSQL.html


# ---------------------------------------------
ON AURORA POSTgres
# ---------------------------------------------
DROP TABLE IF EXISTS public.sales;
CREATE TABLE IF NOT EXISTS public.sales
(
    invoiceid integer NOT NULL,
    itemid integer NOT NULL,
    category character varying(255) COLLATE pg_catalog."default",
    price numeric(10,0),
    quantity integer NOT NULL,
    orderdate timestamp without time zone,
    destinationstate character varying(2) COLLATE pg_catalog."default",
    shippingtype character varying(255) COLLATE pg_catalog."default",
    referral character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT sales_pkey PRIMARY KEY (invoiceid)
)

# ---------------------------------------------
ON ATHENA
# ---------------------------------------------

CREATE DATABASE dmsdb;



CREATE EXTERNAL TABLE  `dmsdb`.`raw_sales`(
  `action` string,
  `invoiceid` bigint,
  `itemid` bigint,
  `category` string,
  `price` bigint,
  `quantity` bigint,
  `orderdate` string,
  `destinationstate` string,
  `shippingtype` string,
  `referral` string)
ROW FORMAT DELIMITED
  FIELDS TERMINATED BY ','
STORED AS INPUTFORMAT
  'org.apache.hadoop.mapred.TextInputFormat'
OUTPUTFORMAT
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://dms-g/DMS/public/sales/'
  
TBLPROPERTIES (
  'CrawlerSchemaDeserializerVersion'='1.0',
  'CrawlerSchemaSerializerVersion'='1.0',
  'UPDATED_BY_CRAWLER'='s3',
  'areColumnsQuoted'='false',
  'classification'='csv',
  'columnsOrdered'='true',
  'compressionType'='none',
  'delimiter'=',',
  'typeOfData'='file'
  )

  
  
  