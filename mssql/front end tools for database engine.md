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
