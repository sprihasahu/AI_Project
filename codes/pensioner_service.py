from database import get_connection

def get_pensioner_by_ppo(ppo_number):
    connection = get_connection()
    row = connection.execute("""
    SELECT *
    FROM pensioners
    WHERE ppo_number = ?
    """, (ppo_number.strip(),)).fetchone()
    
    connection.close()
    return dict(row) if row else None

def get_pensioner_by_id(pensioner_id):
    connection = get_connection()
    row = connection.execute("""
    SELECT *
    FROM pensioners
    WHERE pensioner_id = ?
    """, (pensioner_id,)).fetchone()
    
    connection.close()
    return dict(row) if row else None

def get_all_pensioners():
    connection = get_connection()
    rows = connection.execute("""
    SELECT pensioner_id, name, ppo_number, date_of_birth,
    bank_name, account_number, ifsc, email, mobile
    FROM pensioners
    ORDER BY pensioner_id
    """).fetchall()
    
    connection.close()
    return [dict(row) for row in rows]