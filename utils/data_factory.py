from uuid import uuid4


def unique_suffix() -> str:
    return uuid4().hex[:8]


def customer_data():
    suffix = unique_suffix()
    return {
        "name": f"QA Customer {suffix}",
        "email": f"qa_{suffix}@example.com",
        "phone": "9876543210",
    }


def product_data():
    suffix = unique_suffix()
    return {
        "name": f"QA Product {suffix}",
        "sku": f"SKU-{suffix.upper()}",
        "price": "1000",
        "stock": "25",
    }
