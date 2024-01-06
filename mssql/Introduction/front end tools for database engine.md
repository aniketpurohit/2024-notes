# Front End Tools for database engine

## SQL server management Studio

the database engine provides various tools that are used for different purposes, such as system installation, configuration and performance testing.

The main components used for authoring, administration, and management of overall system are:

- Registered Servers
- Object Explorer
- Query Editor
- Solution Explorer
- Data Discovery and Classification

### Connecting to a server

- Server type : for most of cases use Database engine
- Server Name : select or type the server that you want to use.
- Authentication
  - Windows Authentication : uses your Windows account
  - SQL Server Authentication : uses its own Authentication
  - Active Directory - interactive authentication method that supports Azure Multi-factor Authentication
  - Active Directory - password adn Active-Directory  : non-interactive authentication methods supported by Azure Active Directory

### registered Servers

- is represented as a pane that allows connections to already used server.
- can use these connections to check a server's status or to manage its objects.
- can add new server to the list of all servers, ore remove one or more existing servers.

### object Explorer

- contains a tree view of all database object in a server. (select View | Object Explorer)
- Tree view shows you a hierarchy of the objects on a server instance.
- object allows you to connect to multiple servers in the same pane.

## Using SQL server management Studio with Database Engine

It has 2 major purposes :

- Administration of database servers.
- Management of database objects

### Administering Database Server

- Register Serves
  - separates the activities of registering servers and exploring databases and their objects.
  - Every server (local or remote) must be registered before you can use its databases and objects.
  - To register a database server, right-click the icon of your database server in Object Explorer and choose Register.

- Connect to a server
  - registering a server does not automatically connect you to the server at SSMS startup.
- Create a new server groups
  - create a new server group in the Registered Servers pane, right-click Local Server Groups
and choose New Server Group
- manage multiple servers
- Start and Stop servers
  - Database Engine server starts automatically by default each time the Windows operating system starts.

### Managing Databases Using Object Explorer

**Creating Databases Without Using Transact-SQL**

- create a new database by using Object Explorer or the Transact-SQL language
- The General page of the Database Properties dialog box (see Figure 3-5) displays, among other things, the database name, the owner of the database, and its collation.
- The properties of the data files that belong to a particular database are listed in the Files page and comprise the name and initial size of the file, where the database will be stored, and the type of the file

The Filegroups page of the Database Properties dialog box displays the name(s) of the filegroup(s) to which the database file belongs, the art of the filegroup (default or nondefault), and the allowed operation on the filegroup (read/write or read-only).

Options page of the Database Properties dialog box enables you to display and modify all database-level options.

- Database Read-Only : Allows read-only access to the database (default False)
- Database State : Describes the state of the database. (The default value is Normal.)
- Restrict Access : Restricts the use of the database to one user at a time. (The default value is MULTI_USER.)
- Encryption Enabled : Controls the database encryption state. (The default value is False.)

## Authoring Activities Using SQL Server Management Studio

### Query Editor

open Query Editor, the status bar at the bottom of the pane tells you whether your query is in a connected or disconnected state.
Query Editor can be used by end user for the following tasks:

- Generating and Executing Transact-SQL statements
- Storing the generated Transact-SQL statements in a file.
- Generating and analyzing plans for generated queries.
- Graphically illustrating the execution plan for a selected query.

The additional information concerning the execution of the statement(s) is displayed in the status bar at the bottom of the Query Editor window:

- The status of the current operation
- Database server name
- Current username and server process ID
- Current database name
- Elapsed time for the execution of the last query
- The number of retrieved rows

Object Explorer is very useful if you want to display the graphical execution plan for a particular query. (The execution plan is the plan selected by the optimizer to execute a given query.) by using display estimated execution plan

### Solution Explorer

A solution can have zero, one or more projects associated with it. A blank solution does not contain any project.

### Data Discovery and Classification

set of services that is used to discover, classify and report sensitive data in database. Sensitive data includes business, financial, and healthcare information.
To protect your sensitive data by meeting the data privacy standards and by controlling access to the data.

- Applying you own classification policy.
- applying recommended classification
- Summarizing the classification using a report.

#### Applying your own Classification Policy

- budget column of project table as confidential.
the following classification level of selected data.
- public
  - unauthorized disclosure, alteration or destruction would result in little or no risk to the company that owns it.
- General
  - general personal data that can be identified by reference to an identifier, such as name or and identification number.
- Confidential
  - Data whose access is restricted according to data classification scheme defined by the particular organization.
- Confidential - GDPR
  - Confidential data additionally falls with in the scope of the EU's general data protection regulation.
- Highly Confidential
- access in any form  including  paper or electronic is restricted to authorized individuals only.Transmitting or storing this data without encryption is prohibited.

#### Applying and Summarizing the Recommended Classification

Data Discovery and Classification tool is the capability to scan and  discover the sensitive data in your database

can change the Information Type and the Sensitivity Label values provided by the tool with any value listed previously according to your company policies and/or standards using the drop-down boxes to the right of each column.  you accept the recommended classification on the selected columns, a notification message informs you that the changes will not be updated until you save all changes. Additionally, the Discovery and Classification tool allows you to generate a report that summarizes the classification state of the database. To do this, click the View Report button in the top menu of the window, after performing the previous classifications.

## Azure Data Studio

It is a cross platform, desktop front-end tool for data professionals that cna be used as a data platform on Linux and macOS

### Configuration

Preferences are customized by a JSON file called setting.json

### Object Explorer

In Azure Data Studio,

- Manage : opens dashboards for different tasks, such as database backup  and restore.
- New Query : opens the new code Editor window
- Refresh ; Updates the database and its objects.

### Database Dashboard and Customization

Azure Data Studio has two dashboard :

- Server
- Database
These dashboard are populated by objects called widgets.

## SQL Server Management Studio VS Azure Data Studio

- use SQL Server Management Studio
- Spend most of your time on database administration tasks.
- perform sophisticated  administrative tasks.
- Perform security management, including user management, vulnerability assessment and configuration of security features.
- Need to make use of performance tuning advisors.

- use Azure Data Studio
- need to run front-end toll on Linux or macOS
- spend most of time editing or executing queries
- need to ability to quickly chart and visualize result sets.
