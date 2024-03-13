# Introduction

Data engineers must maintain data systems that are accurate, highly secure, and constantly available.

## On-Premises and cloud-based servers

CLoud Servers
an organization provisions service in the cloud and pays only for what it uses. Moving servers and services to the cloud also reduces operational costs.

### Computing environment

- require equipment to execute applications and services.
- overhead costs such as (power, cooling, periodic maintenance and storage)

### Licensing

- Each OS have it's licensing cost.

### Maintenance

- On-premises require maintenance for hardware, firmware, BIOS, OS, software and antivirus software.
- In the cloud, Microsoft manages many operations to create a stable computing environment.
- Microsoft manages key infrastructure services such as physical hardware, computer networking, firewalls and network security, datacenter fault tolerance, compliance, and physical security of the buildings. Microsoft also invests heavily to battle cybersecurity threats, and it updates operating systems and firmware for the customer

### Scalability

- scale an on-premises server horizontally, server administrators add another server node to a cluster. Clustering uses either a hardware load balancer or a software load balancer to distribute incoming network requests to a node of the cluster.
- scalability in the cloud is measured in compute units. Compute units might be defined differently for each Azure product

### Availability

- Service-level agreements (SLAs) specify your organization's availability expectations.
- Azure duplicates customer content for redundancy and high availability. Many services and platforms use SLAs to ensure that customers know the capabilities of the platform they're using.

|UP Time | Uptime hours per year | Downtime hours per year |
|:---: |:---:| :---:|
|99.9%| 8751.24 | 8.76|
|99.99%| 8759.12 | 0.88|
|99.999%| 8759.91 | 0.09|

### Support

- Cloud systems are easy to support because the environments are standardized
- On-premises due multiple vendors available, a company can use multiple vendors with different product. Which require a more support

### Multilingual support

- Cloud systems often store data as a JSON file that includes the language code identifier (LCID).The LCID identifies the language that the data uses. Apps that process the data can use translation services such as the Bing Translator API to convert the data into an expected language when the data is consumed or as part of a process to prepare the data

### Total cost of ownership

- describes the final cost of owing a given technology.
For On-Premises systems
- Hardware
- Software Licensing
- Labor (  installation, upgrades, maintenance )
- Datacenter overhead (power, telecommunications, building, heating and cooling)

Because on-premises server systems are very expensive, costs are often capitalized

- Azure track costs by subscriptions. A subscription can be based on usage that's measured in compute units, hours, or transactions.
- The cost of operating an on-premises server system rarely aligns with the actual usage of the system. In cloud systems, the cost usually aligns more closely with the actual usage.

### LIFT and SHIFT

When moving to the cloud, many customers migrate from physical or virtualized on-premises servers to Azure Virtual Machines. This strategy is known as lift and shift.
benefits include higher availability, lower operational costs, and the ability to transfer workloads from one datacenter to another. The disadvantage is that the application can't take advantage of the many features available within Azure.

## Understand Job responsibilities

a data engineer you'll extract raw data from a structured or unstructured data pool and migrate it to a staging data repository.Because the data source might have a different structure than the target destination, you'll transform the data from the source schema to the destination schema. This process is called transformation. You'll then load the transformed data into the data warehouse. Together, these steps form a process called extract, transform, and load (ETL).

## use cases for the cloud

### WEB

use the Azure Cosmos DB multimaster replication model to create a data architecture that supports web and mobile applications.
By reducing the processing time of their websites, global organizations can increase customer satisfaction.

### Healthcare

use Azure Databricks to accelerate big-data analytics and AI solutions. Apply these technologies to genome studies or pharmacy sales forecasting at a petabyte scale. Using Databricks features, you can set up your Spark environment in minutes and autoscale quickly and easily.

### IoT solutions

Using technologies like Azure IoT Hub, you can design a data solution architecture that captures information from IoT devices so that the information can be analyzed.

## Explore data Types

### Structured data

- Data structure is designed in the form of tables and is designed before any information is loaded into the system.
- Relational systems react slowly to changes in data requirements because the structural database needs to change every time a data requirement changes.

### non structural Data

- Non structured data is stored in nonrelational systems, commonly called unstructured or NoSQL systems.
- The data structure is defined only when the data is read.
- The open-source world offers four types of NoSQL databases:
  - key-value store
    - stored key-value of data in table structure
  - Document DB
    - Stored documents that are tagged with metadata to aid document searches.
  - graph DB
    - finds relationship between data points by using a structure that's composed of vertices and edges
  - Column DB
    - Stores data based on columns rather than rows.
    - columns can be defined at the query's runtime, allowing for flexible and performance data.
