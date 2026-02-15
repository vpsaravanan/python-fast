# 🔌 MySQL Database Connection Guide

## ✅ Setup Complete!

Your FastAPI application is now configured to connect to MySQL. Here's what was set up:

## 📁 Files Created/Updated

### 1. **database.py** - Database Connection
- SQLAlchemy engine setup
- Database URL from environment variable
- Session management
- `get_db()` dependency for routes

### 2. **models.py** - Database Models
- `User` model (id, username, email, age, timestamps)
- `ProcessedData` model (for storing calculation results)
- SQLAlchemy ORM definitions

### 3. **init_db.py** - Database Initialization Script
- Creates all database tables
- Can be run manually if needed

### 4. **Updated Routers**
- `routers/create_user.py` - Now saves users to MySQL
- `routers/users.py` - Now fetches users from MySQL

### 5. **Updated requirements.txt**
- Added `pymysql` - MySQL driver for Python
- Added `aiomysql` - Async MySQL support

## 🚀 How to Start

### Step 1: Rebuild Docker Containers
```bash
cd /Users/saravana/Documents/python
docker-compose down
docker-compose up --build -d
```

### Step 2: Check Logs
```bash
# Check if MySQL is ready
docker logs python-mysql-1

# Check if FastAPI connected successfully
docker logs -f python-python-app-1
```

### Step 3: Verify Database Tables
```bash
# Connect to MySQL container
docker exec -it python-mysql-1 mysql -u root -ppassword python-fastapi

# Inside MySQL, run:
SHOW TABLES;
DESCRIBE users;
DESCRIBE processed_data;
EXIT;
```

## 📝 API Endpoints

### Create User (POST)
```bash
# Using curl
curl -X POST "http://localhost:8000/create-user" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "age": 25
  }'

# Or use Swagger UI: http://localhost:8000/docs
```

### Get All Users (GET)
```bash
curl http://localhost:8000/users

# With pagination
curl "http://localhost:8000/users?skip=0&limit=10"
```

### Get User by ID (GET)
```bash
curl http://localhost:8000/users/1
```

## 🔗 Connection Details

### From FastAPI Container to MySQL:
- **Host**: `mysql` (service name in docker-compose)
- **Port**: `3306`
- **Database**: `python-fastapi`
- **Username**: `root`
- **Password**: `password`
- **Connection String**: `mysql+pymysql://root:password@mysql:3306/python-fastapi`

### From Your Mac to MySQL:
- **Host**: `localhost`
- **Port**: `3306`
- **Database**: `python-fastapi`
- **Username**: `root`
- **Password**: `password`

```bash
# Connect from Mac terminal
mysql -h 127.0.0.1 -P 3306 -u root -ppassword python-fastapi
```

## 🔍 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    age INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
);
```

### Processed Data Table
```sql
CREATE TABLE processed_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    total FLOAT NOT NULL,
    average FLOAT NOT NULL,
    maximum FLOAT NOT NULL,
    minimum FLOAT NOT NULL,
    count INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🛠️ Troubleshooting

### Issue: "Can't connect to MySQL server"
```bash
# Check if MySQL container is running
docker ps | grep mysql

# Check MySQL logs
docker logs python-mysql-1

# Restart MySQL
docker restart python-mysql-1
```

### Issue: "Access denied for user"
Check the credentials in `docker-compose.yml`:
```yaml
environment:
  MYSQL_ROOT_PASSWORD: password
  MYSQL_DATABASE: python-fastapi
```

### Issue: "Table doesn't exist"
The tables are created automatically on startup. If they don't exist:

```bash
# Restart the FastAPI container
docker restart python-python-app-1

# Or manually initialize
docker exec -it python-python-app-1 python init_db.py
```

### Issue: "Module 'pymysql' not found"
```bash
# Rebuild containers to install new dependencies
docker-compose down
docker-compose up --build -d
```

## 📊 Testing the Connection

### 1. Create a Test User
Visit: http://localhost:8000/docs
- Find POST `/create-user`
- Click "Try it out"
- Enter:
  ```json
  {
    "username": "testuser",
    "email": "test@example.com",
    "age": 30
  }
  ```
- Click "Execute"

### 2. Get All Users
Visit: http://localhost:8000/users

You should see your created user in the response!

### 3. Verify in Database
```bash
docker exec -it python-mysql-1 mysql -u root -ppassword python-fastapi -e "SELECT * FROM users;"
```

## 🔐 Environment Variables

The database URL is set in `docker-compose.yml`:
```yaml
environment:
  - DATABASE_URL=mysql://root:password@mysql:3306/python-fastapi
```

To change credentials:
1. Update `docker-compose.yml` environment variables
2. Update the `DATABASE_URL` variable
3. Rebuild containers: `docker-compose up --build -d`

## 📚 SQLAlchemy ORM Examples

### Query Users
```python
from sqlalchemy.orm import Session
from models import User
from database import get_db

# Get all users
users = db.query(User).all()

# Get user by username
user = db.query(User).filter(User.username == "johndoe").first()

# Get users older than 25
users = db.query(User).filter(User.age > 25).all()

# Count users
count = db.query(User).count()
```

### Create User
```python
new_user = User(username="jane", email="jane@example.com", age=28)
db.add(new_user)
db.commit()
db.refresh(new_user)
```

### Update User
```python
user = db.query(User).filter(User.id == 1).first()
user.age = 31
db.commit()
```

### Delete User
```python
user = db.query(User).filter(User.id == 1).first()
db.delete(user)
db.commit()
```

## 🎯 Next Steps

1. ✅ **Test the connection** - Create a user via API
2. ✅ **Verify in database** - Check MySQL directly
3. 📝 **Add more models** - Create tables for your data
4. 🔐 **Add authentication** - Implement user login
5. 🚀 **Deploy** - Move to production with secure credentials

## 📖 Additional Resources

- [FastAPI SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/orm/tutorial.html)
- [MySQL Docker Hub](https://hub.docker.com/_/mysql)

---

**Ready to test!** 🚀

Start with: `docker-compose up --build -d`
Then visit: http://localhost:8000/docs
