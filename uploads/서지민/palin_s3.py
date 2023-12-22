n = int(input())

def check_palin(s):
    left, right = 0, len(s) - 1
    
    while left < right:
        if s[left] != s[right]:
            #왼쪽 삭제 혹은 오른쪽 삭제
            if s[left+1:right+1] == s[left+1:right+1][::-1] or s[left:right] == s[left:right][::-1]:
                print(2)
                return
            else:
                print(3)
                return
        left += 1
        right -= 1
    print(1)
    return

for _ in range(n):
    value = input()
    check_palin(value)