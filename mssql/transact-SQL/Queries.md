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
