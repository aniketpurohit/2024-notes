# Modification of Table's Content

## INSERT STATEMENT

- inserts rows (or parts of them ) into a table

SYNTAX

```SQL
-- exactly one row is inserted into the corresponding table.
INSERT [INTO] tab_name [(col_list)]
    DEFAULT VALUES | VALUES ({DEFAULT | NULL | expression} [,....n]);

-- inserts the result set from SELECT statement
INSERT INTO tab_name|view_name [(col_list)]
    {select_statement | execute_statement};

-- ***To ensure compatibility, all character-based values and data and time data must be enclosed in apostrophes, while all numeric values need no such enclosing.***
```

### Inserting a Single row

- explicit specification of the column list is optional.

```SQL
INSERT INTO employee VALUES (25348, 'Matthew', 'Smith','d3'); 
INSERT INTO employee VALUES (10102, 'Ann', 'Jones','d3'); 
INSERT INTO employee VALUES (18316, 'John', 'Barrimore', 'd1');

INSERT INTO department VALUES ('d1', 'Research', 'Dallas'); 
INSERT INTO department VALUES ('d2', 'Accounting', 'Seattle'); 
INSERT INTO department VALUES ('d3', 'Marketing', 'Dallas');

INSERT INTO employee VALUES (15201, 'Dave', 'Davis', NULL);
-- explicit use of the keyword NULL inserts the null value into the corresponding column.
```

### Inserting a Multiple rows

- inserts one or more rows selected with a subquery.

```SQL
CREATE TABLE dallas_dept 
    (dept_no CHAR(4) NOT NULL, 
    dept_name CHAR(20) NOT NULL); 

-- The second form of insert statement
INSERT INTO dallas_dept (dept_no, dept_name) 
    SELECT dept_no, dept_name 
         FROM department 
         WHERE location = 'Dallas';
```

### Table Value Constructors and INSERT

- A table (or row) value constructor allows you to assign several tuples (rows) with a DML statement such as INSERT or UPDATE

```SQL
 INSERT INTO department VALUES  
    ('d4', 'Human Resources', 'Chicago'),  
    ('d5', 'Distribution', 'New Orleans'), 
    ('d6', 'Sales', 'Chicago');
```

## UPDATE Statement

- modifies values of table rows

```SQL
UPDATE tab_name 
    SET column_1 = {expression | DEFAULT | NULL} [,...n] 
    [FROM tab_name1 [,...n]]; 
    [WHERE condition]
```

> An UPDATE statement can modify data of a single table only
> always use with WHERE clause

```SQL

UPDATE works_on 
   SET job = 'Manager' 
   WHERE emp_no = 18316 
   AND project_no = 'p2';


UPDATE works_on 
    SET job = NULL 
    WHERE emp_no IN 
    (SELECT emp_no 
        FROM employee 
        WHERE emp_lname = 'Jones');

-- identical to above query 
UPDATE works_on 
  SET job = NULL 
   FROM works_on, employee 
   WHERE emp_lname = 'Jones' 
   AND works_on.emp_no = employee.emp_no;


UPDATE project 
  SET budget = CASE 
    WHEN budget >0 and budget < 100000  THEN budget*1.2 
    WHEN budget >= 100000 and budget < 200000  THEN budget*1.1 
    ELSE budget*1.05 
    END
```

> The FROM clause is a Transact-SQL extension to the ANSI SQL standard.

## DELETE

- deletes rows from a table.

```sql
DELETE FROM table_name  
[WHERE predicate];

DELETE table_name 
    FROM table_name [,...n] 
    [WHERE condition];
```

- Explicitly naming columns within the DELETE statement is not necessary (or allowed), because the DELETE statement operates on rows and not on columns
- If the WHERE clause is omitted, all rows of a table will be deleted.

```sql
USE sample; 
DELETE FROM works_on 
   WHERE job = 'Manager';

DELETE FROM works_on 
    WHERE emp_no IN 
    (SELECT emp_no 
         FROM employee 
         WHERE emp_lname = 'Moser'); 
DELETE FROM employee 
    WHERE emp_lname = 'Moser'
```

## Other T-SQL Modification Statements and Clauses

### TRUNCATE

- normally provides a “faster executing” version of the DELETE statement without the WHERE clause.
- The TRUNCATE TABLE statement deletes all rows from a table more quickly than does the DELETE statement because it drops the contents of the table page by page, while DELETE drops the contents row by row.

```sql
TRUNCATE TABLE table_name
```

### MERGE

- MERGE statement combines the sequence of conditional INSERT, UPDATE, and DELETE statements in a single atomic statement, depending on the existence of a record.
- If a row in the new data corresponds to an item that already exists in the table, an UPDATE or a DELETE statement is performed. Otherwise, an INSERT statement is performed.

```sql
MERGE INTO bonus B 
   USING (SELECT project_no, budget 
                    FROM project) E 
          ON (B.pr_no = E.project_no) 
         WHEN MATCHED THEN 
                    UPDATE SET B.bonus = E.budget * 0.1 
         WHEN NOT MATCHED THEN 
                    INSERT (pr_no, bonus) 
                           VALUES (E.project_no, E.budget * 0.05);
```

### OUTPUT Clause

- result of the execution of an INSERT, UPDATE, or DELETE statement contains by default only the text concerning the number of modified rows
- If the content of such a result doesn’t fit your needs, you can use the OUTPUT clause, which displays explicitly the rows that are inserted or updated in the table or deleted from it

```sql
DECLARE @del_table TABLE (emp_no INT, emp_lname CHAR(20)); 
DELETE employee 
OUTPUT DELETED.emp_no, DELETED.emp_lname INTO @del_table 
WHERE emp_no > 15000; 
SELECT * FROM @del_table;
```
