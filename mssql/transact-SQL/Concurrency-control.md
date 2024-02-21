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
  -  specifies the start of a distributed transaction managed by the Microsoft Distributed Transaction Coordinator (DTC)
  -  one that involves databases on more than one server.
  - 

- `COMMIT [WORK]`
  - successfully ends the transaction started with the BEGIN TRANSACTION statement. 
  - 
- `ROLLBACK [WORK]`
- `SAVE TRANSACTION`
- `SET IMPLICIT_TRANSACTION`
