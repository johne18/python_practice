def calculate_total(
        first_number: int | float, 
        second_number: int | float,
    ) -> int | float:
    if not isinstance(first_number, (int, float)):
        raise TypeError(
            "first_number must be numeric. Ex: 1 or 1.0"
        )

    if not isinstance(second_number, (int, float)):
        raise TypeError(
            "second_number must be numeric. Ex: 1 or 1.0"
        )

    return first_number + second_number


def contains_substring(
        message: str, 
        substring: str,
    ) -> bool:
    if not isinstance(message, str):
        raise TypeError("message must be a string")

    if not isinstance(substring, str):
        raise TypeError("substring must be a string")

    if not message or not substring:
        raise ValueError("both message and substring cannot be empty")

    return substring in message

if __name__ == "__main__":
    print(calculate_total(3154, 234))
    print(contains_substring("Python in Docker", "Docker"))
    print(contains_substring("Python in Docker", "bleh"))