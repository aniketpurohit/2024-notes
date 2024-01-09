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

**CASE 1** Insert a new row into *refrence table* for which data is not available in parent table.
*WHAT HAPPENS* the DB Engine rejects the insertion of new row.

**CASE 2** Modify the data of *reference table* for which data is not present in *Parent table* (in case of above SQL query )
*WHAT HAPPENS* The DB Engine rejects the modification of rows in *reference table*
