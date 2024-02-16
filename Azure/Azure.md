## Data Operations

### Data Integration 
- establishing links between Operational and analytical services and data sources to enable secure, reliable access to daata across multiple systems.
### Data transformation 
- tranform the data into suitable structure and format for analysis, often as a part of an *ETL* process
- data is prepared to support analytical needs
### Data consolidation
- combining data that has been extracted from multiple data source into a consistent structure. 

## Concepts 

### Operational and analytical data 
- **Operational**
  - transacrional data that is generated and stored by application.
- **Analytical**
  - data that has been optimized for analysis and reporting 
  - often in a data wareshouse

### Streaming Data 
- to prepetual sources of data that generate data values in real-time, often relating to specific events
- common sources includes IoT device and social media feeds.


### Data Pipelines
- orchestrtate activities that transfer and transfrom data
- primary way to implement repeatable extract, transfrom , load solutions based on schedule.

### Data Lakes
- storage repository holds large amount of data in native, raw formats.
- optimized for scaling to massive volumes (terabytes or petabytes) of data.
- data typically comes form multiple heterogeneous sources and may be structures, semi-structured, or unstructured.

### data warehouse
- centralized repository of inegrated data from one or more disparate source.
- stores current and historical data in relational tables are organized into a schema that optimizing peformance for anlytical queries.

### Apache spark 
- parallel processing framework that takes advantage of in-memory processing and a distributed file storage.
- It's common open-source software (OSS) tool for big data scenarios

- ![data engineering in microdsoft Azure](https://learn.microsoft.com/en-us/training/wwl-data-ai/introduction-to-data-engineering-azure/media/3-data-engineering-azure.png)

## Azure data Lake storage Gen2
- provides filebased storage, usually in a distributed file system that supports high scalability for based storage
- combines a file system with a storage platform to help you quickly indetify insights inot your data.
- enables analytics performance, the tiering and data lifecycle management capabilities of Blob storage, and high-availability, security and durability capabilities of Azure Storage.

### benefits 
- can use Data lake storage gen2 as the basis for both real-time and batch solutions.
- **Hadoop compatible access**
  - ability to use storage mechanisms such as parquet format, which is highly compressed and performs well across multiple platforms using an internal columnar storage.
- **security**
  -  supports access control lists(ACLs) and portable Operating System Interface (POSIX) permissions that don't inherit the permission of parent directory.
  -  All data that is stored is encryped at rest by using Microsoft or customer-managed keys.
-  **Performance**
  - organizes the stored data into a hierarchy of directories and subdirectories, much like file system.
  - data processing requires less computational resources, reducing both the time and cost.
- **Data redundancy**
  - takes advantage of Azure Blob replication models that provide data redundancy in a single center with locally redundant storage (LRS), or GRS.

### Enable Azure Data lake storage GEN2
- Azure Data lake storage Gen2 isn't a standalone Azure service, but rather a configurable of **StorgaeV2**.
- To enable from Storage account, you can select option **Enable Hierarchial namespace** in the **Advanced** page when creating the storage account

### Comparison Azure Data Lake Store to Azure Blob storage 
**In Azure Blob**
- large amounts of unstructured ("object") data in a flat namespace within a blob container
- can include "/" characters to organize blobs into virtual "folders", but in terms of blob manageability the blobs are stored as a single-level hierarchy in a flat namespace.
- can access this data by using HTTP or HTTPs

**Azure Data Lake Storage Gen2**
- builds on blob storage and optimizes I/O of high-volume data by using a hierarchical namespace that organizes blob data into directories, and stores metadata about each directory and the files within it.
- 
