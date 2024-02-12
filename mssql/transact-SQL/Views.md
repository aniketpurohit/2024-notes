# Introduction

- Views by default do not exists physically (except for indexed views)
- Views are database objects that are always derived from one or more base tables (or views) using metadata information
- information (including the name of the view and the way the rows from the base tables are to be retrieved) is the only information concerning views that is physically stored.
- views are also called *virtual tables*

## Create a View

- by using `CREATE VIEW`

```SQL
CREATE VIEW view_name [{column_list}]
    WITH [{ENCRYPTION | SCHEMABINDING | VIEW_METADATA}]
    AS select_Statement
    [WITH CHECK OPTION]
```

- view_name is the name of defined view.
- column_list is the list of names to be used for columns in a view.
- select_statement specifies the SELEct statement that retrieves rows and columns from one or more tables
- The SCHEMABINDING clause binds the view to the schema of the underlying table. When SCHEMABINDING is specified, the base table or tables cannot be modified in a way that would affect the view definition

### Purpose of Views

- To restrict use of a particular columns/ rows of table. views can be used for controlling access to a particular part
- To hide the details of complicated queries. If database applications need queries that involve complicated join operations, the creation of corresponding views can simplify the use of such queries.
- To restrict inserted and updated values to certain ranges.

EXAMPLE

```SQL
USE sample;
Create VIEW v_count (project_no, count_project)
AS SELECT project_no, COUNT(*) FROM works_on GROUP BY project_no;
```

## Altering and Removing Views

- Transact-SQL language supports the nonstandard ALTER VIEW statement, which is used to modify the definition of the view query

```SQL
ALTER VIEW v_without_budget AS SELECT project_no, project_name
FROM project WHERE project_no >= 'p3';
```

- DROP VIEW statement removes the definition of the specified view from the system tables

```SQL
DROP VIEW v_count;
```

> If you delete a view, on which another view is dependent then, it will throw an error which is binding error (4413)

## DML Statement and Views

### View Retrieval

```SQL
CREATE VIEW v_d2 
    AS SELECT emp_no, emp_lname 
    FROM employee 
        WHERE dept_no ='d2'; 
GO 
SELECT emp_lname 
    FROM v_d2 
    WHERE emp_lname LIKE 'J%';
```

### INSERT Statement and a View

When a view is used to insert rows, the rows are actually inserted into the underlying base table.
It is generally impossible to insert a row that does not statify the conditions of the view query's WHERE clause.

```SQL
CREATE VIEW v_2016_check 
    AS SELECT emp_no, project_no, enter_date FROM works_on 
    WHERE enter_date BETWEEN '01.01.2016' AND '12.31.2016' WITH CHECK OPTION;

INSERT INTO v_2016_check 
    VALUES (22334, 'p2', '1.15.2017')

-- This will failed because condition is not met.

CREATE VIEW v_2016_nocheck 
    AS SELECT emp_no, project_no, enter_date FROM works_on 
    WHERE enter_date BETWEEN '01.01.2016' AND '12.31.2016' WITH CHECK OPTION;

INSERT INTO v_2016_nocheck 
    VALUES (22334, 'p2', '1.15.2017')

-- The insert is successful but you can see the changes in view
```

the insertion of rows into the underlying tables is not possible if the corresponding view contains any of the following features

- The FROM clause in view definition involves two or more tables and the column list includes columns more than one table.
- A column of view is derived from an aggregate function.
- SELEcT in view contains GROUP BY clause or the DISTINCT option.
- A column of view is derived from a constant or an expression.

## UPDATE statement and a View

```SQL
CREATE VIEW v_p1 
    AS SELECT emp_no, job 
    FROM works_on 
    WHERE project_no = 'p1'; 
GO 
UPDATE v_p1 
    SET job = NULL 
    WHERE job = 'Manager';
```

the modification of columns in the underlying tables in not possible if the corresponding view contains any of the following features.

- The FROM clause in the view definition involves two or more tables and the column list includes columns from more than one table.
- The SELECT statement in the view contains the GROUP BY clause or DISTINCT option.
- A column of the view is derived from an aggregate function
- A column of view that is derived from a constant or an expression

```SQL
CREATE VIEW v_uk_pound (project_number, budget_in_pounds) 
AS SELECT project_no, budget*0.65 
FROM project 
WHERE budget > 100000; 
```

## DELETE Statement and a View

```SQL
CREATE VIEW v_project_p1 
AS SELECT emp_no, job 
FROM works_on 
WHERE project_no = 'p1'; 
GO 
DELETE FROM v_project_p1 
WHERE job = 'Clerk';
```

The deletion of rows in the underlying tables is not possible if the corresponding view contains any of the following features:

- The FROM clause in the view definition involves two or more tables and the column list includes columns from more than one table.
- A column of the view is derived from an aggregate function.
- The SELECT statement in the view contains the GROUP BY clause or the DISTINCT option.

## Editing Information Concerning Views

- sys.views displays additional information about existing views.
- the system procedure sp_helptext, you can display the query belonging to a particular view
