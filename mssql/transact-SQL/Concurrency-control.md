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
