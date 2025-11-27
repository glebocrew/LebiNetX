### Some actions that were made while developing this shit
```sql
CREATE USER "lebinetx" IDENTIFIED BY "****"
```

```sql
SHOW LOCAL VARIABLES LIKE "%HOST%";
```

```sql
SHOW LOCAL VARIABLES LIKE "%PORT%";
```

```sql
CREATE DATABASE lebinetx;
```

```sql
GRANT ALL PRIVILEGES ON `lebinetx`.* TO 'lebinetx'@'%';
```

```sql
FLUSH PRIVILEGES;
```

        USER{
        VARCHAR(36) userId
        VARCHAR(50) nickname
        VARCHAR(50) email
        DATETIME createdAt
        DATETIME updatedAt
        BLOB avatar
    }

```sql
CREATE TABLE users (
    userId VARCHAR(36) PRIMARY KEY,
    nickname VARCHAR(50) UNIQUE,
    email VARCHAR(50) UNIQUE,
    pwd VARCHAR(512),
    createdAt DATETIME,
    updatedAt DATETIME,
    avatar BLOB
);
```