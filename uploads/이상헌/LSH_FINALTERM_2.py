def is_palindrome(s):
    return s == s[::-1]

def is_quasi_palindrome(s):
    for i in range(len(s) // 2):
        if s[i] != s[len(s) - 1 - i]:
            new_s = s[:i] + s[i + 1:]
            return is_palindrome(new_s)
    return True

def classify_string(s):
    s = s.lower()
    return 1 if is_palindrome(s) else (2 if is_quasi_palindrome(s) else 3)

def main():
    N = int(input())
    for _ in range(N):
        input_str = input().strip()
        print(classify_string(input_str))

if __name__ == "__main__":
    main()