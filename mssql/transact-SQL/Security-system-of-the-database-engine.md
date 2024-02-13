# Overview

The following begins with an overview of most important security concepts

- Data Encryption
- Authentication
- Authorization
- Schemas
- Roles
- Change Tracking
- Data Security and Views

***Some terms***

- **principal**
  - Subjects that have permission to access a particular entity.
  - A role is collection of logins and other roles.

- **Securable**

  - resources to which DB authorization system regulates access.
  - Most securable build a hierarchy.

- **Permissions**
  - securable has associated *permission* can be granted to a principal.
  
## Encrypting Data

The DB Engine secures data with hierarchical encryption layers and a key management infrastructure.
Each layer secures layer beneath it, using a combination of certificates,asymmetric keys, and symmetric keys.

![DB Engine hierarchical encryption layers](../img/DB-engine-hierarchical-encryption-layers.png)

**Service master key**
The service master key specifies the key that rules all other keys and certificates. the service master key is created automatically when you install the DB Engine.

- is encrypted using Windows Data  Protection API (DPAPI).
- managed by system

**DB master key**
root encryption object for all keys, certificates, and data at DB level.

- Each DB has single DB master key created by using `CREATE MASTER KEY`
- as this key is protected by service master key, it is possible for the system to automatically decrypt master key.

There are 3 types of user forms:

- ***Symmetric Keys***
  - sender and receiver shares a common key.
  - **Advantage**
    - can protect significant greater amount of data than any other type/
    - it is faster than using asymmetric key.
  - **disadvantage**
    - in distributed env, using this key can make it almost impossible to keep encryption secure.

- Each symmetric key must be opened before you can use it to encrypt data or protect another new key.

- After you open a symmetric key, you need to `EncryptByKey` system function for encryption. this function has two input parameters:
  - ID of the symmetric key to be used
  - text to be encrypted.
- for decryption, use `DecryptByKey`

- ***Asymmetric Keys***
  - consist og two parts: a private key and the corresponding public key.
  - Each key can decrypt data encrypted by the other key.
  - `EncryptByAsymKey` to encrypt data
  - `DecryptByAsymKey` to decrypt data.

- ***Certificates***
  - is a digitally signed statement that binds a value of public key to identity of the person, device or service that holds the corresponding private key.
  - Certificate are issued and signed by a certification authority (CA)
  > there is no significant difference between certificates and asymmetric keys. Both uses RSA algorithm
  - certificates contains more information
    - The subject's public key value
    - the subjects's identifier information
    - Issuer identifier information
    - The digital signature of the issuer.
- A primary benefit it relieve hosts of the need to maintain a set of passwords for individual subjects.

> Certificates provide highest level of encryption in DB engine security model. the encryption algorithm are very processor-intensive.

```SQL
USE master;
CREATE MASTER KEY
ENCRYPTION BY PASSWORD ='pls4w9dl' -- you passsword

GO 
CREATE CERTIFICATE cert01
    WITH SUBJECT = 'CERTIFICATE FOR DBO';

-- ENCRYPTION BY , you have to create DB master key 
-- if this option is not used CERTIFICATE is protected by DB master key 
-- 
```
