# From: https://www.geeksforgeeks.org/check-if-a-string-represents-a-hexadecimal-number-or-not/
# Ideally this would utilize regex https://www.geeksforgeeks.org/how-to-validate-hexadecimal-color-code-using-regular-expression/

def isValidHex(s):
   
    # Iterate over string
    for ch in s:
 
        # Check if the character
        # is invalid
        if ((ch < '0' or ch > '9') and
            (ch < 'A' or ch > 'F')):
            return False
    return True