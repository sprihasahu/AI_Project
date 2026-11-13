from datetime import datetime
from database import get_connection

def verify_certificate(pensioner, submitted_ppo,
                       submitted_account, submitted_ifsc):
    errors = []
    
    if submitted_ppo.strip().upper() != pensioner["ppo_number"].upper():
        errors.append("PPO number does not match registered records. ")
        
    if submitted_account.strip() != pensioner["account_number"]:
        errors.append("Bank account number does not match. ")
        
    if submitted_ifsc.strip().upper() != pensioner["ifsc"].upper():
        errors.append("IFSC code does not match.")
        
    if errors:
        status = "REJECTED"
        rejection_reason = "".join(errors)
    else:
        status = "APPROVED"
        rejection_reason = None
        
    connection = get_connection()
    cursor = connection.execute("""
    INSERT INTO life_certificates (
        pensioner_id, submitted_ppo, submitted_account,
        submitted_ifsc, status, rejection_reason, submission_date
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        pensioner["pensioner_id"],
        submitted_ppo.strip(),
        submitted_account.strip(),
        submitted_ifsc.strip().upper(),
        status,
        rejection_reason,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    
    certificate_id = cursor.lastrowid
    connection.commit()
    connection.close()
    
    return {
        "certificate_id": certificate_id,
        "status": status,
        "errors": errors,
        "reason": rejection_reason
    }