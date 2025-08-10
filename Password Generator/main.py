import random
import string

def generate_password(length=12, use_uppercase=True, use_digits=True, use_special=True):
    """Generate a secure random password."""
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase if use_uppercase else ""
    digits = string.digits if use_digits else ""
    special = string.punctuation if use_special else ""
    
    all_chars = lower + upper + digits + special
    
    if not all_chars:
        raise ValueError("No character types selected for password generation.")
    
    # Ensure at least one of each selected type
    password = []
    if use_uppercase:
        password.append(random.choice(upper))
    if use_digits:
        password.append(random.choice(digits))
    if use_special:
        password.append(random.choice(special))
    
    # Fill the rest of the password length
    password += random.choices(all_chars, k=length - len(password))
    
    # Shuffle to avoid predictable patterns
    random.shuffle(password)
    
    return "".join(password)

if __name__ == "__main__":
    print("=== Password Generator ===")
    length = int(input("Enter password length: "))
    use_uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'
    use_digits = input("Include digits? (y/n): ").lower() == 'y'
    use_special = input("Include special characters? (y/n): ").lower() == 'y'
    
    try:
        password = generate_password(length, use_uppercase, use_digits, use_special)
        print("\nGenerated Password:", password)
    except ValueError as e:
        print("Error:", e)
