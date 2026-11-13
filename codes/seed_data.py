from database import create_tables, get_connection

def insert_dummy_records():
    create_tables()
    connection = get_connection()
    
    pensioners = [
        (
            "Rajesh Kumar",
            "PPO202400123",
            "1958-05-15",
            "State Bank of India",
            "123456789012",
            "SBIN0001234",
            "rajesh.demo@gmail.com",
            "9000000001"
        ),
        (
            "Suresh Sharma",
            "PPO202400456",
            "1960-08-20",
            "Punjab National Bank",
            "456789123012",
            "PUNB0001234",
            "suresh.demo@gmail.com",
            "9000000002"
        ),
        (
            "Amit Verma",
            "PPO202400789",
            "1959-12-10",
            "Bank of Baroda",
            "789123456012",
            "BARB0001234",
            "amit.demo@gmail.com",
            "9000000003"
        ),
        (
            "Spriha Sahu",
                        "PPO202400788",
                        "1959-12-10",
                        "Bank of Baroda",
                        "789123456012",
                        "BARB0001234",
                        "sprihasahu@gmail.com",
                        "9000000003"
        )
    ]
    
    connection.executemany("""
    INSERT OR IGNORE INTO pensioners (
        name, ppo_number, date_of_birth, bank_name,
        account_number, ifsc, email, mobile
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, pensioners)
    
    connection.commit()
    connection.close()
    print("Dummy pensioner records inserted successfully.")

if __name__ == "__main__":
    insert_dummy_records()