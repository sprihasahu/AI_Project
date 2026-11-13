from database import get_connection

def get_certificate_history(pensioner_id):
    connection = get_connection()
    rows = connection.execute("""
    SELECT certificate_id, submitted_ppo, submitted_account,
           submitted_ifsc, status, rejection_reason, submission_date
    FROM life_certificates
    WHERE pensioner_id = ?
    ORDER BY certificate_id DESC
    """, (pensioner_id,)).fetchall()
    
    connection.close()
    return [dict(row) for row in rows]

def get_all_certificates():
    connection = get_connection()
    rows = connection.execute("""
    SELECT c.certificate_id, p.name, p.ppo_number,
           c.submitted_ppo, c.status, c.rejection_reason,
           c.submission_date
    FROM life_certificates AS c
    INNER JOIN pensioners AS p
    ON c.pensioner_id = p.pensioner_id
    ORDER BY c.certificate_id DESC
    """).fetchall()
    
    connection.close()
    return [dict(row) for row in rows]