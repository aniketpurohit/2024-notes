# Creating Database Objects

the physical objects are related to the organization of the data on the physical device(disk). The DB Engine's physical objects are files and filegroups.

Logical objects represents a user's view of database. Database, tables, columns, and views are example of logical view.

The first DB object that has to be created is a database itself. The DB Engine manages both the system ad user DB. An Authorized user can create user databases, while system DB are generated during the installation of DB.

## Creation of DB

```sql
CREATE DATABASE db_name [ON [PRIMARY] {file_spec1},...]
    [LOG ON {file_spec2}, ...]
     [COLLATE collation_name]
    [FOR {ATTACH |ATTACH_REBUILD_LOG}]
```

- db_name is the name of database. (max 128 chars)
- maximum number of database managed by single system is 32,767
- All DB are stored in files. these files can be explicitly specified by the system administrator or implicitly provided by the system.

> The DB engine uses disk files to store data. Each disk file contains data pf single DB.

- ON specifies the files explicitly. **file_spec1** represents a file specification which includes further options like name of file, the physical name, and size.
- A login account of DB engine that is used to create a DB is called DB Owner. A DB can have one owner, who correspond to the login account name. The login account, which is DB owner, has the special name **dbo**.
- **dbo** uses  LOG ON option define one or more physical destination of the transaction log of the DB. IF LOG ON option is not defined, the transaction logs still be created because every DB must have at least one transaction log file.
- The COLLATE option, you can specify the default collation for the DB. if not specified, DB is assigned to the default collation model database.
- FOR ATTACH option specifies DB is created by attaching an existing set of files. if this option is used you must specify the PRIMARY FIRST.
- creation of new DB, The DB engine uses the **model** DB as a template.

Example :

```sql
USE master;
CREATE DATABASE projects 
  ON (NAME = projects_dats, 
    FILENAME ='C:\TEMP\projects.mdf',
    SIZE=10,
    MAXSIZE = 100,
    FILEGROWTH = 5)
  LOG ON 
    (NAME=projects.log,
      FILENAME='c:\temp\projects.ldf',
      SIZE=40,
      MAXSIZE =100,
      FILEGROWTH =10);
```

> if you have a DB object that should exist in each user DB, you should create that object in model DB

### Creation of a DB snapshot

The `CREATE DATABASE`  statement can be used to create a DB snapshot of an existing DB. A DB snapshot is transactional consistent with the source DB as it existed at the time of snapshot's creation

```sql
CREATE DATABASE database_snapshot_name
    ON (NAME = logical_file_name, FILENAME ='os_file_name') [,..n]
        AS SNAPSHOT of source_database_name
```

- the snapshot file contains only modified data has a changed from the source from the source database.
- process of creating a DB snapshot must include the logical name of each file from the source DB as well as new corresponding physical name.
- To create snapshots of a database, you need NTFS disk volumes, because only such volumes support the sparse file technology that is used for storing snapshots.
- usually used as a mechanism to protect data against user errors.

EXAMPLE of SNAPSHOT

```sql
USE master;
CREATE DATABASE AdventureWorks_snapshot
  ON (NAME = 'AdventureWorks_Data',
    FILENAME= 'C:\temp\snapshot_DB.mdf',
    ) AS SNAPSHOT of AdventureWorks;
```

### Attaching and Detaching

- a database can be detached and then attached to the same or another database server.
- should be done if you want to move the DB.
- you can detach a DB from DB server by using **sp_detach_db** system procedure.
- when you attach a DB, all data files must be available.

## Create TABLE: A BASIC FORM

- creates a new base table with all corresponding column and their data types.

```sql
CREATE TABLE table_name
    (col_name1 type1 [not null | null]
    [{, col_name2 type2 [not null |null]....}])
```

**table_name** is the name of table

- maximum number of tables per DB is limited by the number of objects in DB

> the name of DB object can generally contain four parts [server_name.[db_name.[schema_name.]]]object_name.

- **object_name** is the name of DB object **schema_name** name of the schema to which the object belongs. **Server_name** and **db_name** are the names of the server an database object belongs
- A database object is always created within a schema of a DB. A user can create a table only in a schema for which he/she has ALTER permissions. Any user in the **sysadmin**, or **db_ddladmin**or, **db_owner** can create a table in any schema.

- you should always specify the table name together with the corresponding schema name.

EXAMPLEs

```sql
USE sample;
CREATE TABLE employee(
  emp_no INTEGER NOT NULL,
  emp_fname CHAR(20) NOT NULL,
  emp_lname CHAR(20) NOT NULL,
  dept_no CHAR NULL
);

CREATE TABLE Item_Attributes  ( 
  item_id INT NOT NULL, 
  attribute NVARCHAR(30) NOT NULL, 
  value SQL_VARIANT NOT NULL, 
  PRIMARY KEY (item_id, attribute)
  );
```

Temporary tables are special kind of the base table. They are stored in the **tempdb** database and are automatically dropped at the end of session.

Beside the data  type and the nullability, the column specification can contain:

- DEFAULT :
  - specifies default value of the column.
- IDENTITY
  - allows integer only, which are implicitly assigned by the system.
  
### CREATE TABLE and Declarative Integrity Constraints

Constraints are used to check the modification or insertion of data, are called *constraints*.

- Increased reliability of data
  - Integrity constraint must be defined only once in DB whereas in application everywhere that data is used.
  - application enforced constraints are usually more complex to code than are of DB
  - the modification of structure in application programs requires teh modification of every program that involves the corresponding code .

- Reduced programming time
- Simple maintenance

There are two groups of integrity constraints handled by a DBMS.

- Declarative integrity constraints.
- Procedural integrity constraint that are handled by triggers.

Declarative constraint are defined using DDL statements `CREATE TABLE` and `ALTER TABLE`
 Column-level
constraints, together with the data type and other column properties, are placed within the declaration of the column, while table-level constraints are always defined at the end of the `CREATE TABLE` or `ALTER TABLE` statement, after the definition of all columns

Each declarative constraint has a name. name can be explicitly assigned using `CONSTRAINT` option in the `CREATE TABLE` statement  or the `ALTER TABLE`. If the `CONSTRAINT` option is omitted, the database Engine assigns an implicit name for the constraint

All declarative constraints can be categorized into several groups

#### DEFAULT clause

- we have already learnt it

#### UNIQUE Clause

- All columns or group that qualify to be primary keys are called
*candidate keys*. Each candidate key is defined using the `UNIQUE` clause in the `CREATE TABLE` or `ALTER TABLE` statement.

```sql
[CONSTRAINT c_name] UNIQUE [CLUSTERED| NONCLUSTERED] (col_name1 ,...)
```

The `CONSTRAINT` option `UNIQUE` clause assigns an explicit name to the candidate jey. the Option `CLUSTERED or NONCLUSTERED` relates to The DB engine always generates order of rows is specified using the indexed order of teh column values. if order is not specified  `NONCLUSTERED`.

> the maximum number of columns per candidate key is 16

```sql
USE sample;
CREATE TABLE projects (
  project_no CHAR DEFAULT 'p1',
  project_name CHAR(15) NOT NULL,
  budget FLOAT NULL
  CONSTRAINT unique_no UNIQUE (project_no)
);
```

#### PRIMARY KEY clause

*primary key* of a table is a column or group of columns whose is different in every row.

SYNTAX

```sql
[CONSTRAINT c_name] PRIMARY KEY [CLUSTERED | NONCLUSTERED] ({col_name1},...)
```

in contrast to the `UNIQUE`, the `PRIMARY KEY` column must be `NOT NULL` and its default value is `CLUSTERED`
It is a column level constraint

EXAMPLE:

```sql
USE sample;
CREATE TABLE employee(
  emp_no INTEGER NOT NULL,
  emp_fname CHAR(20) NOT NULL,
  emp_lname CHAR(20) NOT NULL,
  dept_no CHAR NULL,
  CONSTRAINT prim_empl PRIMARY KEY (emp_no)
)

/*
same query other ways
*/
CREATE TABLE employee(
  emp_no INTEGER NOT NULL CONSTRAINT prim_empl PRIMARY KEY,
  emp_fname CHAR(20) NOT NULL,
  emp_lname CHAR(20) NOT NULL,
  dept_no CHAR NULL
)
```

#### CHECK Clause

*check constraint* specifies conditions for the data  inserted into a column.
SYNTAX:

```sql
[CONSTRAINT c_name] CHECK [NOT FOR REPLICATION] expression
```

**expression** must evaluate to a Boolean value and can reference any column in current table.

EXAMPLE:

```sql
USE sample;
CREATE TABLE customer(
  cust_no INTEGER NOT NULL,
  cust_group CHAR NULL,
  CHECK (cust_group IN ('c1', 'c2', 'c3'))
);
-- the customer must belongs to the one of the groups c1, c2, c3
```

#### FOREIGN KEY

*foreign key* is a column or group of columns in one table that contains values that match the primary values in the same or another table.

SYNTAX

```SQL
[CONSTRAINT c_name] 
  [[FOREIGN KEY] ({col_name1},....)]
  REFERENCES table_name ({col_name2},...)
    [ON DELETE {NO ACTION | CASCADE | SET NULL | SET DEFAULT}]
    [ON UPDATE {NO ACTION | CASCADE | SET NULL | SET DEFAULT}]
```

- defines all columns explicitly that belongs to the foreign key.
- the references specifies the table name with all column that build the corresponding  primary key.
- the number and datatype of columns in FOREIGN KEY must match number of corresponding PRIMARY KEY.
- The table that contains the foreign key is called the *referencing table*, and the table that contains the corresponding primary key is called the *parent table or referenced table*.

EXAMPLE

```SQL
USE sample;
CREATE TABLE works_on (
  emp_no INTEGER NOT NULL, 
  project_no CHAR NOT NULL, 
  job CHAR (15) NULL, 
  enter_date DATE NULL, 
  CONSTRAINT prim_works PRIMARY KEY(emp_no, project_no), 
  CONSTRAINT foreign_works FOREIGN KEY(emp_no) 
    REFERENCES employee (emp_no)
);
```

- The FOREIGN KEY clause can be omitted if the foreign key is defined as a column-level constraint, because the column being constrained is the implicit column “list” of the foreign key, and the keyword REFERENCES is sufficient to indicate what kind of constraint this is
- it imposes referential Integrity.

#### REFERENTIAL Integrity

*referential integrity* enforces insert and update rules for the tables with the foreign key and the corresponding primary key constraint.

#### *Possible problem with referential integrity*

**CASE 1** Insert a new row into *reference table* for which data is not available in parent table.
*WHAT HAPPENS* the DB Engine rejects the insertion of new row.

**CASE 2** Modify the data of *reference table* for which data is not present in *Parent table* (in case of above SQL query )
*WHAT HAPPENS* The DB Engine rejects the modification of rows in *reference table*

**CASE 3** Modify the employee number in the parent table
*WHAT HAPPENS* if the referenced table is using the data that will be modified in the parent table. it will reject the changes on parent table.

**CASE 4** Delete of rows in parent table
*WHAT HAPPENS* the deletion would remove the employee for which matching rows exists in the referencing table.

#### ON DELETE and ON UPDATE Options

- **NO ACTION**
  - allows you to modify (update or delete) only those values of the parent table do have any corresponding values in foreign key of the referencing table.

- **CASCADE**
  - allows you to modify all values of the parent table.
  - A row ion referencing table is modified if the corresponding value in the primary key of the parent has been updated.

- **SET NULL**
  - allows you to modify all values of the parent table.
  - update a value of parent table and this modification would lead to data inconsistences in the referencing table to NULL.

- **SET DEFAULT**
  - Analogous to SET NULL option, with one exception: all corresponding values in the foreign key are set to a default value.

### Creating Other Database Objects

- views
  - virtual tables
  - a view is derived from one or more table
  - no physical storage is needed.

- INDEX
  - a new index on a specified table.
  - the indices are primarily used to allow efficient access to the data stored on a disk.
  
- Stored procedure
  - can be created using the corresponding `CREATE PROCEDURE` statement
  
- trigger
  - specifies an action as a result of an operation.

- synonym
  - object that provides a link between itself and another object manged by the same or a linked database server.

- schema
  - includes statements for creation of table, views and user privileges.
  > can think of schema as a construct that collects together several tables, corresponding views, and user privileges.
  - a schema is defined as a collection of database objects that is owned by a single principal and forms a single namespace. A namespace is a set of objects that cannot have duplicate names.

### Integrity Constants and Domains

A *domain* is the set of all possible legitimate values of a table may contain. Use of data types to define the set of all possible values.

FOR example zip code : we need to use CHECK to implement correctly.
The T-SQL provide support for domains by creating alias data types using `CREATE TYPE` statement.

#### Alias Data Types

- defined by user using a existing base data types.
- can be used with `CREATE TABLE` statement to define one or more columns.

SYNTAX :

```SQL
CREATE TYPE [type_schema_name.] type_name{
  [FROM base_type[(precision[,scale])][NULL | NOT NULL ]]
  | [EXTERNAL NAME assembly_name {.class_name}]
}
```

EXAMPLE:

```sql
USE sample;
CREATE TYPE zip FROM SMALLINT NOT NULL;
```

> GENERALLY, DB Engine implicitly converts between compatible columns of different data types. This is valid for alias data types too

#### CLR Data Types

- The CREATE TYPE statement can also be applied to create a user-defined data type using .NET.
- the implementation of a user-defined data type is defined in a class of an assembly in the Common Language Runtime (CLR).

## Modifying Database Objects

### Altering a Database

- changes the physical structure of a database
- allows  changing the following properties of a database
  - Add or remove one or more database files, log files, or filegroups
  - Modify file or filegroup properties
  - Set database options
  - Change the name of the database using the sp_rename stored procedure

#### Adding or Removing Database Files, Log Files, or Filegroups

`ALTER DATABASE` statement allows the addition and removal of database files.
clauses `ADD FILE` and `REMOVE FILE` specify the addition of a new file and the deletion of an existing file, respectively.

EXAMPLE:

```SQL
USE master;

GO 
ALTER DATABASE projects 
ADD FILE (NAME=projects_dat1, 
FILENAME = 'C:\temp\projects1.mdf',   SIZE = 10, 
MAXSIZE = 100,   FILEGROWTH = 5);
```

The REMOVE FILE clause removes one or more files that belong to an existing  database. The file can be a data file or a log file. The file cannot be removed unless it is empty.
e CREATE FILEGROUP clause creates a new filegroup, while DELETE FILEGROUP removes an existing filegroup from the system. you cannot remove a filegroup unless it is empty

### Modifying File or Filegroup Properties

can use the `MODIFY FILE` clause to change the following file properties:

- Change the logical name of a file using the NEWNAME option of the `MODIFY FILE` clause
- Increase the value of the SIZE property
- Change the FILENAME, MAXSIZE, or FILEGROWTH property
- Mark the file as OFFLINE

can use the `MODIFY FILEGROUP` clause to change the following filegroup
properties:

- Change the name of a filegroup using the NAME option of the `MODIFY FILEGROUP` clause.
- Mark the filegroup as the default filegroup using the DEFAULT option
- Mark the filegroup as read-only or read-write using the `READ_ONLY` or `READ_WRITE` option

#### Setting Database Options

-used to set different database options.

- Some options must be set to ON or OFF, but most of them have a list of possible values
- database option has a default value, which is set in the model database.
All options that you can set are divided into several groups:
- State options
- Auto options
- SQL options

state options control the following:

- User access to the database (options are SINGLE_USER, RESTRICTED_USER, and MULTI_USER)
- The status of the database (options are ONLINE, OFFLINE, and EMERGENCY)
- The read/write modus (options are READ_ONLY and READ_WRITE)

> SQL options control the ANSI compliance of the database and its objects
>All SQL options can be edited using the DATABASEPROPERTYEX function and modified using the ALTER DATABASE statement

### Storing FILESTREAM Data

FILESTREAM storage has to be enabled at two levels:

- For the Windows operating system
- For the particular database server instanc

SQL Server Configuration Manager to enable FILESTREAM storage at the OS
level.
open SQL Server Configuration Manager, type SQLServerManager15.msc in the Search field for SQL Server 2019 or type SQLServerManager14.msc for SQL Server 2017.

FILESTEAM ACCESS LEVEL

***method -1***

- Disabled FILESTREAM storage is not allowed
- Transact-SQL Access Enabled FILESTREAM data can be accessed using T-SQL statements.
- Full Access Enabled FILESTREAM data can be accessed using T-SQL as well as from the OS.

***method -2***

- use the sp_configure system procedure with the filestream access level option:

```SQL
EXEC sp_configure filestream_access _level, 2
RECONFIGURE

-- value 2 means "FULL Access Enabled"
```

### Contained database

One of the significant problems with SQL Server database is that they cannot be exported (or imported ) easily.
Attaching and de-attaching has many important parts missing (security in general and existing login in particular )

A contained database comprises all database setting and data required to specify the database and is isolated from the instance of the database engine on which it is installed.

- Fully contained DB
  - DB objects cannot cross the application boundary.
  - An application boundary defines the scope of an application.
- Partially contained DB
  - allow database objects to cross the application boundary,
- Nonconatined DB
  - do not support the notion of an application boundary at all.

## altering A table

- modifies the schema of the table.
  - Add or drop one or more columns
  - Modify column properties
  - Add or remove disable objects
  - Enable or disable constraint
  - rename tables another DB objects

### Adding or Dropping a Column

```SQL
-- ADD clause 

USE sample;
ALTER TABLE employee ADD telephone_no CHAR(12) NULL;

-- DROP Clause 
ALTER TABLE employee DROP COLUMN telephone_no;
```

### Modifying Column properties

- Data type
- Nullability

```SQL
USE sample;
ALTER TABLE department ALTER COLUMN location CHAR(12) NOT NULL;
```

## Adding or Removing Integrity Constraints

```SQL
USE sample;

CREATE TABLE sales 
  (order_no INTEGER NOT NULL,
  order_date DATE NOT nULL,
  ship_date DATE NOT NULL);
  GO 
  ALTER TABLE SALES 
    ADD CONSTRAINT ORDER_CHECK CHECK(ORDER_DATE <= SHIP_DATE>)

  -- add CONSTRAINT
  ALTER TABLE SALES ADD CONSTRAINT PRIMARYK_SALES PRIMARY KEY(ORDER_NO);

  -- DROP CONSTRAINT
  ALTER TABLE SALES DROP CONSTRAINT ORDER_CHECK;
```

## Enabling or Disabling COnstraint

an integrity constraint always has a name that can be explicitly declared using the `CONSTRAINT`option or implicitly declared by the system. the name of all declared constraint for a table can be viewed by `sp_helpconstraint`

```sql
ALTER TABLE sales NOCHECK CONSTRAINT ALL;
```

> Use of NOCHECK option is not recommended. Any constraint violations that are suppressed may cause updates to fail.

### Rename Table and Other Database objects

`sp_rename` system procedure modifies the name of an existing table

```SQL
USE sample;
EXEC sp_rename @objname= department,@newname = subdivision
-- changes the name from department to subdivision
```

> Do not use `sp_rename` system procedure, because changing object names can be influence other database objects that reference them.

### Removing DB Objects

used to remove DB object have the following general form:
`DROP object_type object_name`

remove one or more database
`DROP TABLE table_name1 {,....}`
> all data, indices, and triggers belonging to the removed table are also dropped. All views that are defined using the dropped table are not removed.

Can also drop

- TYPE
- SYNONYM
- PROCEDURE
- INDEX
- VIEW
- TRIGGER
- SCHEMA
