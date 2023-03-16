def merge_sort(list):
    if len(list) <= 1:
        return list
    else:
        mid = len(list) // 2
        # sort left
        left = merge_sort(list[:mid])
        # sort right
        right = merge_sort(list[mid:])

        # print(f"List: {list}")
        # print(f"L: {left}")
        # print(f"R: {right}")

        ans = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                ans.append(left[i])
                i += 1
            else:
                ans.append(right[j])
                j += 1
        while i < len(left):
            ans.append(left[i])
            i += 1
        while j < len(right):
            ans.append(right[j])
            j += 1
        return ans

list = [5,4,4,3,2,1,6]
print(merge_sort(list))