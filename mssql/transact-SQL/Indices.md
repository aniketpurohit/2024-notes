# introduction to Indices

If a table does not have an appropriate index, the database system uses the table scan method to retrieve rows
Table scan means that each row is retrieved and examined in sequence
(from first to last) and returned in the result set if the search condition in the WHERE clause
evaluates to TRUE.

Indices are stored in additional data structures called index pages.
For each indexed row there is an index entry, which is stored in an index page.

The Database Engine’s indices are constructed using the B+-tree data structure.

Index access is generally the preferred and obviously advantageous method for accessing tables with many rows. With index access, it takes only a few I/O operations to find any row of a table in a very short time, whereas sequential access (i.e., table scan) requires much more time to find a row physically stored at the end of the table

![B+-tree for the emp_no column of the employee table](../img/B-tree-example.png)

## Clustered Indices

A clustered index determines the physical order of the data in a table.
Database Engine allows the creation of a single clustered index per table, because the rows of the table cannot be physically ordered more than one way.

When using a clustered index, the system navigates down from the root of the B+-tree structure to the leaf nodes, which are linked together in a doubly linked list called a page chain.
its leaf contain data page

If a clustered index in defined for a table, the table is called a *clustered table*.

![Physical structure of a clustered index](../img/physical-structure-of-clustered-index.png)

- clustered index is built by default for each table for which you define the primary key using the primary key constraint.
- each clustered index is unique by default
- If a clustered index is built on a nonunique column, the Database Engine will force uniqueness by adding a 4-byte identifier to the rows that have duplicate values.

## Nonclustered indices

- A nonclustered index does not change the physical order of the rows in the table.
- The leaf pages of a nonclustered index consist of an index key plus a bookmark.

- A bookmark of a nonclustered index shows where to find the row corresponding to the index key.

- If a clustered index exists, the bookmark of the nonclustered index shows the B+-tree structure of the table’s clustered index. If the table has no clustered index, the bookmark is identical to the row identifier (RID), which contains three parts: the address of the file to which the corresponding table belongs, the address of the physical block (page) in which the row is stored, and the offset, which is the position of the row inside the page.

- **Heap**
  - Traversal of the nonclustered index structure is followed by arrival of the rows the RID.

- **Clustered table**
  - Traversal of the nonclustered index structure id followed by traversal of the corresponding clustered index.

![structure of nonclustered index](../img/structure-of-non-clustered-index.png)

## Creating Indices

SYNTAX

```SQL
CREATE [UNIQUE] [CLUSTERED |NONCLUSTERED] INDEX index_name 
    ON table_name (column1 [ASC | DESC] ,...) 
           [ INCLUDE ( column_name [ ,... ] ) ] 
 [WITH 
[FILLFACTOR=n] 
[[, ] PAD_INDEX = {ON | OFF}] 
[[, ] DROP_EXISTING = {ON | OFF}] 
[[, ] SORT_IN_TEMPDB = {ON | OFF}] 
[[, ] IGNORE_DUP_KEY = {ON | OFF}] 
              [[, ] ALLOW_ROW_LOCKS = {ON | OFF}] 
              [[, ] ALLOW_PAGE_LOCKS = {ON | OFF}] 
[[, ] STATISTICS_NORECOMPUTE = {ON | OFF}] 
              [[, ] ONLINE = {ON | OFF}]] 
              [ON file_group | "default"]
```

- index_name identifies the name of the created index
- column1 is the name of the column for which the index is created
- The maximum size of an index is 900 bytes, while the index can contain up to 16 columns.
- The UNIQUE option specifies that each data value can appear only once in an indexed column.
- The CLUSTERED option specifies a clustered index. The NONCLUSTERED option (the default) specifies that the index does not change the order of the rows in the table.  The Database Engine allows a maximum of 249 nonclustered indices per table.
- Descending indices should be used when you create a composite
index on columns that have opposite sorting directions
- The INCLUDE option allows you to specify the nonkey columns, which are added to the leaf pages of the nonclustered index.
- Significant performance gains can be achieved when all columns in a query are included in the index, because the query optimizer can locate all the column values within the index pages without having to access pages with table data. This feature is called a covering index or covered query.
- FILLFACTOR=n defines the storage percentage for each index page at the time the index is
created.
- The PAD_INDEX option is tightly connected to the FILLFACTOR option. The FILLFACTOR option mainly specifies the percentage of space that is left free on leaf index pages. The PAD_INDEX option specifies that the FILLFACTOR setting should be applied to the index pages as well as to the data pages in the index.
- The DROP_EXISTING option allows you to enhance performance when re-creating a clustered index on a table that also has a nonclustered index.
- The SORT_IN_TEMPDB option is used to place into the tempdb system database the data from intermediate sort operations used while creating the index
- The IGNORE_DUP_KEY option causes the system to ignore the attempt to insert duplicate values in the indexed column(s).
- ALLOW_ROW_LOCKS option specifies that the system uses row locks when this option is activated (set to ON).
- ALLOW_PAGE_LOCKS option specifies that the system uses page locks when this option is set to ON
- The STATISTICS_NORECOMPUTE option specifies that statistics of the specified index  should not be automatically recomputed. (
