# User Authentication API

This project provides a simple user authentication API using MongoDB Atlas as the database. It includes user registration, login, and profile retrieval with JWT-based authentication.

## Prerequisites

1. **Create a MongoDB Atlas Account**  
   Sign up for a free MongoDB Atlas account:  
   [Register here](https://www.mongodb.com/cloud/atlas/register)

2. **Configure MongoDB URI**  
   - Update `config/database.py` with your MongoDB URI.  
   - Add your MongoDB Atlas **username** and **password**.

## Setup Instructions

### 1. Create a Virtual Environment  
Run the following command to create a virtual environment:

```sh
python -m venv env
```

### 2. Activate the Virtual Environment

- **Windows**:  
  ```sh
  env\Scripts\activate
  ```

- **Mac/Linux**:  
  ```sh
  source env/bin/activate
  ```

### 3. Install Dependencies

Run the following command to install all required dependencies:

```sh
pip install -r requirements.txt
```

### 4. Generate a Secure Secret Key

Generate a secret key for JWT authentication and add it to `SECRET_KEY` in `routers\routes.py`:

```sh
$ openssl rand -hex 32
```

### 5. Create a Database Collection

Run `database.py` to create the required collection in MongoDB:

```sh
python database.py
```

### 6. Run the Application

Start the API by running:

```sh
python main.py
```

## API Endpoints

The project includes three main API endpoints:

- **`/register`** – Registers a new user.  
- **`/login`** – Logs in a user and generates a JWT token.  
- **`/profile`** – Retrieves the authenticated user's profile upon successful authentication.
