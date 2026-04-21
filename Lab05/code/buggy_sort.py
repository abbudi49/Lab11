# Sorting algorithms with intentional bugs
# Task: Ask AI to find and explain the bugs

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i):   # Bug 1: should be n - i - 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def binary_search(arr, target):
    left = 0
    right = len(arr)              # Bug 2: should be len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid            # Bug 3: should be mid + 1
        else:
            right = mid - 1
    return -1

def count_occurrences(arr, target):
    count = 0
    for i in range(len(arr) + 1):  # Bug 4: should be len(arr)
        if arr[i] == target:
            count += 1
    return count

def remove_duplicates(lst):
    result = []
    for item in lst:
        if item not in lst:        # Bug 5: should check `result`, not `lst`
            result.append(item)
    return result


if __name__ == "__main__":
    data = [64, 34, 25, 12, 22, 11, 90]
    print("Sorted:", bubble_sort(data.copy()))
    print("Search 25:", binary_search(sorted(data), 25))
    print("Count 22:", count_occurrences(data, 22))
    print("No duplicates:", remove_duplicates([1, 2, 2, 3, 3, 4]))
