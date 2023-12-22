def is_palindrome(s):
    if len(s) <= 1:
        return True
    if s[0] == s[-1]:
        return is_palindrome(s[1:-1])
    return False

def check_palindrome(s):
    s = ''.join(s.split()).lower()
    
    if is_palindrome(s):
        return 1
    
    for i in range(len(s)):
        if is_palindrome(s[:i] + s[i+1:]):
            return 2
    
    return 3