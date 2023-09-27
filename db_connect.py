import psycopg2

def connect_to_db():
    """
    Establishes and returns a connection to the PostgreSQL database.
    """
    # Connection parameters
    params = {
        'host': 'localhost',  # or the hostname where your database is hosted
        'port': 5432,  # default PostgreSQL port
        'dbname': 'proposal_wizard',
        'user': 'postgres',  # Replace with your username
        'password': 'Ridgeway78'  # Replace with your password
    }
    
    try:
        conn = psycopg2.connect(**params)
        return conn
    except Exception as e:
        print(f"Error: Unable to connect to the database.\n{e}")
        return None
