def calculate(num1, num2, operation):
    try:
        if operation == '+':
            return num1 + num2
        elif operation == '-':
            return num1 - num2
        elif operation == '*':
            return num1 * num2
        elif operation == '/':
            if num2 == 0:
                return "You can't divide by zero!"
            return num1 / num2
        else:
            return "Unknown operator"
    except Exception as e:
        return f"There's an error: {e}"

print("Dumb Calculator")
num1 = float(input("What will be your first operand?: "))
num2 = float(input("And the second one?: "))
operation = input("Choose operator (+, -, *, /): ")

result = calculate(num1, num2, operation)
print(f"Result: {result}")