from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus
import os

# Load environment variables or use default values
DATABASE_USER = os.getenv("DATABASE_USER", "root")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "Santosh@27")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_NAME = os.getenv("DATABASE_NAME", "blogapplication")
DATABASE_PORT = os.getenv("DATABASE_PORT", "3306")  # Default port for MySQL
DATABASE_DRIVER = "aiomysql"  # Async driver for MySQL

# URL-encode the password to handle special characters
encoded_password = quote_plus(DATABASE_PASSWORD)

# Construct the DATABASE_URL incorporating the encoded password
DATABASE_URL = f"mysql+{DATABASE_DRIVER}://{DATABASE_USER}:{encoded_password}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# Create an asynchronous engine with echo=True for SQL query logging
engine = create_async_engine(DATABASE_URL, echo=True)

# Configure sessionmaker for creating AsyncSession instances
AsyncSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    class_=AsyncSession
)

# Base class for declarative class definitions
Base = declarative_base()