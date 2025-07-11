import streamlit as st
import pandas as pd
import altair as alt
import time
import random

st.set_page_config(page_title="Sorting Visualizer", layout="wide")
st.title("📊 Sorting Algorithm Visualizer")
st.markdown("Visualize how different sorting algorithms work with smooth animations and dynamic coloring.")

# Sidebar
algo = st.sidebar.selectbox("Choose Sorting Algorithm", 
                            ["Bubble Sort", "Insertion Sort", "Selection Sort", "Quick Sort", "Merge Sort"])
num_elements = st.sidebar.slider("Number of Elements", 5, 90, 15)
speed = st.sidebar.slider("Animation Speed (lower is faster)", 0.001, 0.3, 0.05, step=0.01)

# -------- Sorting Algorithms with Color Tracking --------

def bubble_sort(data):
    frames = []
    arr = data.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            frames.append((arr.copy(), j, j+1))  # Track indices being compared
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                frames.append((arr.copy(), j, j+1))  # Frame after swap
    return frames

def insertion_sort(data):
    frames = []
    arr = data.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            frames.append((arr.copy(), j, j + 1))
            j -= 1
        arr[j + 1] = key
        frames.append((arr.copy(), j + 1, i))
    return frames

def selection_sort(data):
    frames = []
    arr = data.copy()
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            frames.append((arr.copy(), i, j))
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        frames.append((arr.copy(), i, min_idx))
    return frames

def quick_sort(data):
    frames = []
    arr = data.copy()

    def quicksort(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quicksort(arr, low, pi - 1)
            quicksort(arr, pi + 1, high)

    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            frames.append((arr.copy(), j, high))  # comparing with pivot
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                frames.append((arr.copy(), i, j))
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        frames.append((arr.copy(), i+1, high))
        return i + 1

    quicksort(arr, 0, len(arr) - 1)
    return frames

def merge_sort(data):
    frames = []
    arr = data.copy()

    def merge_sort_recursive(arr, left, right):
        if left < right:
            mid = (left + right) // 2
            merge_sort_recursive(arr, left, mid)
            merge_sort_recursive(arr, mid + 1, right)
            merge(arr, left, mid, right)

    def merge(arr, left, mid, right):
        L = arr[left:mid + 1]
        R = arr[mid + 1:right + 1]

        i = j = 0
        k = left

        while i < len(L) and j < len(R):
            frames.append((arr.copy(), k, k))
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
            frames.append((arr.copy(), k-1, k-1))

        while i < len(L):
            frames.append((arr.copy(), k, k))
            arr[k] = L[i]
            i += 1
            k += 1
            frames.append((arr.copy(), k-1, k-1))

        while j < len(R):
            frames.append((arr.copy(), k, k))
            arr[k] = R[j]
            j += 1
            k += 1
            frames.append((arr.copy(), k-1, k-1))

    merge_sort_recursive(arr, 0, len(arr) - 1)
    return frames

# ---------- Run Sorting ----------
if st.button("Start Sorting"):
    data = random.sample(range(10, 100), num_elements)

    if algo == "Bubble Sort":
        frames = bubble_sort(data)
    elif algo == "Insertion Sort":
        frames = insertion_sort(data)
    elif algo == "Selection Sort":
        frames = selection_sort(data)
    elif algo == "Quick Sort":
        frames = quick_sort(data)
    elif algo == "Merge Sort":
        frames = merge_sort(data)

    chart_container = st.empty()

    for frame, idx1, idx2 in frames:
        df = pd.DataFrame({
            'index': list(range(len(frame))),
            'value': frame,
            'color': ['red' if i == idx1 or i == idx2 else 'steelblue' for i in range(len(frame))]
        })

        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('index:O', axis=None, title=None),
            y=alt.Y('value:Q', title=None),
            color=alt.Color('color:N', scale=None),  # Use exact color names
            tooltip=['index', 'value']
        ).properties(
            height=400
        )

        chart_container.altair_chart(chart, use_container_width=True)
        time.sleep(speed)
