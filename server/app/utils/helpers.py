def serialize_bill(bill):
    return {
        "id": bill.id,
        "user_creator_id": bill.user_creator_id,
        "name": bill.name,
        "label": bill.label,
        "status": bill.status,
        "total_sum": bill.total_sum,
        "created_at": bill.created_at,
        "users": [user.id for user in bill.users]
    }
