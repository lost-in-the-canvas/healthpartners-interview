def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def main():
    result = fibonacci(30)
    print(f"The 30th Fibonacci number is: {result}")

if __name__ == "__main__":
    main()
