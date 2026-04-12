import random
import string
"""Step 1: Initialize an empty set for passwords.

Step 2: Loop until the set has 100 unique passwords.

Step 3: For each password: pick 1 uppercase letter, then pick 6 characters from (letters, digits, symbols).

Step 4: If unique, add to the set.

Step 5: Save the results to a TXT/CSV file."""

def generate_passwords(count=100):
    passwords = set()
    first_char_pool = string.ascii_uppercase  
    
    digits = string.digits                    
    symbols = "@#$%,&"                        
    letters = string.ascii_letters            
    
    remaining_pool = digits + symbols + letters
    
    while len(passwords) < count:
        first_char = random.choice(first_char_pool)
        
        remaining_chars = ''.join(random.choices(remaining_pool, k=6))
        

        full_password = first_char + remaining_chars
        passwords.add(full_password)
    
    return list(passwords)

generated_passwords = generate_passwords(100)

#Store the 100 generated passwords in a text file
try:
    with open("generated_passwords.txt", "w") as file:
        for index, password in enumerate(generated_passwords, 1):
            file.write(f"{index}. {password}\n")
    print("Success: 100 passwords have been saved to 'generated_passwords.txt'.")
except IOError as e:
    print(f"Error saving to file: {e}")

# Displaying the first 5 passwords as a sample
print("\nSample of generated passwords:")
for pwd in generated_passwords[:5]:
    print(pwd)