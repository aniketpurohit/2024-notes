# Queries

## SELECT statement

- one basic statement for retrieving information from a DB.
- result of a `SELECT` statement is another table, also known as *result set*

SYNTAX:

```SQL
SELECT [ALL | DISTINCT] column_list FROM{table1 {tab_alias1}, ....};
```

- *alias* is another name for corresponding table and can be used as shorthand way to refer the table.

***Column_list***

- the asterisk (*), specifies all columns of the named tables in the FROM clause.
- explicit specification of column names to be retrieved.
- specification column_name [AS] column_heading can replace name of column or to assign a new name to an expression.
- an expression
- a system or an aggregate function

> A `SELECT` statement can retrieve either columns or rows from a table. the first operation is called *SELECT list (or projection)* and the second one is called *selection*. the combination of both operation is also possible in a SELECT statement.

```SQL
SELECT select_list 
    [INTO new_table] FROM table
    [WHERE search_condition]
    [GROUP BY group_by_expression]
    [HAVING search_condition]
    [ORDER BY order_expression [ASC|DESC]];
```

### WHERE Clause

- define one or more conditions that limit the selected rows.
- specifies a boolean expression.if expression is true, then the row is returned, if it is false, it is discarded.

| comparison operator | Description |
|:---: | :---|
|<> (or !=)| not equal|
|<| less than|
|>|greater than|
|>=| greater than or equal |
|<= |less than or equal|
|!>|not greater than|
|!<| not less than|

```SQL
USE sample;

SELECT dept_name, dept_no FROM department WHERE location = 'Dallas';

SELECT emp_lname, emp_fname FROM employee where emp_no >= 15000;

SELECT project_name FROM project WHERE budget*0.51 > 60000;
```

> Comparisons of strings are executed in accordance with collating sequence in effect ('sort order' specified when DB engine is installed).
> FOR ASCII one character is in lower priority than the other if it appears in the code table before the other one.
> Two string with different lengths are compared after the shorter one is padded at the right with blanks, so the length of both strings are equal.
> Numbers are compare algebraically
> value of temporal data types compare in chronological order.

### Boolean operators

- multiple conditions can be built using Boolean operators `AND, OR, NOT`

```SQL
SELECT project_no,emp_no from works_on
where project_no ='p1' OR project_no='p2';

-- illegal statements will throw error
SELECt emp_fname, DISTINCT emp_no 
from employee where emp_lname ='Moser'; 
-- DISTINCT option can be used only once in SELECT list. and it must precede all column names in list.
```

the where clause may include any number of the same or different Boolean operations.
> NOT has the highest priority after that AND and at last OR
> Use parentheses to improve readability and reduce the possibility of errors.
> negation of NULL is NULL

### In and Between operators

`IN` operator allow the specification of two or more expressions to be used for a query search.

```SQL
SELECT emp_no, emp_fname, emp_lname from employee where emp_no IN (29346, 28559, 25348);
```

An `IN` operator is equivalent to a series of conditions, connected with one or more OR operators.

`BETWEEN` operator specifies a range, which determines the lower and upper bounds of qualifying values.

```SQL
SELECT project_name, budget from project where budget Between 95000 and 120000;
```

- `BETWEEN` is range inclusive

### Queries involving NULL values

All comparisons with `NULL` values returns False. to retrieve the rows with `NULL` values we will use `is null`
`column IS [NOT] NULL`

```SQL
-- syntax correct but flawed logic
SELECT project_no, job from works_on where job <> NULL;

-- syntax correct with correct logic
SELECT project_no, job from works_on where job IS NOT NULL;

--
SELECT emp_no, ISNULL(job, 'job unknown') AS task from works_on where project_no ='p1'
```

### LIKE operator

- used for pattern matching, compares values with a specified pattern.
- **pattern** may be string or expression  and must be compatible with the data type of the corresponding column.
- Certain characters within pattern called *wildcard characters* have a specific interpretation.
  - % any sequence of zero or more characters
  - _ any single characters

```SQL
SELECt emp_fname, emp_lname, emp_no FROM employee WHERE emp_fname LIKE '_a%';

-- all dept whose location begins with a character in range C through F 
SELECT dept_no, dept_name, location FROM department WHERE location LIKE '[C-F]%'


--  numbers and first and last names of all employees whose last name does not begin with the letter J, K, L, M, N, or O and whose first name does not begin with the letter E or Z:

SELECT emp_no, emp_fname, emp_lname FROM employee WHERE emp_lname LIKE '[^J-O]%'  AND emp_fname LIKE '[^EZ]%';

--  full details of all employees whose first name does not end with the character n

SELECT emp_no, emp_fname, emp_lname FROM employee WHERE emp_fname NOT LIKE '%n' ;


```

> Any wildcard within square brackets stands for itself or equivalent feature is available in ESCAPE option

```SQL
SELECT project_no, project_name FROM project WHERE project_name LIKE '%[_]%';

-- OR 
SELECT project_no, project_name FROM project WHERE project_name LIKE '%!_%' ESCAPE '!';
```

### GROUP BY clause

defines one or more columns as a group such that all rows within any group have same values for those columns.

```SQL

USE sample;
SELECT job FROM works_on GROUP BY job
```

> Each columns appearing  in the select clause must also appear in `GROUP BY` clause. this restriction is not applied to constants that are part of aggregate function.

## Aggregate Functions

### Convenient aggregate functions

supports SIX aggregate functions

- all aggregate function  operate on a single argument, which can be a column or an expression.

> The only exception is the second form of COUNT and COUNT_BIG
> the aggregate function appear in the `SELECT` list, which can include a `GROUP BY` clause. If there is no `GROUP BY` clause in `SELECT` statement, and the select list must include at least one aggregate functions.

```SQL
-- an illegal statement 

USE sample;
SELECT emp_lname, MIN(emp_no) FROM employee;
/*
EXPLANATION
emp_lname column of the column employee table must not appear in the SELECT list 
because it is not the argument of an aggregate function. On the other hand 
all column names that are not arguments of an aggregate function may appear in select list if they are used  for grouping
*/

```

- **ALL**
  - indicates that all values of a column are to be considered.

- **DISTINCT**
  - Eliminates duplicate values of a column before the aggregate function is applied.

#### MIN AND MAX

- provides the lowest and highest values in the column.

```SQL
USE sample;

-- provide the minimum employee no in the table Employee
SELECT MIN(emp_no) as min_employee_no FROM Employee;

-- number  and last name of employee with the lowest employee number
SELECT emp_no, emp_lname FROM Employee WHERE emp_no = (
  SELECT MIN(emp_no) FROM employee;
)

-- employee number of the manager who entered last in the works_on table
SELECT emp_no FROM works_on WHERE enter_date = (
  SELECT MAX(enter_date) from works_on WHERE job='Manager'
)

-- the DISTINCT option cannot be used with the aggregate functions MIN and MAX.
-- ALL NULL values in the columns that are the argument of the aggregate function MIN or MAX are always eliminated before MIN or MAX is applied.
```

#### SUM

calculate the sum of values in the column. the argument of the function SUM must be numeric.

```SQL
SELECT SUM(budget) sum_of_budgets from projects;

-- the use of syntax for GROUP BY clause is recommended because it defines a grouping explicitly. 

SELECT SUM(budget) sum_of budgets from projects GROUP BY();
```

#### AVG

calculates the average of the values in the column. the argument of function `AVG` must be numeric. all `NULL` values are eliminated

```SQL
SELECt AVG(budget) avg_budget FROM project WHERE budget > 100000
```

#### COUNT and COUNT_BIG

aggregate function `COUNT` has two

```SQL
COUNT([DISTINCT] col_name)
COUNT(*)
```

the first form calculates the number of values in the **col_name** column. `DISTINCT` keyword is used, all duplication values are eliminated before `COUNT` is applied.

```SQL
SELECT project_no, COUNT(DISTINCT job) job_count FROM works_on 
GROUP BY project_no;
```

> `COUNT(*)` counts the number of rows in the table. returns the number of rows for which the `WHERE` condition is True.

```SQL
SELECT job, COUNT(*) job_count
FROM works_on
GROUP BY job;
```

> COUNT_BIG always returns a value of teh BIGINT data types, while COUNT function always return a value of INTEGER data types

### Statical Aggregate Functions

[[details in the ]]

#### VAR

computes the variance of all values listed in a column or expression.

#### VARP

computes the variance for the population of all the values listed in a column or expression

#### STDEV

computes standard deviation (is computed as the square root of corresponding variance ) of all the values listed in the column or expression

#### STDEVP

computes the standard deviation for the population of all values listed in a column or expression

### User-Defined Aggregate Functions

[[will mention the page link]]

## HAVING Clause

define the condition is then applied to groups of rows. clause has the same meaning to groups of rows that `WHERE` clause has to be content of the corresponding table.

```SQL
SELECT project_no FROM works_on
  GROUP BY project_no
  HAVING COUNT(*) <4;

-- it counts the number of rows in each group and select those groups with three or fewer rows.

SELECT job FROM works_on 
GROUP BY job
HAVING job LIKE 'M%';
```

## ORDER BY

defines particular order of the rows in the results of a query.

```SQL
ORDER BY {[col_name | col_number [ASC | DESC]]}, ....
```

the **col_number** is the alternative specification that identifies the column by its ordinal position in the sequence of all columns in the `SELECt` list DESC indicates descending order, with ASC as the default value.

```SQL
SELECT emp_fname, emp_lname. dept_no 
  FROM employee
  WHERE emp_no < 20000
  ORDER BY emp_lname , emp_fname;
```

use of column names instead of columns names is an alternative solution  if the order criterion contains any aggregate function.
using column names rather than numbers in the ORDER BY clause is recommended, to reduce the difficulty of maintaining the query if any columns need to be added or deleted from the SELECT list.

```SQL
SELECT project_no, COUNT(*) emp_quantity 
  FROM works_on
  GROUP BY project_no
  ORDER BY 2 DESC
  
-- T-SQL language orders NULL values at the beginning of all values if the order is ascending and orders them at the end values if the order is descending
```

## Using ORDER BY to Support Paging

server-side paging generally provides better performance, because only the rows needed for printing are sent to the client.
Database Engine supports two clauses in relation to server-side paging: OFFSET and FETCH.

```SQL
SELECT BusinessEntityID, JobTitle, BirthDate 
  FROM HumanResources.Employee
  WHERE Gender='F'
  ORDER BY JobTitle
  OFFSET 20  rows
  FETCH NEXT 10 ROWS ONLY;
```

THE `OFFSET` clause specifies the number of rows to skip before starting to return the rows. This is evaluated the `ORDER BY` clause is evaluated and the rows are sorted. THE `FETCH NEXT` clause specifies the number of number of rows to retrieve.

## SELECT Statement and IDENTITY Property

the `IDENTITY` property allows to specify a counter of values for a specific column of a table.

- columns with numeric data types, `TINYINT`, `SMALLINT`, `INT`,`BIGINT`
you can the `IDENTITY` property to let the system generate unique numeric values for the table column of your choice.

```SQL
CREATE TABLE product
  (product_no INTEGER IDENTITY(10000,1) NOT NULL,
  product_name CHAR(30) NOT NULL,
  price MONEY
  );
  SELECT $identity 
    FROM product 
    WHERE product_name ='soap';
```

Some system functions and variables are related to the `IDENTITY` property. uses the `$identity` variable.
> starting  value and increment of the column with `IDENTITY` property, you can use the `IDENT_SEED` and `IDENT_INCR` functions

```SQL
SELECT IDENT_SEED('product'), INDENT_INCR('product');
```

the system automatically sets identity values. If you want to supply you own values for particular row, you must set the IDENTITY_INSERT option ON before the explicit value be inserted.

```SQL
SET IDENTITY_INSERT table_name ON
```

IDENTITY_INSERT option can be used to specify any values for a column with the IDENTITY property, IDENTITY does not generally enforce uniqueness.

## CREATE SEQUENCE statement

Using `IDENTITY` property has several significant disadvantages, the most important of which are the following:

- can  use it only with specified table.
- cannot obtain the new value before using it.
- can specify the `IDENTITY` property only when the column is created.

THE DB Engine offers another solution called `SEQUENCES`.
A `SEQUENCE` has the same semantics as the IDENTITY property but doesn't have the limitations.

- enables you to specify a counter of values for different database objects, such as columns and variables.

```SQL
CREATE SEQUENCE dbo.Sequence1
  AS INT
  START WITH 1 INCREMENT BY 5
  MINVALUE 1 MAXVALUE 256
  CYCLE;

  -- START specify the initial value for sequence called Sequence1 
  -- INCREMENT clause defines teh incremental value.
  -- MINVALUE or MAXVALUE defines the specifies minimal and maximum value of 
  -- the CYCLE specifies it should restart from minimum value
  -- default for CYCLE is no cycle 

```

> It is a table-independent
the `NEXT VALUE FOR` expression can be used to create new sequence values

```SQL
SELECT NEXT VALUE FOR dbo.sequence1;
SELECT NEXT VALUE FOR dbo.sequence1;
```

> can use the catalog view called ***sys.sequence*** to check the current value of the sequence, without using it.

```SQL
SELECT current_value from sys.sequences where name  = 'sequences'
```

`ALTER SEQUENCE` statement modifies the properties of an existing sequence. use si in the relation to `RESTART WITH` clause, which 'reseds' a given sequence

```SQL
ALTER SEQUENCE dbo.sequence1
  RESTART WITH 100 
  INCREMENT BY 50 
  MINVALUE 50 
  MAXVALUE 10000
  NO CYCLE;

  -- TO drop a sequence use DROP SEQUENCE
```

## SET operators

### UNION

union of two set of all elements appearing in either or both of the sets

```SQL
select_1 UNION [ALL] select_2 {[UNION [ALL] select_3]}

-- select_1, select_2 are SELECT statements that build the union
-- ALL options is used, all resulting rows, including duplicates, are displayed.
-- the ALL option is the default in select statement, bit it must be specified with UNION operator to display all resulting rows.
-- 
```

ALTERNATIVE WAY TO CREATE TABLE FROM AN EXISTING TABLE

```SQL
SELECT emp_no, emp_fname, emp_lname, dept_no 
INTO employee_enh 
FROM employee 
ALTER TABLE employee_enh 
ADD domicile CHAR(25) NULL;

/*
  EXAMPLE of UNION 
*/

SELECT domicile FROM employee_enh 
UNION SELECT location FROM department
```

> `SELECT` lists ust have same number of columns and teh corresponding columns must have compatible data types. the ordering of the result of union can be done only if `ORDER BY` clause is used with last `SELECT statement`

OR operator can be used instead of the UNION operator if all select statements connected by one or more UNION operators refrence the sam e table. the set of select statement si replaced through one `SELECT` statement with set of OR operators.

### INTERSECT and EXCEPT

intersection of two tables is the set of rows belonging to both tables.

```SQL
SELECT emp_no 
  FROM employee
  WHERE dept_no ='d1'
INTERSECT 
SELECT emp_no 
  FROM works_on
  WHERE enter_date < '01.01.2018';

-- THE T-SQL does not support INTERSECT operator with ALL option

SELECT emp_no from employee
WHERE dept_no = 'd3'
EXCEPT 
SELECT emp_no 
  FROM works_on
  WHERE enter_date > '01.01.2018';
```

## CASE

to modify the representation of data.
> CASE does not represent a statement but a expression. Therefore case can be used anywhere.

### SIMPLE CASE expression

```SQL
CASE expression_1
  {WHEN expression_2 THEN result_1} ...
  [ELSE result_n]
END
```

EXAMPLEs

```SQL
SELECT ProductNumber, Category = 
  CASE ProductLine
    WHEN 'R' THEN 'Road'
    WHEN 'M' THEN 'Monitoring'
    WHEN 'T' THEN 'TOURING'
    WHEN 'S' THEN 'OTHER SALE ITEMS'
    ELSE 'NOT FOR SALE'
  END
  NAME FROM PRODUCTION.PRODUCT
```

## Subqueries

T-SQL offers the ability to compare columns values with the result of another SELECT statement. SELECt statement of a subquery is called the *outer query* in contrast to the *inner query*, which denotes the SELECT statements used in comparison .
The Inner query is evaluated first, the outer query receives the values of inner query.

> An INNER query can also be nested in INSERT, UPDATE or DELETE statement.

### Self-Contained and Correlated

- inner query is logically evaluated exactly one.
- whereas correlated subquery differs from a self-contained one in that its value depends upon a variable from outer query, therefore, INNER query is logically evaluated each time the system retrieves row from outer query.

A self-contained subquery can be used with following operators.

- Comparison operators
- IN operators
- ANY or ALL operator

```SQL
SELECT emp_fname, emp_lname FROM Employee
  WHERE dept_no = (
    SELECT dept_no FROM department WHERE dept_name = 'Research'
  );

-- The drawbacks of using = operator is the inner query must return one value. 

/*
  IN OPERATOR
*/
SELECT * from employee WHERE dept_no IN (
  SELECT dept_no FROM department WHERE location = 'Dallas'
);

-- Each inner query may contain further queries ( subqueries with multiple level of nesting)
-- 
SELECT emp_lname, FROM Employee 
  WHERE emp_no IN (
    SELECT emp_no FROM works_on 
      WHERE project_no IN 
        (
          SELECT project_no FROM project WHERE project_name ='Apollo'
        )
  );


/*
  WITH ANY and ALL operators 
  -------------------------------------------
  operators ANY and ALL always use in combination with one of the comparison

  SYNATAX 

  column_name operator [ANY | ALL] query 
*/

-- get employee numbers, project numbers, job names for employee who have not spent the most time on one of the projects 

SELECT DISTINCT emp_no, project_no , job 
  FROM works_on 
  WHERE enter_date > ANY 
  (
    SELEcT enter_date FROM works_on
  );

```

## Temporary Tables

- A temporary table is a database that is temporarily stored and managed by the database system.
- Temporary can local or global.
- local temp tables have physical representation stored in **tempdb**.
- specified with prefix `#` ( for example `#table_name`)
- local temp table is owned by the session that created it and it visible only to other session.
- automatically dropped when the creating session terminates.

- Global Temporary table are visible to any user and any connection after they are created, and are deleted when all users that are referencing the table disconnect from database.
- prefix with `##`

```SQL
CREATE TABLE #project_temp 
  (
    project_no CHAR(4) NOT NULL,
    project_name CHAR(25) NOT NULL
  );

-- --------***********************---***************
SELECT project_no, project_name 
  INTO #project_temp1
  FROM project;
```

## JOIN Operator

- used to retrieve data from more than one table.
- allows data to be spread over many tables and thus achieves a vital property (NON redundant data)
- attaches the column of tables whereas in UNION is attaches the rows of tables

### Two syntax form to implement joins

- Explicit join syntax (ANSI SQL:1992 join syntax)
- IMPLICIT JOIN syntax ( old-style join syntax)

using the corresponding for each type of join operation. the keywords concerning the explicit definition of join are:

- CROSS JOIN
- [INNER] JOIN
- LEFT [OUTER] JOIN
- RIGHT [OUTER] JOIN
- FULL [OUTER] JOIN

`CROSS JOIN` specifies cartesian product of two tables. `INNER JOIN` defines the natural join of two tables, While LEFT OUTER JOIN and RIGHT OUTER JOIN characterize the join operations of the same names .
FULL OUTER JOIN specifies the union of the right and left outer joins.

> Use of explicit join syntax is recommended.

## Natural Join

- also known as `equi-join`.
- the equi join operation has one or more pairs of columns that have identical values in every row. The operation that eliminates such columns from the equi-join is called a natural join.

```SQL
SELECT employee.*, department.* 
  FROM employee  INNER JOIN department 
  ON employee.dept_no = department.dept_no;
```

- The `ON` clause is also part of the FROM clause, it specifies the join condition from both tables.

```SQL
SELECT employee.* , department.*
  from employee, department
  WHERE employee.dept_no = department.dept_no;
```

- the semantics of the corresponding join columns must be identical. this means both columns must have the same logical. it is not required that the corresponding join columns have the same name, although this will often we case.

> database systems can check only the data type and the length of string data types. The Database Engine requires that the corresponding join columns have compatible data types, such as INT and SMALLINT.

Qualifying a column name means that, to avoid any possible ambiguity about which table teh column belongs to column name is preceded by its table name, separated by a period.

```SQL
SELECT dept_no 
  FROM employee JOIN works_on
  ON employee.emp_no = works_on.emp_no 
  WHERE enter_date = '10.15.2017';
```

#### Joining More than two tables

Theoretically, there is no upper limit on number of tables that can be joined using a SELECT statement.
the DB Engine has an implementation restriction: the maximum number of  tables that can be joined in a select statement is 64.
