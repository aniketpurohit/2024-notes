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
