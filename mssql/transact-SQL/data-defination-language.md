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

Temporary tables are special kind of the base table. They are stored in the **tempdb** database and are automatically dropped at the end of session.

Beside the data  type and the nullability, the column specification can contain:

- DEFAULT :
  - specifies default value of the column.
- IDENTITY
  - allows integer only, which are implicitly assigned by the system.
  
### a database can be detached and then attached to the same or another database server
