import psycopg2
import pandas as pd

# Connect to the PostgreSQL database
connection_string = "postgresql://doadmin:AVNS_AZ-3Q1oUpp9WnsReBBX@devtradingsagedb-do-user-12481132-0.b.db.ondigitalocean.com:25060/defaultdb?sslmode=require"
conn = psycopg2.connect(connection_string)

# Define the input dates
date1 = '2023-01-02'
date2 = '2023-01-05'

# Define the SQL query
query = f"""
    SELECT strike, instrument_type, 
        (SELECT OI FROM test_assignment 
         WHERE date = '{date2}' AND strike = t1.strike AND instrument_type = t1.instrument_type) - 
        (SELECT OI FROM test_assignment 
         WHERE date = '{date1}' AND strike = t1.strike AND instrument_type = t1.instrument_type) as OI_difference
    FROM test_assignment t1
    WHERE date = '{date1}'
    GROUP BY strike, instrument_type, OI_difference
"""

# Execute the SQL query and store the result in a pandas DataFrame
result = pd.read_sql_query(query, conn)

# Print the result
print(result)

# Close the database connection
conn.close()
