# SQL Server Editions and Management Tools

## SQL Server Editions

- **Express Edition**
  - the lightweight version of SQL Server deigned for use by application developers.
  - the product support Common Language Runtime (CLR)
  - SSMS enables to easily manage a database.

- **Standard Edition**
  - for small and medium-sized business.
  - supports up to four processors and includes the full range of BI functionality, including Analysis Services, Reporting Services, and Integration Services

- **Enterprise Edition**
  - intended for time-critical applications with a huge number of users.
  - data partitioning and online database maintenance

- **Developer Edition**
  - Designed for developers to build and test any type of application with SQL Server.
  - Each license of Developer Edition entitles one developer to use the software on as many systems as necessary; additional developers can use the software by purchasing additional licenses.

## Management Tools

- **SQL Server Management Studio(SSMS)**
  - primary tool for interacting with SQL server system on Windows is SQL Server management.

- **Azure Data Studio**
  - similar to SSMS.
  - SSMS is implemented for Windows whereas Data Studio is implemented for linux, Windows, and macOS.
  - SSMS is a mature tool, whereas Data Studio is new tool supports a subset of features already implemented in SSMS.

- **SQL Server Configuration manager**
  - tool to manage the services associated with SQL Server.
  - to configure the network protocols used by SQL server.
  - manage connectivity configuration from SQL Server client computers.

  - **SQL Server profiler**
    - SQL server Profiler is a graphical tool lets system admin monitor and record database and server activities.
  - **Database Engine tuning Advisor**
    - allows to automate the physical design of your database.
  - **SQL Server Data Tools**
    - SQL server data tools (SSDT) transform database development by introducing a model that spans all phases of database development

## planning Phase

- **Which operating System will be used**
Since SQl server 2017, the instances of system can be installed and used additionally on Linux and in Docker containers, which opens the possibility of running SQL Server on macOS.

- ### Which SQL Server Components should be Used ?

There are two groups of features on the Feature Selection page: **instance features** and **shared features**

**Instance features** are the components that are installed once for each instance, meaning you have multiple copies of them (one for each instance).**Shared features** are features that are common across all instances on a given machine.

#### instance features

- Database Engine Services. Database Engine is the relational database system of SQL Server
- SQL Server Replication  allows you to replicate data from one system to another.
- Full-Text and Semantic Extractions for Search (aka Full-Text Search). The Database Engine allows you to store structured data in columns of relational tables. By contrast, the unstructured data is primarily stored as text in file systems.Full-Text Search is a component of SQL Server that allows you to store and query unstructured data.
- Data Quality Services   related to Data Quality Client.
- PolyBase is a component of SQL
Server that builds a gateway from SQL to Hadoop. This functionality has been available for several years in the Microsoft Analytics Platform System (APS) and is now an integrated part of SQL Server

- ### Where Will the Root Directory Be Stored?

root directory is where the Setup program stores all program files and those files that do not change as you use the SQL Server system.
By default, the installation process stores all program files in the subdirectory Microsoft SQL Server, although you can change this setting during the installation process.

- ### Should Multiple Instances of the Database Engine Be Used?

An instance is a database server that does not share its system and user databases with other instances (servers).

there are 2 types of instance Default and named

When SQL Server is installed in the default instance, it does not require a client to specify the name of the instance to make a connection.
Any instance of the database server other than the default instance is called a named instance. To identify a named instance, you have to specify its name as well as the name of the computer on which the instance is running.

The main purpose of multiple instances is to divide databases that exist in your organization into different groups
A single-processor machine will not be the right hardware platform to run multiple instances of the Database Engine, because of limited resources.
