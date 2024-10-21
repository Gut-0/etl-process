class NumberSet:
    def __init__(self):
        self.numbers = set(range(1, 101))
        self.extracted = []

    def extract(self, number):
        if not isinstance(number, int):
            return "The number must be an integer."
        if number < 1 or number > 100:
            return "The number must be between 1 and 100."
        if number in self.numbers:
            self.numbers.remove(number)
            self.extracted.append(number)
            return f"Extracted number: {number}"
        else:
            return f"The number {number} has already been extracted."


def main():
    number_set = NumberSet()

    try:
        for _ in range(4):
            user_number = int(input("Enter a number between 1 and 100 to extract: "))
            result = number_set.extract(user_number)
            print(result)

    except ValueError:
        print("Error: Please enter a valid integer.")

    print(f"All extracted numbers: {number_set.extracted}")
    print(f"Remaining numbers: {sorted(number_set.numbers)}")


if __name__ == "__main__":
    main()
