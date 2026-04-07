import random

def generate_barcode() -> str:
    """Simple unique barcode generator"""
    return "B" + str(random.randint(1000000000, 9999999999))
