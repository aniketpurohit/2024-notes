# Stored procedures and user-defined functions

*Batch* is a sequence of T-SQL statements and procedural extensions.
*routine* can be either stored procedure or a user-defined function(UDF)

## procedural Extensions

- number of statements in a batch is limited by the size of the compiled batch object.
- main advantage of a batch over a group of singleton statements is that executing all statements at once brings significant performance.
- The number of restriction concerning the appearance of different statements in a batch.

> To Separate DDL statements from one another, use `GO` statement.

### BLOCK of statements

- allows the building of units with one or more T-SQL statement.
- begins with `BEGIN` and terminates with `END`

```SQL
BEGIN 
    statement_1
    statement_2
    ....
END
```

## IF Statement

- executes one T-SQL statement if a Boolean expression, which follows the keyword IF, evaluates to TRUE.

```SQL
IF (select count(*) FROM work_on WHERE project_no='p1' GROUP BY project_no) > 3
    PRINT 'The number of employees in the project p1 is 4 or more'
ELSE BEGIN 
    PRINT 'The following employees work for the project p1'
    SELECT emp_fname, emp_lname
        FROM employee, works_on 
        WHERE employee.emp_no = works_on.emp_no 
        AND project_no ='p1'
    END
```

> PRINT statement is another statement that belongs to procedural extensions

## WHILE statement

- t repeatedly executes one Transact-SQL statement (or more, enclosed in a block) while the Boolean expression evaluates to TRUE.
- can optionally contain one of two statements used to control the execution of the statements within the block: BREAK or CONTINUE.

```SQL
WHILE (SELECT SUM(budget) FROM project) < 50000
BEGIN 
    UPDATE project SET budget = budget *1.1
    IF (SELECT MAX(budget) FROM project) > 240000
        BREAK 
    ELSE
        CONTINUE 
    END
```

## LOCAL variables

- used to store values (of any type) within a batch or a routine.
- can be referenced only within the same batch in which they were declared.
- must be defined using the `DECLARE` statement
- Variables are always referenced in a batch using the prefix @.

Assignment of local variable is done:

- using special form of SELECT statement.
- using the SET statement.
- Directly in DECLARE statement using = sign.

```SQL
DECLARE @avg_budget MONEY, @extra_budget MONEY
DECLARE @pr_nr CHAR(4)
    SET @extra_budget = 15000
    SELECT @avg_budget = AVG(budget) FROM project 
    IF (SELECT budget FROM project WHERE project_no = @pr_nr) < @avg_budget
    BEGIN
        UPDATE project SET budget = budget + @extra_budget 
        WHERE project_no = @pr_nr
        PRINT 'Budget for @pr_nr increased by @extra_budget'
    END

-- will be sent to the system to process them at the same time

-- USING CURSOR

DECLARE @avg_budget MONEY;
DECLARE @extra_budget MONEY;
DECLARE @budget MONEY;
DECLARE @pr_nr CHAR(4);
DECLARE @p_cursor as CURSOR;
SET @extra_Budget = 15000;
SELECT @avg_budget = AVG(budget) FROM project; 
SET @budget = 0;
SET @P_cursor = CURSOR FOR SELECT project_no, budget FROM project;
OPEN @P_cursor;
FETCH NEXT FROM @P_cursor INTO @pr_nr, @budget

WHILE @@FETCH_STATUS = 0
BEGIN 
    PRINT @pr_nr 
    PRINT @budget 
    IF (SELECT budget FROM project WHERE project_no=@pr_nr) >= @avg_budget
    BEGIN 
        GOTO L1
    END
    ELSE
        UPDATE project SET budget= budget +@extra_budget WHERE project_no = @pr_nr
        PRINT 'Budget for @pr_nr increased'
    L1: 
        FETCH NEXT FROM @p_cursor INTO @pr_nr, @budget
END
CLOSE @p_cursor
DEALLOCATE @P_cursor
```

- main difference between these two solutions is that 8.3b retrieves each row from the result separately; i.e., in this case the system processes one record (row) at a time. (For this reason, the type of processing is called record-oriented processing.)

### Creation of CURSOR

- declare your cursor by using the DECLARE statement and assigning
the CURSOR data type.
- you use the SET statement to assign the set of rows, which
will be retrieved (one by one) with the cursor.
- opening the cursor using the OPEN statement.
- Immediately after the OPEN statement is executed, the cursor points before the first row of the selected set of rows.
- To move the cursor to the first row in the result set, you use the FETCH NEXT `FETCH NEXT FROM @P_cursor INTO @pr_nr, @budget`

> statement fetches a record from the result set and assigns values retrieved with the SELECT statement to the variables @pr_nr and @budget, respectively

- WHILE statement uses the system function called @@FETCH_STATUS to create a loop, which will be terminated when all records from the result set are processed.
- you use the CLOSE statement to close the cursor.
- the DEALLOCATE statement DEALLOCATE the particular cursor

> Do not use the implementation with CURSOR unless absolutely necessary. The record-oriented processing og rows is significantly slower than the set-oriented processing.

## Miscellaneous Procedural Statement

### RETURN

- statement has the same functionality inside a batch as the BREAK statement inside WHILE.
- causes the execution of the batch to terminate and the first statement following the end of the batch to begin executing.

### GOTO

- statement branches to a label, which stands in front of a Transact-SQL statement within a batch.

### RAISERROR()

- statement generates a user-defined error message and sets a
system error flag.
- user-defined error number must be greater than 50000.
- All error numbers <= 50000 are system defined and are reserved by the Database Engine.
- error values are stored in the global variable `@@error`.

### WAITFOR

defines either the time interval (if the DELAY option is used) or a specified time (if the TIME option is used) that the system has to wait before executing the next statement in the batch

```SQL
WAITFOR {DELAY 'time' | TIME 'time' | TIMEOUT 'timeout'}
--  TIMEOUT specifies the amount of time, in milliseconds, to wait for a message to arrive in the queue. 
```

## Exception Handling with TRY, CATCH, and THROW\

- exception is a problem (usually an error) that prevents the continuation of a program

BENEFITS

- provide a clean way to check for errors without cluttering code.
- provide a mechanism to signal errors directly rather than using some side effects.
- Exceptions can be seen by the programmer and checked during the compilation process.
- `THROW` statement is another return mechanism, which behaves similarly to the already described `RAISERROR()` statement.

```SQL
BEGIN TRY 
    BEGIN TRANSACTION
    INSERT into employee values(1111, 'Ann' 'smith','d2');
    INSERT into employee values(22222, 'Mattew' , 'Jones', 'd4'); -- referential integrity error
    COMMIT TRANSACTION 
    PRINT 'Transaction committed'
END TRY 
BEGIN CATCH 
    ROLLBACK 
    PRINT 'TRansaction rolled back'
    THROW
END CATCH

-- that supports server-side paging
DECLARE @pageSize TINYINT = 20,  @CurrentPage INT     = 4;

SELECT BusinessEntityID, JobTitle, BirthDate  
   FROM HumanResources.Employee 
   WHERE Gender = 'F' 
ORDER BY JobTitle 
OFFSET (@PageSize * (@CurrentPage - 1)) ROWS 
    FETCH NEXT @PageSize ROWS ONLY;
```

## Stored Procedures

- stored procedure is a special kind of batch written in Transact-SQL, using the SQL language and its procedural extensions
- stored a DB object. stored procedures are saved on the server side to improve the performance and consistency of repetitive tasks.
- System procedures are provided with the Database Engine and can be used to access and modify the information in the system catalog
- stored procedure is precompiled before it is stored as an object in the database
  - the repeated compilation of a procedure is (almost always) eliminated
  - the execution performance is therefore increased.
    - concerning the volume of data that must be sent to and from the database system

> Stored procedures can be natively compiled, meaning that the particular procedure is compiled when it is created, rather than when it is executed.

### Creation and Execution of Stored Procedures

```SQL
CREATE PROC[EDURE] [schema_name.]proc_name  
[({@param1} type1 [ VARYING] [= default1] [OUTPUT])] {, …} 
[WITH {RECOMPILE | ENCRYPTION | EXECUTE AS 'user_name'}] 
[FOR REPLICATION] 
AS batch | EXTERNAL NAME method_name

-- EXPLANATION
    -- schema_name is the name of schema to which ownership of created stored procedure is assigned
```

***EXPLANATION***

- schema_name is the name of schema to which ownership of created stored procedure is assigned
- proc_name is name of stored procedure
- @param1 is a parameter of type1
- default1 specifies the optional default value of the corresponding parameter
- OUTPUT option indicates that the parameter is a return parameter and can be returned to the calling procedure or to the system
- you want to generate the compiled form each time the procedure is executed, use the WITH `RECOMPILE` option
- `EXECUTE AS` clause specifies the security context under which to execute the stored procedure after it is accessed.
- only the members of the sysadmin fixed server role, and the db_owner and db_ddladmin fixed database roles, can use the CREATE PROCEDURE statement.

```SQL
GO 
CREATE PROCEDURE increased_budget (@percent INT=5)
    AS UPDATE project SET budget = budget + budget*@percent /100;

--  GO statement is used to separate two batches. (The CREATE PROCEDURE statement must be the first statement in the batch.
```

- it is possible to create temporary stored procedures that are always placed in the temporary system database called tempdb.
- Analogous to local and global temporary tables, you can create local or global temporary procedures by preceding the procedure name with a single pound sign (#proc_name) for local temporary procedures and a double pound sign (##proc_name) for global temporary procedures
- A local temporary stored procedure can be executed only by the user who created it, and only during the same connection
- life cycle of a stored procedure has two phases: its creation and its execution.
- EXECUTE statement executes an existing procedure.  execution of a stored procedure is allowed for each user who either is the owner of or has the EXECUTE privilege for the procedure

```sql
 [[EXEC[UTE]] [@return_status =] {proc_name  
        | @proc_name_var} 
        {[[@parameter1 =] value | [@parameter1=] @variable [OUTPUT]] | 
DEFAULT}.. 
        [WITH RECOMPILE]

-- return_status is an optional integer variable that stores the return status of a procedure. 
-- The value of a parameter can be assigned using either a value (value) or a local variable (@variable)
--  DEFAULT clause supplies the default value of the parameter as defined in the procedure.
```

```sql
CREATE PROCEDURE delete_emp @employee_no INT, @counter INT OUTPUT 
    AS SELECT @counter = COUNT(*) 
            FROM works_on 
            WHERE emp_no = @employee_no; 
    DELETE FROM employee 
            WHERE emp_no = @employee_no; 
        DELETE FROM works_on 
            WHERE emp_no = @employee_no;

DECLARE @quantity INT; 
EXECUTE delete_emp @employee_no=28559, @counter=@quantity OUTPUT;
```

> The value of the parameter will be returned to the calling procedure if the OUTPUT option  is used. @counter parameter must be declared with the OUTPUT option in the procedure as well as in the EXECUTE statement

### The EXECUTE Statement with RESULT SETS Clause

- can change conditionally the form of the result set of a stored procedure.

```sql
GO 
CREATE PROCEDURE employees_in_dept (@dept CHAR(4)) 
 AS SELECT emp_no, emp_lname  
   FROM employee  
   WHERE dept_no IN (SELECT @dept FROM department  
                       GROUP BY dept_no)


-- with results sets
USE sample; 
EXEC employees_in_dept 'd1' 
  WITH RESULT SETS 
  ( ([EMPLOYEE NUMBER] INT NOT NULL, 
    [NAME OF EMPLOYEE] CHAR(20) NOT NULL));
```

- allows you to change the name and data types of columns displayed in the result set.
- this functionality gives you the flexibility to execute stored procedures and display the output result sets in another form.

### Changing the Structure of Stored Procedures

- ALTER PROCEDURE statement, which modifies the structure of a stored procedure
- ALTER PROCEDURE statement is usually used to modify Transact-SQL statements inside a procedure.
- A stored procedure is removed using the DROP PROCEDURE statement
- owner of the stored procedure and the members of the db_owner and sysadmin fixed roles can remove the procedure.

## User-Defined Functions

Use-Defined functions can be

- Scalar
  - return value is always a single value
  - scalar functions can be called using `EXECUTE` statement,

- Table-valued
  - returns data of a table type

### CREATION AND EXECUTION OF UDFs

```SQL
CREATE FUNCTION [schema_name.]function_name 
    [({@param } type [= default])  {,...} 
    RETURNS {scalar_type | [@variable] TABLE} 
    [WITH {ENCRYPTION | SCHEMABINDING} 
    [AS] {block | RETURN (select_statement)}
```

- **schema_name** name of the schema to which the ownership of created UDF is assigned.
- **function_name** name of new function.
- **@param** is an input parameter.
- **default** specifies the optional default value of the corresponding parameter.
- `RETURNS` defines data type of the value returned by UDF. (with the exception of `TIMESTAMP`)
- `WITH ENCRYPTION` encrypts the information in the system catalog that contains the text of `CREATE FUNCTION`. OR  `WITH SCHEMABINDING` binds the UDF to the database objects that it references. Any attempt to modify the structure of the database object that the function references fails.
  - Database objects that are referenced by a function must fulfill the following conditions if you want to use the SCHEMABINDING clause during the creation of that function:
    - All views and UDFs referenced by the function must be schema-bound.
    - All database objects (tables, views, or UDFs) must be in the same database as the function

**block** is the BEGIN/END block that contains the implementation of the function. final statement of the block must be a RETURN statement with an argument.

- Assignment statement such as SET
- Control-of-flow statements such as WHILE and IF
- DECLARE statements defining local data variables.
- SELECT statements containing SELECT lists with expressions that assign to variables that are local to the function.
- INSERT, UPDATE and DELETE statements modifying variables of TABLE data type that are local to the function.

```SQL
-- This function computes additional total costs that arise 
-- if budgets of projects increase

GO CREATE FUNCTION compute_costs (@percent INT=10)
    RETURNS DECIMAL(16,2)
    BEGIN 
        DECLARE @additional_costs DEC (14,2), @sum_budget dec(16,2)
    SELECT @sum_budget = SUM(budget) FROM project
    SET @additional_costs = @sum_budget *@percent /100
    RETURN @additional_costs
END


-- INVOKING 
SELECT project_no, project_name FROM project 
WHERE budget < dbo.compute_costs(25)
```

### SCALAR UDF Inlining

prior to SQL Server 2019, scalar user-defined functions are generally a performance issue because they are generally processed in a row-oriented way, meaning that they run for every returned row.

- and did not allowed parallel execution of rows.
- allows certain scalar UDFs to have their definitions directly into query so that the query does not call the UDF executing each row.

### TABLE- Valued Functions

- RETURNS clause specifies TABLE with no accompanying list of columns, the function is an inline function.
- he Query Optimizer may inline a function’s text into a query and thus optimize a query as a whole.
- Multistatement table-valued functions are difficult to optimize, and are not considered by the Query Optimizer.

```SQL
CREATE FUNCTION employees_in_project (@pr_number CHAR(4))
    RETURNS TABLE 
    AS RETURN (SELECT emp_fname, empl_name FROM works_on, employee
    WHERE employee.emp_no = works_on.emp_no 
    AND project_no = @pr_number)

-- calling of function 
SELECT * FROM employees_in_project('p3')
```

### TABLE-VALUED functions and APPLY

`APPLY` operator is a relational operator that allows you to invoke a table-valued function for each row of table expression.

- CROSS APPLY
  - returns those rows from the inner (left) table expression that match rows in the outer (right) table expression.
  - logically same as INNER JOIN
  - advantage of the CROSS JOIN is that it can yield a better execution plan and better performance, since it can limit the set being joined, before the join occurs
- OUTER JOIN
  - returns all the rows from inner table expression.
  - rows for which there is no corresponding matches in the outer table expression
  - equivalent to LEFT OUTER JOIN

```SQL
CREATE FUNCTION dbo.fn_getjob(@empid as INT)
RETURNS TABLE AS
    RETURN 
    SELECT job FROM works_on WHERE emp_no = @empid
    AND job is NOT NULL AND project_no ='p1';

-- USE CROSS APPLY 
SELECT E.emp_no, emp_fname, enp_lname, job FROM employee as E
CROSS APPLY dbo.fn_getjob(E.emp_no) AS A

-- USE OUTER APPLY 
SELECT E.emp_no, emp_fname, emp_lname, job FROM employee as E 
    OUTER APPLY dbo.fn_getjob(E.emp_no) as A
```

#### TABLE-VALUED Parameter

```SQL
GO 
CREATE TYPE departmentType as TABLE
    (dept_no  CHAR(4),dept_name CHAR(25),location CHAR(30));

GO 
CREATE TABLE #dallasTable 
  (dept_no CHAR(4),dept_name CHAR(25),location CHAR(30));

GO 
CREATE PROCEDURE insertProc 
  @Dallas departmentType READONLY 
  AS SET NOCOUNT ON 
  INSERT INTO #dallasTable (dept_no, dept_name, location) 
   SELECT * FROM @Dallas

GO 
DECLARE @Dallas AS departmentType; 
INSERT INTO @Dallas( dept_no, dept_name, location) 
SELECT * FROM department 
WHERE location = 'Dallas' 
EXEC insertProc @Dallas;
```

The use of table-valued parameters gives you the following benefits:
 • It simplifies the programming model in relation to routines.
 • It reduces the round trips to the server.
 Part II
 • The resulting table can have different numbers of rows.

- removed using the DROP FUNCTION statement.
- supports the ALTER FUNCTION statement, which modifies the structure of a UDF.
- the owner of the function(or the members of the db_owner and sysadmin fixed database roles) can remove the function.
