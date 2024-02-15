hudi_options = {
    'hoodie.table.name': table_name,
    'hoodie.datasource.write.table.type': table_type,
    'hoodie.datasource.write.recordkey.field': recordkey,
    'hoodie.datasource.write.table.name': table_name,
    'hoodie.datasource.write.operation': method,
    'hoodie.datasource.write.precombine.field': precombine,

    "hoodie.clean.automatic": "true"
    , "hoodie.clean.async": "true"
    
    ,"hoodie.parquet.max.file.size": 512 * 1024 * 1024  # 512MB
    ,"hoodie.parquet.small.file.limit": 104857600  # 100MB

}

'''
The following are important configuration parameters used in the Hudi data management system:

hoodie.parquet.small.file.limit: This parameter sets the threshold for identifying small files. The default value is 100MB. Smaller file sizes can improve write performance as they can be processed faster during ingestion.

hoodie.parquet.max.file.size: This parameter determines the desired size for Hudi-managed files. The default value is 120MB. Larger file sizes can be beneficial for query performance, as reading from larger files is generally faster. However, larger files may increase writer latency during ingestion.

It is generally recommended to have a target file size between 100MB and 500MB for faster Parquet reading. However, the optimal size also depends on the cluster configurations. If the cluster has sufficient resources, larger file sizes can be used, but it is advisable to stick to around 100MB to 200MB for most scenarios.

Clustering can also be employed to improve the efficiency of larger files in async mode. By clustering related data together, the query performance can be further optimized, as it reduces the amount of data that needs to be read for a specific query.

To ensure that new inserts are always routed to newer file groups and only updates go to existing ones, set the hoodie.parquet.small.file.limit to 0 in your configuration.
'''
