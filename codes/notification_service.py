def generate_whatsapp_message(name, certificate_id, reason):
    return f"""
Dear {name},

Your Life Certificate submission was REJECTED
in the demonstration application.
Certificate ID: {certificate_id}
Reason: {reason}

Please check your registered PPO and bank details,
then make a corrected submission. Contact your bank
or pension authority if you need official assistance.

Pension Assistance Demo
"""

def generate_success_message(name, certificate_id):
    return f"""
Dear {name},

Your submission passed the local demo checks.
Certificate ID: {certificate_id}

This is NOT official bank or government approval.
Please follow the official pension authority process.

Pension Assistance Demo
"""