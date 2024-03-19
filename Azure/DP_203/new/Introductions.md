# Introductions

## type of data

|Structured|Semi-structured|Unstructured|
|:---:|:---:|:---:|
|Structured data primarily comes from table-based source systems|Semi-structured data is data such as JavaScript object notation (JSON) files, which may require flattening prior to loading into your source system|Unstructured data includes data stored as key-value pairs that don't adhere to standard relational model|
|The primary element of a structured file is that the rows and columns are aligned consistently throughout the file.| When flattened, this data doesn't have to fit neatly into a table structure.|that are commonly used include portable data format (PDF), word processor documents, and images.

## Data operations

### Data ingestion

Data Integration involves establishing links between operational and analytical services and data sources to enable secure, reliable access to data across multiple systems.

### Data transformation

Operational data usually needs to be transformed into suitable structure and format for analysis, often as part of an extract, transform, and load (ETL) process; though increasingly a variation in which you extract, load, and transform (ELT) the data is used to quickly ingest the data into a data lake and then apply "big data" processing techniques to transform it.

### data consolidation

Data consolidation is the process of combining data that has been extracted from multiple data sources into a consistent structure - usually to support analytics and reporting.

## important data engineering concepts

### Operational and Analytical data

- Operational data is usually transactional data that is generated and stored by applications, often in a relational or non-relational database.
- Analytical data is data that has been optimized for analysis and reporting, often in a data warehouse.

### Streaming data

- Streaming data refers to perpetual sources of data that generate data values in real-time, often relating to specific events.
- solutions that capture real-time stream of data and ingest them into analytical data systems, often combining the real-time data with other application data that is processed in batches

### data Pipelines

- Data pipelines are used to orchestrate activities that transfer and transform data.
- peatable extract, transform, and load (ETL) solutions that can be triggered based on a schedule or in response to events.

### Data lakes

- A data lake is a storage repository that holds large amounts of data in native, raw formats.
- Data lake stores are optimized for scaling to massive volumes (terabytes or petabytes) of data. The data typically comes from multiple heterogeneous sources, and may be structured, semi-structured, or unstructured.
- The idea with a data lake is to store everything in its original, untransformed state. This approach differs from a traditional data warehouse, which transforms and processes the data at the time of ingestion.

### Data Warehouses

- A data warehouse is a centralized repository of integrated data from one or more disparate sources. Data warehouses store current and historical data in relational tables that are organized into a schema that optimizes performance for analytical queries.
- designing and implementing relational data warehouses, and managing regular data loads into tables.

### Apache Spark

- Apache Spark is a parallel processing framework that takes advantage of in-memory processing and a distributed file storage. It's a common open-source software (OSS) tool for big data scenarios.

## data Engineering in microsoft Azure

![data engineering in microsoft azure](https://learn.microsoft.com/en-us/training/wwl-data-ai/introduction-to-data-engineering-azure/media/3-data-engineering-azure.png)

This operational data must be captured, ingested, and consolidated into analytical stores; from where it can be modeled and visualized in reports and dashboards.

The core Azure technologies used to implement data engineering workloads include:

- Synapse Analytics
- Data lake storage gen2
- stream analytics
- Data factory
- Databricks

## data lake gen 2

A data lake provides file-based storage, usually in a distributed file system that supports high scalability for massive volumes of data. Organizations can store structured, semi-structured, and unstructured files in the data lake and then consume them from there in big data processing technologies, such as Apache Spark

A data lake is a repository of data that is stored in its natural format, usually as blobs or files.

Data Lake Storage builds on Azure Blob storage capabilities to optimize it specifically for analytics workloads. This integration enables analytics performance, the tiering and data lifecycle management capabilities of Blob storage, and the high-availability, security, and durability capabilities of Azure Storage

### Benefits

Data Lake Storage is designed to deal with this variety and volume of data at exabyte scale while securely handling hundreds of gigabytes of throughput

### Hadoop compatible access

- A benefit of Data Lake Storage is that you can treat the data as if it's stored in a Hadoop Distributed File System (HDFS).

### Security

Data Lake Storage supports access control lists (ACLs) and Portable Operating System Interface (POSIX) permissions that don't inherit the permissions of the parent directory.

This security is configurable through technologies such as Hive and Spark or utilities such as Azure Storage Explorer, which runs on Windows, macOS, and Linux. All data that is stored is encrypted at rest by using either Microsoft or customer-managed keys.

### Performance

Azure Data Lake Storage organizes the stored data into a hierarchy of directories and subdirectories.  data processing requires less computational resources, reducing both the time and cost

### Data redundancy

Data Lake Storage takes advantage of the Azure Blob replication models that provide data redundancy in a single data center with locally redundant storage (LRS), or to a secondary region by using the Geo-redundant storage (GRS) option.

### Azure Blob lake store vs Blob Storage

you can store large amounts of unstructured ("object") data in a flat namespace within a blob container. Blob names can include "/" characters to organize blobs into virtual "folders", but in terms of blob manageability the blobs are stored as a single-level hierarchy in a flat namespace.

![BLOB storage](https://learn.microsoft.com/en-us/training/data-ai-cert/introduction-to-azure-data-lake-storage/media/blob-store.png)

Azure Data Lake Storage Gen2 builds on blob storage and optimizes I/O of high-volume data by using a hierarchical namespace that organizes blob data into directories, and stores metadata about each directory and the files within it.

![Data lake storage](https://learn.microsoft.com/en-us/training/data-ai-cert/introduction-to-azure-data-lake-storage/media/data-lake.png)

There are four stages for processing big data solutions that are common to all architectures:

- Ingest
  - used to acquire the source data.
  - for batch movement of data, pipelines in Azure Synapse Analytics or Azure Data Factory may be the most appropriate technology to use. For real-time ingestion of data, Apache Kafka for HDInsight or Stream Analytics may be an appropriate choice.
- Store
  - where the ingested data should be placed.
  - Azure Data Lake Storage Gen2 provides a secure and scalable storage solution that is compatible with commonly used big data processing technologies.
- Prep and train
  - used to perform data preparation and model training and scoring for machine learning solutions.
- Model and Serve
  - involves the technologies that will present the data to users like PowerBI

## Four Common type analytical technique

- descriptive
  - What is happening in my business?
  - through the creation of a data warehouse in which historical data is persisted in relational tables for multidimensional modeling and reporting.

- Diagnostic
  - Why is it happening?
  - This may involve exploring information that already exists in a data warehouse, but typically involves a wider search of your data estate to find more data to support this type of analysis.

- Predictive
  - What is likely to happen in the future based on previous trends and patterns?

- Prescriptive
  - Enables autonomous decision making based on real-time or near real-time analysis of data, using predictive analytics

![four common types of analytical technique](https://learn.microsoft.com/en-us/training/wwl-data-ai/introduction-azure-synapse-analytics/media/types-analytics.png)

## Introduction

Azure Synapse Analytics provides a cloud platform for all of these analytical workloads through support for multiple data storage, processing, and analysis technologies in a single, integrated solution.

Azure Synapse Analytics combines a centralized service for data storage and processing with an extensible architecture through which linked services enable you to integrate commonly used data stores, processing platforms, and visualization tools.

### Working with files in a data lake

One of the core resources in a Synapse Analytics workspace is a data lake, in which data files can be stored and processed at scale

Data is extracted from multiple operational sources and transferred to a central data lake or data warehouse for analysis. Azure Synapse Analytics includes built-in support for creating, running, and managing pipelines that orchestrate the activities necessary to retrieve data from a range of sources, transform the data as required, and load the resulting transformed data into an analytical store.

> Pipelines in Azure Synapse Analytics are based on the same underlying technology as Azure Data Factory

### Querying and manipulating data with SQL

Azure Synapse Analytics supports SQL-based data querying and manipulation through two kinds of SQL pool that are based on the SQL Server relational database engine:

A built-in serverless pool that is optimized for using relational SQL semantics to query file-based data in a data lake.
Custom dedicated SQL pools that host relational data warehouses.

The Azure Synapse SQL system uses a distributed query processing model to parallelize SQL operations, resulting in a highly scalable solution for relational data processing. You can use the built-in serverless pool for cost-effective analysis and processing of file data in the data lake, and use dedicated SQL pools to create relational data warehouses for enterprise data modeling and reporting.

### Processing and analyzing data with Apache Spark

 you can create one or more Spark pools and use interactive notebooks to combine code and notes as you build solutions for data analytics, machine learning, and data visualization.

### Exploring data with Data Explorer

- based on the Azure Data Explorer service
- Data Explorer uses an intuitive query syntax named Kusto Query Language (KQL) to enable high performance, low-latency analysis of batch and streaming data.

### Integrating with other Azure data services

can be integrated with other Azure data services for end-to-end analytics solutions

1. Azure synapse link

- enables near-realtime synchronization between operational data in Azure Cosmos DB, Azure SQL Database, SQL Server, and Microsoft Power Platform Dataverse and analytical data storage that can be queried in Azure Synapse Analytics.

2. PowerBI

- Enables data analysts to integrate a Power BI workspace into a Synapse workspace, and perform interactive data visualization

3. Purview

- enables organizations to catalog data assets in Azure Synapse Analytics, and makes it easier for data engineers to find data assets and track data lineage when implementing data pipelines that ingest data into Azure Synapse Analytics.

4. Machine Learning

- enables data analysts and data scientists to integrate predictive model training and consumption into analytical solutions.

### When to use Azure Synapse Analytics

- Large-scale data warehousing
- Advanced analytics
- Data exploration and discovery
- Real time analytics
- Integrated analytics
- Integrated analytics
