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

```sql
CREATE TABLE posts (
    postId VARCHAR(36) PRIMARY KEY,
    userId VARCHAR(36) NOT NULL,
    title TEXT,
    content TEXT,
    createdAt DATETIME,
    updatedAt DATETIME,
    FOREIGN KEY (userId) REFERENCES users(userId) ON DELETE CASCADE
);
```

```sql
CREATE TABLE post_reactions(
    reactionId VARCHAR(36) PRIMARY KEY,
    postId VARCHAR(36) NOT NULL,
    reaction INT,
    FOREIGN KEY (postId) REFERENCES posts(postId) ON DELETE CASCADE
);
```