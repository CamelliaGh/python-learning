def binary_search_recursive(n, sorted_array, left=0, right=None):

    if right is None:
        right = len(sorted_array) - 1

    if left > right:
        return -1

    middle = (right + left) // 2

    if n == sorted_array[middle]:
        return middle
    elif n > sorted_array[middle]:
        return binary_search_recursive(n, sorted_array, middle + 1, right)
    else:
        return binary_search_recursive(n, sorted_array, left, middle - 1)


def binary_search(n, sorted_array):
    low = 0
    high = len(sorted_array)

    while high - low > 1:
        middle = (low + high) // 2

        if n > sorted_array[middle]:
            low = middle
        else:
            high = middle
    return low if sorted_array[low] == n else None


if __name__ == '__main__':
    # print(binary_search_recursive(10, [2, 3, 4, 10, 16, 20, 35, 49, 55]))
    # print(binary_search_recursive(1, [1]))
    # print(binary_search_recursive(1, []))

    # print(binary_search(10, [2, 3, 4, 10, 16, 20, 35, 49, 55]))
    # print(binary_search(1, [1]))
    # print(binary_search(1, []))
    print(binary_search_recursive(9, [7, 8, 9, 2, 3, 4],3,-6))
