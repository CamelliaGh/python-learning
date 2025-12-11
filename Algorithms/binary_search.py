def binary_search(n, array):  # [0,1,2,3,4]
    left = 0
    right = len(array) - 1
    while right - left >= 0:
        mid = (left + right) // 2
        if array[mid] == n:
            return mid
        if array[mid] > n:
            right = mid - 1
        else:
            left = mid + 1
    return -1


def binary_search_recursive(n, array, left=0, right=None):

    if right is None:
        right = len(array) - 1
    if left > right:
        return -1

    middle = (right + left) // 2
    if array[middle] == n:
        return middle

    if array[middle] > n:
        return binary_search_recursive(n, array, left, middle - 1)
    else:
        return binary_search_recursive(n, array, middle + 1, right)


# print(binary_search(1, [0, 1, 2, 3, 4]))
# print(binary_search(4, [0, 1, 2, 3, 4]))
print(binary_search_recursive(4, [0, 1, 2, 3, 4]))
print(binary_search_recursive(0, [0, 1, 2, 3, 4]))
print(binary_search_recursive(3, [0, 1, 2, 3, 4]))
print(binary_search_recursive(1, [0, 1], 0, 1))
print(binary_search_recursive(0, [0]))
