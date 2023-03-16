def binary_search(list, target):
    l = 0
    r = len(list) - 1
    while l <= r:
        mid = (l + r) // 2
        if list[mid] == target:
            return mid
        elif list[mid] < target:
            l = mid + 1
        else:
            r = mid - 1
    return None

list = [1, 2, 3, 4, 5, 6]
print(binary_search(list, 5))