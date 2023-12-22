def palindrome(s):
    return s == s[::-1]

def similar_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            temp_left = s[left:right]
            temp_right = s[left + 1:right + 1]
            return palindrome(temp_left) or palindrome(temp_right)
        left += 1
        right -= 1
    return True

def main():
    n = int(input().strip())  # 문자열의 개수 N을 입력받음
    results = []
    for _ in range(n):
        s = input().strip()  # N개의 문자열을 차례로 입력받음
        if palindrome(s):
            results.append(1)
        elif similar_palindrome(s):
            results.append(2)
        else:
            results.append(3)

    for result in results:
        print(result)

if __name__ == "__main__":
    main()
