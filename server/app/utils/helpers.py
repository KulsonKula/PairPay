import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def log_wrapper(func):
    def wrapper(*args, **kwargs):
        logging.info(
            f"Wywołanie funkcji '{func.__name__}' z argumentami: {args}, {kwargs}"
        )

        result = func(*args, **kwargs)

        logging.info(f"Funkcja '{func.__name__}' zakończona. Wynik: {result}")

        return result

    return wrapper


def serialize_bill(bill):
    return {
        "id": bill.id,
        "user_creator_id": bill.user_creator_id,
        "name": bill.name,
        "label": bill.label,
        "status": bill.status,
        "total_sum": bill.total_sum,
        "created_at": bill.created_at,
        "users": [user.id for user in bill.users],
    }
