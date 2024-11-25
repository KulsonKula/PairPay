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
