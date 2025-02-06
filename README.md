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
