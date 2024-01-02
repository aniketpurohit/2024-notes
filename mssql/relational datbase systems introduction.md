# An Overview

A database system is made up of the following parts/component:

1. **Database application programs**

    - special-purpose software that is designed and implemented by users or third-party.

2. **Client components**

    - general-purpose database software designed and implemented by a database company.
    - using client components, user can access data stored on the same computer or remote computer.

3. **database server(s)**

    - task of server is to manage data stored in a database.
    - each client communicated with a db by using queries.

4. **databases**

    - Users view db as a collection of data that is logically belongs together.
    - for a db system, a database is simply a series of bytes, usually stored on disk.
    - the db system needs to provide not only interfaces that enables users to create database and retrieve or modify data, but also system components to mange the stored data.
    - must provide
        - variety of user interface
        - Physical data independence
        - Logical data independence
        - Query optimization
        - Data integrity
        - Concurrency control
        - backup or recovery
        - database security

## Explanation about database must provide

**variety of user interface**
A user interface can be either graphical or textual.

**physical data independence**
the database application programs do not depend on the physical structure of the stored data in a database. It enables to make changes to the stored data without having any changes to database program. the modification in physical data should not affect existing database applications or the existing database *schema*.

**logical data independence**
In file processing, the declaration of files is done in application programs, so any change to the structure of the file usually requires modification of all program using it. it is used to make changes the logical structure of database without having to  make any changes to the database application programs.

**Query optimization**
Most database systems contain a sub-component called an optimizer that considers a variety of possible execution strategies for querying the data and then selects the most efficient one. The selected strategy is called the execution plan of the query.

**Data Integrity**
One of the tasks of a database system is to identify logically inconsistent data and reject its storage in a database. Additionally, most real-life problems that are implemented using database systems have integrity constraints that must hold true for the data. task of maintaining integrity can be handled by the user in application programs or by the database management system (DBMS). As much as possible, this task should be handled by the DBMS.

**Concurrency Control**
many user applications access a database at the same time. Therefore, each database system must have some kind of control mechanism to ensure that several applications that are trying to update the same data do so in some controlled way.

**Backup and Recovery**
A database system must have a subsystem that is responsible for recovery from hardware or software errors.

**Database Security**
important database security concepts are authentication and authorization.

## Relational Database Systems

In Microsoft SQL Server called the Database Engine is a relational database system.
> A data model is a collection of concepts, their relationships, and their constraints that are used to represent data of a real-world problem.
user’s point of view, a relational database contains tables and nothing but tables.

**General properties of relational database system**

- Rows in a table do not have any particular order.
- Columns in a table do not have any particular order.
- Every column must have a unique name within a table. columns from different tables may have the same name.
- Every single data item in the table must be single valued.
- For every table, there is usually one column with the property that no two rows have the same combination of data values for all table columns. In the relational data model, such an identifier is called a candidate key. If there is more than one candidate key within a table, the database designer designates one of them as the primary key of the table.
- In a table, there are never two identical rows. (This property is only theoretical;)

### SQL: A relational database language

SQL Server uses Transact-SQL (T-SQL). SQL is a set-oriented language. (The former are also called record-oriented languages.) This means that SQL can query many rows from one or more tables using just one statement.  SQL is its non-procedurality.
SQL contains two sub-languages: a data definition language (DDL) and a data manipulation language (DML). DDL statements are used to describe the schema of database tables.  DML encompasses all operations that manipulate the data.
There are always four generic operations for manipulating the database retrieval, insertion, deletion, and modification.

### Database Design

Designing a database is a very important phase in the database life cycle, which precedes all other phases except the requirements collection and the analysis.
bad design problems

1. resulting database will most likely not meet the user requirements concerning performance
2. superfluous data redundancy, which in itself has two disadvantages: the existence of data anomalies and the use of an unnecessary amount of disk space.

Normalization of data is a process during which the existing tables of a database are tested to find certain dependencies between the columns of a table.  A functional dependency means that by using the known value of  one column, the corresponding value of another column can always be uniquely determined.

The functional dependencies between columns A and B
is denoted by A ⇒ B, specifying that a value of column A can always be used to determine the corresponding value of column B. (“B is functionally dependent on A.”) empid to empname
a column is dependent upon the primary key of a table, is called trivial functional dependency.

### Normal Forms

Normal forms are used for the process of normalization of data and therefore for the database design.

**First Normal Form**
First normal form (1NF) means that a table has no multi-valued attributes or composite attributes.  the value of any column in a row must be atomic—that is, single valued.

**Second Normal Form**
A table is in second normal form (2NF) if it is in 1NF and there is no non-key column dependent on a partial primary key of that table. This means if (A,B) is a combination of two table columns building the key, then there is no column of the table depending either on only A or only B.

**Third Normal Form**
A table is in third normal form (3NF) if it is in 2NF and there are no functional dependencies between non-key columns.

cont from page 11 entity relation
