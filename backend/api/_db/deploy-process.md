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
CREATE DATABASE your_database_name 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;
```

```sql
GRANT ALL PRIVILEGES ON `lebinetx`.* TO 'lebinetx'@'localhost';
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
    avatar VARCHAR(100)
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
CREATE TABLE hashtags(
    hashtagId VARCHAR(36) PRIMARY KEY,
    postId VARCHAR(36) NOT NULL,
    hashtag VARCHAR(100) NOT NULL,
    FOREIGN KEY (postId) REFERENCES posts(postId) ON DELETE CASCADE
);
```

```sql
CREATE TABLE post_reactions(
    reactionId VARCHAR(36) PRIMARY KEY,
    postId VARCHAR(36) NOT NULL,
    userId VARCHAR(36) UNIQUE NOT NULL,
    reaction INT,
    FOREIGN KEY (postId) REFERENCES posts(postId) ON DELETE CASCADE,
    FOREIGN KEY (userId) REFERENCES users(userId) ON DELETE CASCADE
);
```

```sql
CREATE TABLE comments(
    commentId VARCHAR(36) PRIMARY KEY,
    userId VARCHAR(36) NOT NULL,
    postId VARCHAR(36) PRIMARY KEY,
    postId VARCHAR(36) NOT NULL,
    content TEXT,
    FOREIGN KEY (userId) REFERENCES users(userId) ON DELETE CASCADE,
    FOREIGN KEY (postId) REFERENCES posts(postId) ON DELETE CASCADE
);
```

```sql
CREATE TABLE comment_reactions(
    reactionId VARCHAR(36) PRIMARY KEY,
    commentId VARCHAR(36) NOT NULL,
    userId VARCHAR(36) UNIQUE NOT NULL,
    reaction INT,
    FOREIGN KEY (commentId) REFERENCES comments(commentId) ON DELETE CASCADE,
    FOREIGN KEY (userId) REFERENCES users(userId) ON DELETE CASCADE
)
```