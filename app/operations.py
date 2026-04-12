def add(a: float, b: float) -> float:
    return a + b

def subtract(a: float, b: float) -> float:
    return a - b

def multiply(a: float, b: float) -> float:
    return a * b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
    
# ...existing code...

# Factory Pattern Implementation
class CalculationOperation:
    def compute(self, a: float, b: float) -> float:
        raise NotImplementedError()

class AddOperation(CalculationOperation):
    def compute(self, a: float, b: float) -> float:
        return add(a, b)

class SubOperation(CalculationOperation):
    def compute(self, a: float, b: float) -> float:
        return subtract(a, b)

class MultiplyOperation(CalculationOperation):
    def compute(self, a: float, b: float) -> float:
        return multiply(a, b)

class DivideOperation(CalculationOperation):
    def compute(self, a: float, b: float) -> float:
        return divide(a, b)

class CalculationFactory:
    operations = {
        "Add": AddOperation(),
        "Sub": SubOperation(),
        "Multiply": MultiplyOperation(),
        "Divide": DivideOperation(),
    }

    @classmethod
    def get_operation(cls, op_type: str) -> CalculationOperation:
        if op_type not in cls.operations:
            raise ValueError(f"Invalid calculation type: {op_type}")
        return cls.operations[op_type]