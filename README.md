![image](https://github.com/KiranGunturu/glue-apache-hudi/assets/91672788/7aae7721-b985-4ec9-bd38-5a4af3675d60)


# Real-time Data Migration and Upsert Pipeline: PostgreSQL to S3 with CDC, Glue, and Apache Hudi

The objective of this project is to establish a seamless and efficient data pipeline for migrating data from an AWS PostgreSQL database to Amazon S3 while enabling Change Data Capture (CDC) using AWS Database Migration Service (DMS). The data will then be cataloged using AWS Glue, and subsequently, read from the Glue catalog and upserted to S3 utilizing Apache Hudi.

AWS DMS with CDC: AWS DMS will be configured to capture changes in the PostgreSQL database. This ensures that any modifications or updates to the data are tracked in real-time.

AWS Glue Cataloging: Once the data is migrated to S3 through DMS, AWS Glue will be utilized to catalog the data. Glue will provide a unified metadata repository, enabling easy discovery, organization, and management of the datasets.

Apache Hudi for Upsert: Apache Hudi will be employed to perform upsert operations on the data residing in S3. Hudi's capabilities allow for efficient handling of large datasets while providing support for upsert operations, ensuring that only the latest changes are applied to the data lake.

Glue Notebooks with Hudi Connectors: Glue Notebooks will be utilized in conjunction with Hudi connectors to facilitate the upsert process. These notebooks provide an interactive environment for data exploration, transformation, and integration, making it seamless to leverage Hudi's functionalities within the Glue ecosystem.

Athena for Data Querying: AWS Athena will be employed for querying the data residing in both Glue tables and Hudi tables. Athena offers a serverless querying service, enabling ad-hoc SQL queries on data stored in S3 without the need for managing infrastructure.

Maintaining History in S3 Data Lake: The project will maintain a historical record of the data in the S3 data lake. This ensures that historical snapshots are available for analytical purposes and compliance requirements.

Hudi Tables Reflecting PostgreSQL Data: While historical data is preserved in the S3 data lake, Hudi tables will reflect the current state of the data present in PostgreSQL. This ensures that analytical needs are met with real-time or near-real-time data availability.

Overall, this comprehensive data pipeline ensures the seamless migration, cataloging, and upserting of data from AWS PostgreSQL to S3, facilitating efficient data management and analysis for the organization.




## Deployment

## Provisioning Aurora PostgreSQL Database Instance:

#### 1. Sign in to AWS Console:
Log in to the AWS Management Console using your credentials.

#### 2. Navigate to RDS Dashboard:
Go to the Amazon RDS dashboard by selecting "RDS" from the list of services.

#### 3. Launch Aurora PostgreSQL Instance:

    1. Click on "Create database."
    2. Choose the PostgreSQL engine.
    3. Select "Amazon Aurora" as the edition.
    4. Choose the version and edition of Aurora PostgreSQL you want to use.
    5. Configure instance details like DB instance class, storage, VPC, etc.
    6. Set up the master username and password for the database.
    7. Configure advanced settings if needed, such as VPC, subnet group, security group, etc.
    8. Review the configuration and click "Create database."

#### 4. Note Endpoint and Credentials:
    1. Once the database instance is created, note down the endpoint (hostname) and the credentials (username and password) for future use.

#### 5. Creating an S3 Bucket:
 
    1. Navigate to S3 Dashboard:
    2. Go to the Amazon S3 dashboard by selecting "S3" from the list of services.

#### 6. Create Bucket:

    1. Click on "Create bucket."
    2. Provide a unique bucket name.
    3. Choose the region where you want to create the bucket.
    4. Configure options like versioning, encryption, etc., as per your requirements.
    5. Review the settings and click "Create bucket."
    6. Note Bucket Name: Once the bucket is created, note down the bucket name for future reference.

#### 7. DMS Setup:

    1. Replication Instance:
    2. Create a replication instance with a role having full permissions on DMS.
    3. Source Endpoint: Choose the RDS instance you've created.
    4. Provide the database name and credentials, or choose from the Secrets Manager.
    5. Test the connection to ensure successful connectivity.
    6. Target Endpoint: Choose S3 as the target.
    7. Provide the IAM ARN associated with DMS.
    8. Specify the bucket name and folder. place where DMS will write the data
    9. Test the connection to ensure successful connectivity.

#### 8. RDS Configuration:

    1. Create Parameter Group:
    2. Select parameter group family as "postgres" with the same version as your RDS instance.
    3. Choose the type as "DB cluster parameter group."
    4. Add required parameters like:
    5. rds.logical_replication=1
    6. wal_sender_timeout=0 (to disable write timeout) or specify timeout in seconds.
    7. Assign the parameter group created above to your RDS instance in the database options.
    8. Reboot the RDS database instance for changes to take effect.

#### 9. Data Migration Task:
    1. This task integrates the replication instance, source, and target endpoints to facilitate the data migration process.

#### 10. Install required libraries
  
    pip install -r ./requirements.txt

#### 10. Add RDS credentials and end points to .env file

    AURORA_DB_SERVER=us-east-1.rds.amazonaws.com
    AURORA_DB_PORT=5432
    AURORA_DB_UID=postgres
    AURORA_DB_PWD=postgres
    AURORA_DB_DATABASE=postgres 

### 11. Create the tables In PostgreSQL

    execute tables.sql (Aurora tables)

#### 12. Ingest sales data into PostgreSQL

    python ingest-into-aurora.py

#### 13. Validate the data through pgAdmin tool
#### 14. Validate the data in the S3 bucket
#### 15. Create the tables in athena location pointing to where RDS wrote to (#7, 8th point)
    execute tables.sql (Athena tables)

#### 16. Create Glue job and upload notebook with IAM role (Role which has permissions to s3 and Glue)

    0. upload the notebook hudi-upsert.ipynb
    1. provide recordKey
    2. provide precombineKey
    3. provide S3 location where we want to store the hudi dataset
    4. write operation as upsert











    

