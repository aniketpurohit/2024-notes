# Serverless SQL pools

Synapse SQL is distributed query system in Azure Analytics

- Serverless SQL pools
  - On-demand SQL query procesing, primarily used to work with data in data lake
- Dedicated SQL Pools
  - Enterprise-scale relational DB instances used to host data warehouses in which data is stored in relational tables.

Serverless SQL pool is tailored for querying data residing n data lake, so in addition to eliminating management burden, it eliminates a need to worry about ingesting the data into the system.

 SQL serverless resource model is great for unplanned or "bursty" workloads that can be processed using the always-on serverless SQL endpoint in your Azure Synapse Analytics workspace

 > Serverless SQL pool is an analytics system and is not recommended for OLTP workloads

### Query Files using a serverless SQL pool

 query data files in various common file formats:

- Delimited text
- Javascript objetc notation (JSON) files
- parquet files

basic syntax is built on OPENROWSET SQL function; which generates a tabular rowset from data in one or more files.

```SQL
SELECT TOP 100*
FROM OPENROWSET(
  BULK 'https://mydatalake.blob.core.windows.net/data/files/*.csv',
    FORMAT = 'csv') AS rows

/* Explanation
* OPENROWSET function includes more parameters that determine factors
* The schema of resulting rowset
* Additional formatting options for delimited text files
* server-scoped credential if file is protected with SAS key or custom identity

*/
```

### Querying delimited text files

The specific formatting used in delimited files can vary

- With and without a header row
- Comma and tab-delimited values
- Windows and UNIX style line endings
- Non-quoted and quoted values and escaping characters.

```SQL
SELECT TOP 100 *
FROM OPENROWSET(
    BULK 'https://mydatalake.blob.core.windows.net/data/files/*.csv',
    FORMAT = 'csv',
    PARSER_VERSION = '2.0',
    FIRSTROW = 2) AS rows
```

***Explanation***

- PARSER_VERSION
  - used to determine how the query interprets the txt encoding used in files.
  - Version 1 is default and supports a wide range of file encoding
  - Veriosn 2 supports fewer encoding but offers better performance
  - FIRSTROW parameter is used to skip rows in text file, to eliinate any unstructured preamble text
  - FIELDTERMINATOR
    - The character used to separate field values in each row.
    - default field terminator is a comma (,)
  - ROWTERMINATOR
    - character used to signify the end of row of data.
  - FIELDQUOTE
    - character used to enclose quoted string values.
    - the double-quote (") is default quote character

#### specifying the rowset schema

**HEADER_ROW** paramter (which is only available when using parser version2.0 ) instructs the qurey engine to use first row of data in each file

```SQL
SELECT TOP 100 * FROM OPENROWSET(
  BULK = 'https://mydatalake.blob.core.windows.net/data/files/*.csv',
  FORMAT='CSV',
  PARSER_VERSION='2.0',
  HEADER_ROW = TRUE
) AS rows
```

---
when HEADER_ROW is not present

```SQL
SELECT TOP 100 *
FROM OPENROWSET(
    BULK 'https://mydatalake.blob.core.windows.net/data/files/*.csv',
    FORMAT = 'csv',
    PARSER_VERSION = '2.0')
WITH (
    product_id INT,
    product_name VARCHAR(20) COLLATE Latin1_General_100_BIN2_UTF8,
    list_price DECIMAL(5,2)
) AS rows
```

> If you encounter some incomptiblity with UTF-8 encoded data and collation uses compatible collation for individual VARCHAR columns

### Querying JSON file

JSON is a popular format for web applications that exchange data through REST interfaces or use NoSQL data stores such as Azure Cosmos DB

return product data from a folder containing multiple JSON files in this format, you could use the following SQL query:

```SQL
SELECT doc
FROM
    OPENROWSET(
        BULK 'https://mydatalake.blob.core.windows.net/data/files/*.json',
        FORMAT = 'csv',
        FIELDTERMINATOR ='0x0b',
        FIELDQUOTE = '0x0b',
        ROWTERMINATOR = '0x0b'
    ) WITH (doc NVARCHAR(MAX)) as rows
```

To extract individual values from the JSON, you can use the JSON_VALUE function in the SELECT statement, as shown here:

```SQL
SELECT JSON_VALUE(doc, '$.product_name') AS product,
           JSON_VALUE(doc, '$.list_price') AS price
FROM
    OPENROWSET(
        BULK 'https://mydatalake.blob.core.windows.net/data/files/*.json',
        FORMAT = 'csv',
        FIELDTERMINATOR ='0x0b',
        FIELDQUOTE = '0x0b',
        ROWTERMINATOR = '0x0b'
    ) WITH (doc NVARCHAR(MAX)) as rows
```

### Querying Parquet files

Parquet is a commonly used format for big data processing on distributed file storage. It's an efficient data format that is optimized for compression and analytical querying.
FORMAT must be *parquet*

```SQL
SELECT TOP 100 *
FROM OPENROWSET(
    BULK 'https://mydatalake.blob.core.windows.net/data/files/*.*',
    FORMAT = 'parquet') AS rows
```

### Partitioned data

common in a data lake to partition data by splitting across multiple files in subfolders that reflect partitioning criteria. This enables distributed processing systems to work in parallel on multiple partitions of the data, or to easily eliminate data reads from specific folders based on filtering criteria

To create a query that filters the results to include only the orders for January and February 2020, you could use the following code:

```SQL
SELECT *
FROM OPENROWSET(
    BULK 'https://mydatalake.blob.core.windows.net/data/orders/year=*/month=*/*.*',
    FORMAT = 'parquet') AS orders
WHERE orders.filepath(1) = '2020'
    AND orders.filepath(2) IN ('1','2');
```

### Create External DB Object

can use the graphical interface in Synapse Studio, or a CREATE DATABASE statement. One consideration is to set the collation of your database so that it supports conversion of text data in files to appropriate Transact-SQL data types.

```SQL
CREATE DATABASE SalesDB COLLATE Latin1_General_100_BIN2_UTF8
```

### Creating an extrernal data source

can use the OPENROWSET function with a BULK path to query file data from your own database. it's more efficient to define an external data source that references that location.

```SQL
CREATE EXTERNAL DATA SOURCE files
WITH (
    LOCATION = 'https://mydatalake.blob.core.windows.net/data/files/'
)
```

you can simplify an OPENROWSET query to use the combination of the data source and the relative path to the folders or files you want to query:

```SQL
SELECT * FROM OPENROWSET(
BULK 'orders/*csv',
DATA_SOURCE = 'files',
FORMAT='csv',
PARSER_VERSION='2.0'
) AS orders
```

Another benefit of using a data source is that you can assign a credential for the data source to use when accessing the underlying storage, enabling you to provide access to data through SQL without permitting users to access the data directly in the storage account.

```SQL
CREATE DATABASE SCOPED CREDENTIAL sqlcred
WITH
  IDENTITY = 'SHARED ACCESS SIGNATURE',
  SECRET = 'YOU SECRET';
GO

CREATE EXTERNAL DATA SOURCE secureFiles WITH (
LOCATION  = 'https://mydatalake.blob.core.windows.net/data/secureFiles/',
CREDENTIAL = sqlcred
);
GO
```

### Creating an external file format

```SQL
CREATE EXTERNAL FILE FORMAT CsvFormat WITH (
  FORMAT_TYPE=DELIMITEDTEXT,
  FORMAT_OPTIONS(
  FIELD_TERMINATOR =',',
  STRING_DELIMITER = '"'
  )
);
GO 
```

### Creating an external table

To simplify access to the data, you can encapsulate the files in an external table; which users and reporting applications can query using a standard SQL SELECT statement just like any other database table

```SQL
CREATE EXTERNAL TABLE dbo.products
(
  product_id INT,
  product_name VARCHAR(20),
  list_price DECIMAL(5,2)
)
WITH
(
  DATA_SOURCE = files,
  LOCATION = 'products/*.csv'
  FILE_FORMAT = CsvFormat
);
GO 
```

## SQL pools to transform data in data lake

The SQL language includes many features and functions that enable you to manipulate data.

- Filter rows and columns in a Dataset
- Rename data fields and convert between data types.
- Calculate derived data fields
- Manipulate string values.
- Group and aggregate data.

Can be used to run SQL statements that transform data and persist the results as a file in a data lake for further processing or querying.
CREATE EXTERNAL TABLE AS SELECT (CETAS) statement in a dedicated SQL pool or serverless SQL pool to persist the results of a query in an external table, which stores its data in a file in the data lake.

![External table as select ](https://learn.microsoft.com/en-us/training/wwl-data-ai/use-azure-synapse-serverless-sql-pools-for-transforming-data-lake/media/create-external-table-as-select.png)

### Creating external database objects to support CETAS

CETAS expression, can be used with a Database. With regard to serverless SQL pool, create these objects in a custom database (`CREATE DATABASE`)

#### External data source

An external data source encapsulates a connection to a file system location in a data lake.
If the source data for the CETAS statement is in files in the same data lake path, you can use the same external data source in the OPENROWSET function used to query it

```SQL
-- create an external data source for the azure storage account 
CREATE EXTERNAL DATA SOURCE files 
WITH (
  LOCATION = 'ttps://mydatalake.blob.core.windows.net/data/files/',
  TYPE = HADOOP, -- for dedicated SQL pool
  -- TYPE = BLOB_STORAGE, 
  CREDENTIAL = storageCred
);

-- Without the assuming that the user will have permission for the files

CREATE DATABASE SCOPED CREDENTIAL storagekeycred WITH 
IDENTITY='SHARED ACCESS SIGNATURE',
SECRET='<YOUR SECRET>';

CREATE EXTERNAL DATA SOURCE secureFiles WITH (
  LOCATION='https://mydatalake.blob.core.windows.net/data/secureFiles/'
  CREDENTIAL= storagekeycred
);
```

### External File format

The CETAS statement created a table with its data stored in files. you must specify format of the files you want to create as an external file format.

```SQL
CREATE EXTERNAL FILE FORMAT ParquetFormat WITH (
  FORMAT_TYPE = PARQUET,
  DATA_COMPRESSION = 'org.apache.hadoop.io.compress.SnappyCodec'

);
```

### Using CETAS satement

After creating an external data source and external file format, you can use the CETAS statement to transform data and stored the results in an external table.

```SQL
CREATE EXTERNAL TABLE SpecialOrders WITH (
  -- DETAILS FOR STORING RESULTS
  LOCATION = 'special_orders/',
  DATA_SOURCE= files,
  FILE_FORMAT = ParquetFormat
)
AS 
SELECT OrderID, CustomerName, OrderTotal FROM OPENROWSET(
  BULK 'sales_orders/*.csv',
  DATA_SOURCE = 'files',
  FORMAT = 'CSV',
  PARSER_VERSION = '2.0',
  HEADER_ROW = TRUE

) AS source_data
WHERE OrderType = 'Special Order';


--- oR 
CREATE EXTERNAL TABLE SpecialOrders
    WITH (
        -- details for storing results
        LOCATION = 'special_orders/',
        DATA_SOURCE = files,
        FILE_FORMAT = ParquetFormat
    )
AS
SELECT OrderID, CustomerName, OrderTotal
FROM
    OPENROWSET(
        -- details for reading source files
        BULK 'https://mystorage.blob.core.windows.net/data/sales_orders/*.csv',
        FORMAT = 'CSV',
        PARSER_VERSION = '2.0',
        HEADER_ROW = TRUE
    ) AS source_data
WHERE OrderType = 'Special Order';

-- DROP 

DROP EXTERNAL TABLE SpecialOrders;
```

> it's important to understand that external tables are a metadata abstraction over the files that contain the actual data. Dropping an external table does not delete the underlying files.

### Encapsulate data transformations in a stored procedure

```SQL
CREATE PROCEDURE usp_special_orders_by_year @order_year INT
AS
BEGIN

 -- Drop the table if it already exists
 IF EXISTS (
                SELECT * FROM sys.external_tables
                WHERE name = 'SpecialOrders'
            )
        DROP EXTERNAL TABLE SpecialOrders

 -- Create external table with special orders
 -- from the specified year
 CREATE EXTERNAL TABLE SpecialOrders
  WITH (
   LOCATION = 'special_orders/',
   DATA_SOURCE = files,
   FILE_FORMAT = ParquetFormat
  )
 AS
 SELECT OrderID, CustomerName, OrderTotal
 FROM
  OPENROWSET(
   BULK 'sales_orders/*.csv',
   DATA_SOURCE = 'files',
   FORMAT = 'CSV',
   PARSER_VERSION = '2.0',
   HEADER_ROW = TRUE
  ) AS source_data
 WHERE OrderType = 'Special Order'
 AND YEAR(OrderDate) = @order_year
END
```

***Benefits of using SP***

- Reduces client to server network traffic
  - commands in a procedure are executed as a single batch of code; which can significantly reduce network traffic between the server and client because only the call to execute the procedure is sent across the network.
- Provides a security boundary
  - Multiple users and client programs can perform operations on underlying database objects through a procedure, even if the users and programs don't have direct permissions on those underlying object
- Eases maintenance
  - ny changes in the logic or file system locations involved in the data transformation can be applied only to the stored procedure; without requiring updates to client applications or other calling functions.
- Improved performance
  - compiled the first time they're executed, and the resulting execution plan is held in the cache and reused on subsequent runs of the same stored procedure. As a result, it takes less time to process the procedure.
