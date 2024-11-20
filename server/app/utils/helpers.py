def serialize_bill(bill):
    return {
        "id": bill.id,
        "name": bill.name,
        "label": bill.label,
        "status": bill.status,
        "total_sum": bill.total_sum,
        "created_at": bill.created_at,
        "users": [user.id for user in bill.users]
    }
