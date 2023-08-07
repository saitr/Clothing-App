from validate_email import validate_email
import dns.resolver

def is_valid_email(email):
    is_valid_format = validate_email(email)
    if not is_valid_format:
        return False
    
    domain = email.split('@')[1]
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return len(answers) > 0
    except dns.resolver.NoAnswer:
        return False

def main():
    email = input("Enter the email address to verify: ")
    if is_valid_email(email):
        print(f"{email} is a valid and deliverable email address.")
    else:
        print(f"{email} is not a valid email address or does not exist. Please enter a valid email address")

if __name__ == "__main__":
    main()
