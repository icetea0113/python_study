def is_palindrome(s):
    return s == s[::-1]

def is_similar_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            remove_left = s[left + 1:right + 1]
            remove_right = s[left:right]
            return is_palindrome(remove_left) or is_palindrome(remove_right)
        left += 1
        right -= 1
    return True

def main():
    string = input("Enter a string: ")
    if is_palindrome(string):
        print(1)  # Palindrome
    elif is_similar_palindrome(string):
        print(2)  # Similar palindrome
    else:
        print(3)  # Neither