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

-- all dept whose location begins with a charater in range C through F 
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

