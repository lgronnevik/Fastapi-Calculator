import logging

logger = logging.getLogger(__name__)

def add(a: float, b: float) -> float:
    result = a + b
    logger.info(f"Adding {a} + {b} = {result}")
    return result

def subtract(a: float, b: float) -> float:
    result = a - b
    logger.info(f"Subtracting {a} - {b} = {result}")
    return result

def multiply(a: float, b: float) -> float:
    result = a * b
    logger.info(f"Multiplying {a} * {b} = {result}")
    return result

def divide(a: float, b: float) -> float:
    if b == 0:
        logger.error("Attempted division by zero")
        raise ValueError("Cannot divide by zero")
    result = a / b
    logger.info(f"Dividing {a} / {b} = {result}")
    return result