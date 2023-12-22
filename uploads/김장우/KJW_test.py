def palindrome(s):
    return s == s[::-1]

def quasi_palindrome(s):
    for i in range(len(s)):
        s2 = s[:i] + s[i+1:]
        if palindrome(s2):
            return True
    return False

def main():
    n = int(input())

    for _ in range(n):
        x = input().lower()
        if palindrome(x):
            print("1")
        elif quasi_palindrome(x):
            print("2")
        else:
            print("3")

if __name__ == "__main__":
    main()