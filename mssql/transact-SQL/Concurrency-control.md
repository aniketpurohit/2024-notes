# Concurrency Models

## Pessimistic Concurrency

- uses locks to block access to data that is used by another process at the same time.
- Assumes that a conflict between two or more processes can occur at any time and therefore locks resources as they are required, for the duration of a transaction.
- pessimistic concurrency issues exclusive locks for data being modified so that no other processes can read or modify that data.

## Optimistic concurrency

- works on the assumption that a transaction is unlikely to modify data that another transaction is modifying at the same time
- a process that modifies the data can do so without any limitation, because all other processes that read the same data access the saved versions of the data
- only conflict scenario occurs when two or more write operations use the same data. In that case, the system displays an error so that the client application can handle it

## Transactions

A transaction specifies a sequence of T-SQL statements that is used by DB programmers to package read and write operations, so that DB system can guarantee the consistency of data.

- Implicit
  - specifies any INSERT, UPDATE or DELETE statement as a transaction unit
- Explicit
  - A group of T-SQL statements, where the beginning and end of the group are marked using statements such as `BEGIN TRANSACTION`, `COMMIT` and `ROLLBACK`

```SQL
BEGIN TRANSACTION /* the beginning of transaction */
UPDATE employee
  SET emp_no=39831
  WHERE emp_no = 10102
  IF(@@error <>0)
    ROLLBACK /* rollback the transaction */

UPDATE works_on
  SET emp_no=39831
  WHERE emp_no = 10102
  IF(@@error <>0)
    ROLLBACK
COMMIT /* the end of transaction */

```

### properties of Transactions

the acronym ACID stands for Atomicity, Consistency, Isolation, Durability.

- Atomicity
  - guarantees the indivisibility of set of statements that modifies data ina database and is part of a transaction
- Consistency
  - will not allow the database to contain inconsistent data.
- isolation
  - separates concurrent transactions from each other. In other words, an active connection can't see the data modification in a concurrent and incomplete transaction.
- Durability
  - persistence of data.
  - ensures that the effects of particular transaction persist even if a system error occurs.
  - If a system error occurs while a transaction is active, all statements of that transaction wil be undone.
  
## T-SQL statement and transactions

- `BEGIN TRANSACTION`
  - starts the transaction
  - transaction_name is name assigned to the transaction, which can be used only on the outermost pair of nested `BEGIN TRANSACTION/COMMIT`
  - @trans_var is the name of a user-defined variable containing a valid transaction name
  - WITH MARK option specifies that the transaction is to be marked in
the log.
  - . description is a string that describes the mark. If WITH MARK is used, a transaction name must be specified.

  ```SQL
    BEGIN TRANSACTION [{transaction_name | @trasns_var} {WITH MARK ['description']}]
  ```

- `BEGIN DISTRIBUTED TRANSACTION`
  - specifies the start of a distributed transaction managed by the Microsoft Distributed Transaction Coordinator (DTC)
  - one that involves databases on more than one server.

- `COMMIT [WORK]`
  - successfully ends the transaction started with the BEGIN TRANSACTION statement.
  - `WORK` clause is optional

- `ROLLBACK [WORK]`
  - reports an unsuccessful end of the transaction.
  - they assume that the database might be in an inconsistent state.

- `SAVE TRANSACTION`
  - sets a save point within a transaction.
  - *Savepoint* marks a specified point within transaction so that all updates that follow can be canceled without cancelling the entire transaction.

- `SET IMPLICIT_TRANSACTION`
  - DB engine provide implicit transaction or compliance with the SQL standard.
  - When a session operates in implicit transaction,selected statements implicitly issue the BEGIN TRANSACTION statement
  
The global variable @@trancount contains the number of active transactions for the current user.

```SQL
BEGIN TRANSACTION
INSERT INTO department (dept_no, dept_name) VALUES ('d4' , 'Sales');
SAVE TRANSACTION a;
INSERT INTO department(dept_no, dept_name) VALUES ('d5', 'Research');
SAVE TRANSACTION b;  
INSERT INTO department (dept_no, dept_name) 
     VALUES ('d6', 'Management'); 
ROLLBACK TRANSACTION b; 
INSERT INTO department (dept_no, dept_name) 
   VALUES ('d7', 'Support'); 
ROLLBACK TRANSACTION a; 
COMMIT TRANSACTION;
```

### Transaction LOG

The DB Engine keeps all stored records, in particular the before and after values in one or more files called *transaction log*.
Each database has its own transaction log. Thus, if it is necessary to roll back one or more modification operations executed on the tables of current DB.

### Before Images, After images and Write-Ahead log

The transaction log is used to roll back or restore a transaction.
The process in which before images from the transaction log are used to roll back all modification is called undo activity.
After images are modified values that are used to roll forward all modifications since the start of the transaction. This process is called the redo activity and is applied during recovery of a database.

Database Engine (and all other relational database systems) writes data changes to a log before the transaction is committed. This process is called write-ahead logging. Hence, the task of write-ahead logging is to provide high availability and consistency in case of failure.

### Delayed Durability

- enables transactions to continue running as if the data, prepared for logging, had been flushed to disk.
- All write operations to disk are deferred and are sent to disk together with write operation of other transactions.
- the system uses 60 KB chunk of log buffer and attempts to flush the log to disk when this 60 KB is full/
- SET clause delayed durability. This options has 3 options
  - `ALLOWED`
    - any individual transaction can be use delayed durability.
  - `FORCED`
    - all transaction that can use delayed durability will use it.

  - `DISABLED`

the main advantage achieved by application contain mainly short transaction and when a log diak is slow.
`COMMIT TRANSACTION WITH (DELAYED_DURABILITY = ON);`

### Editing Information Concerning Transactions and Logs

There are several dynamic management views that can be used to display different information concerning transactions and logs.

- `sys.dm_tran_active_transactions`
  - DVM returns information about transactions of the particular DB engine instance.
  - transaction_id column provides the unique ID number of each transaction
  - transaction_begin_time columns displays the starting time of each transactions
  - transaction_type column provide the type of particular transaction
    1. for read/write transaction
    2. for read/only transaction
    3. for system transaction
  - name specifies the transaction name

  ```SQL
  SELECT transaction_id ID, transaction_begin_time start, transaction_type type FROM sys.dm_tran_active_transactions; 
  ```

- `sys.dm_tran_database_transactions`
  - displays detailed information about the transactions occurring on your DB engine instance.
  - provides snapshot data, so the result may vary each time.
  -
- `sys.dm_db_log_space_usage`
- `sys.dm_db_log_stats`
