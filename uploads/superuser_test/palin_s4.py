def palindrome(front: int, rear: int, status: int) -> int:
    if status > 3:
        return 3

    while tmp[front] == tmp[rear] and front < rear:
        front += 1
        rear -= 1

    if front >= rear:
        return status
    else:
        res1 = palindrome(front+1, rear, status+1)
        res2 = palindrome(front, rear-1, status+1)
        return min(res1, res2)


if __name__ == '__main__':
    n = int(input())
    for _ in range(n):
        tmp = list(input().strip())
        print(palindrome(0, len(tmp) - 1, 1))
