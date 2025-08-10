import re
import random
import string

def check_password_strength(password):
    suggestions = []
    is_strong = True

    # Check length
    if len(password) < 12:
        suggestions.append("Password should be at least 12 characters long.")
        is_strong = False

    # Check for uppercase letters
    if not re.search(r'[A-Z]', password):
        suggestions.append("Add at least one uppercase letter (A-Z).")
        is_strong = False

    # Check for lowercase letters
    if not re.search(r'[a-z]', password):
        suggestions.append("Add at least one lowercase letter (a-z).")
        is_strong = False

    # Check for numbers
    if not re.search(r'[0-9]', password):
        suggestions.append("Add at least one number (0-9).")
        is_strong = False

    # Check for special characters
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        suggestions.append("Add at least one special character (e.g., !@#$%^&*).")
        is_strong = False

    # Check for common patterns (simple example)
    common_weak_patterns = ["password", "123", "qwerty", "admin"]
    if any(pattern in password.lower() for pattern in common_weak_patterns):
        suggestions.append("Avoid common words or patterns.")
        is_strong = False

    return is_strong, suggestions

def generate_strong_password(length=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*(),.?\":{}|<>"
    while True:
        password = ''.join(random.choice(chars) for _ in range(length))
        is_strong, _ = check_password_strength(password)
        if is_strong:
            return password

# Example usage:
user_password = input("Enter your password to check: ")
is_strong, suggestions = check_password_strength(user_password)

if is_strong:
    print("✅ Your password is strong!")
else:
    print("❌ Your password is weak. Suggestions to improve:")
    for suggestion in suggestions:
        print(f"- {suggestion}")
    new_password = generate_strong_password()
    print(f"\n💡 Here's a stronger password suggestion: {new_password}")
