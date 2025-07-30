import streamlit as st
import pandas as pd
import altair as alt
import time
import random

# ------------------------- Setup ------------------------
st.set_page_config(page_title="Sorting Visualizer", layout="wide")
st.title("Sorting Algorithm Visualizer")
st.markdown("Watch sorting algorithms in action, with visual updates and live description.")

# ------------------------- Sidebar ------------------------
algo = st.sidebar.selectbox("Choose Sorting Algorithm", 
                            ["Bubble Sort", "Insertion Sort", "Selection Sort", "Quick Sort", "Merge Sort", "Bogo Sort", "Sleep Sort"])
num_elements = st.sidebar.slider("Number of Elements", 5, 90, 15)
speed = st.sidebar.slider("Animation Speed (lower is faster)", 0.001, 0.3, 0.03, step=0.01)

# ------------------------- Descriptions ------------------------
DESCRIPTIONS = {
    "Bubble Sort": [
        "Bubble Sort compares adjacent elements and swaps them if they’re in the wrong order.",
        "This process is repeated for each element, gradually 'bubbling' the largest value to the end.",
        "It’s simple but inefficient for large arrays.",
        "Best case: O(n) when already sorted | Worst case: O(n²)",
        "Space complexity: O(1) | Stable: Yes"
    ],
    "Insertion Sort": [
        "Insertion Sort works like sorting playing cards in your hands.",
        "Each element is compared to its predecessors and inserted into the correct position.",
        "It is efficient for small or nearly sorted datasets.",
        "Best case: O(n) | Worst case: O(n²)",
        "Space complexity: O(1) | Stable: Yes"
    ],
    "Selection Sort": [
        "Selection Sort divides the array into sorted and unsorted parts.",
        "It repeatedly selects the smallest element from the unsorted section and places it in the sorted part.",
        "It performs the minimum number of swaps (at most n).",
        "Time complexity: O(n²) always | Space: O(1)",
        "Stable: No (can be made stable with extra logic)"
    ],
    "Quick Sort": [
        "Quick Sort uses divide and conquer strategy with a pivot element.",
        "Elements smaller than the pivot go to the left, larger to the right.",
        "It's fast in practice and has good cache performance.",
        "Best/Average: O(n log n) | Worst: O(n²) when poorly partitioned",
        "Space: O(log n) average | Stable: No"
    ],
    "Merge Sort": [
        "Merge Sort splits the array into halves until each part has one element.",
        "It then merges these sorted halves back together.",
        "Always performs in O(n log n) time regardless of initial order.",
        "Good for linked lists and external sorting.",
        "Time: O(n log n) | Space: O(n) | Stable: Yes"
    ],
    "Bogo Sort": [
        "Bogo Sort is a joke algorithm: it randomly shuffles the array until sorted.",
        "It’s an example of a highly inefficient brute-force approach.",
        "Expected time: O(n!) | Worst case: ∞ theoretically!",
        "It’s more for amusement than practical use.",
        "Space: O(1) | Stable: Random 😄",
        "Keep it 5 to see the effect!"
    ],
    "Sleep Sort": [
        "Sleep Sort uses the value of each number to determine its delay in being 'emitted'.",
        "In real implementations, each number sleeps for a time proportional to its value.",
        "It's mostly used as a quirky visual or educational sort.",
        "Time complexity: ~O(n log n) (due to sorting visualization structure)",
        "Space: O(n) due to timers or threads | Stable: Yes"
    ]
}


# ------------------------- Algorithms ------------------------
def bubble_sort(data):
    frames = []
    arr = data.copy()
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            frames.append((arr.copy(), j, j+1))
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                frames.append((arr.copy(), j, j+1))
        if not swapped:
            break
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
    def quicksort(low, high):
        if low < high:
            pi = partition(low, high)
            quicksort(low, pi - 1)
            quicksort(pi + 1, high)
    def partition(low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            frames.append((arr.copy(), j, high))
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                frames.append((arr.copy(), i, j))
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        frames.append((arr.copy(), i + 1, high))
        return i + 1
    quicksort(0, len(arr) - 1)
    return frames

def merge_sort(data):
    frames = []
    arr = data.copy()
    def merge_sort_recursive(left, right):
        if left < right:
            mid = (left + right) // 2
            merge_sort_recursive(left, mid)
            merge_sort_recursive(mid + 1, right)
            merge(left, mid, right)
    def merge(left, mid, right):
        L = arr[left:mid+1]
        R = arr[mid+1:right+1]
        i = j = 0
        k = left
        while i < len(L) and j < len(R):
            frames.append((arr.copy(), k, k))
            if L[i] < R[j]:
                arr[k] = L[i]; i += 1
            else:
                arr[k] = R[j]; j += 1
            k += 1
            frames.append((arr.copy(), k-1, k-1))
        while i < len(L):
            arr[k] = L[i]; i += 1; k += 1
            frames.append((arr.copy(), k-1, k-1))
        while j < len(R):
            arr[k] = R[j]; j += 1; k += 1
            frames.append((arr.copy(), k-1, k-1))
    merge_sort_recursive(0, len(arr)-1)
    return frames

def is_sorted(arr):
    return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))

def bogo_sort(data):
    frames = []
    arr = data.copy()
    attempts = 0
    max_attempts = 10_000  # Safety limit to prevent freezing

    while not is_sorted(arr):
        frames.append((arr.copy(), -1, -1))
        random.shuffle(arr)
        attempts += 1
        if attempts > max_attempts:
            break  # Optional: to avoid infinite loop

    # Final sorted frame
    if is_sorted(arr):
        frames.append((arr.copy(), -1, -1))
    return frames


def sleep_sort(data):
    frames = []
    arr = data.copy()
    indices = sorted(range(len(arr)), key=lambda i: arr[i])
    sorted_arr = [0] * len(arr)
    for i, idx in enumerate(indices):
        sorted_arr[i] = arr[idx]
        frames.append((sorted_arr.copy(), i, i))
    return frames

# ------------------------- Main Logic ------------------------
if st.button("Start Sorting"):
    data = random.sample(range(10, 100), num_elements)
    chart_container = st.empty()
    desc_container = st.empty()

    # Prepare frames
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
    elif algo == "Bogo Sort":
        frames = bogo_sort(data)
    elif algo == "Sleep Sort":
        frames = sleep_sort(data)

    desc_lines = DESCRIPTIONS[algo]
    line_idx = 0
    char_idx = 0
    typed_lines = []
    typed_line = ""
    typing_delay = 0.03  
    last_type_time = time.time()

    # --- Streamlit containers ---
    chart_container = st.empty()
    desc_container = st.empty()

    # --- Sorting setup ---
    frame_idx = 0
    max_frames = len(frames)

    # --- Animation Loop ---
    while frame_idx < max_frames or line_idx < len(desc_lines):

        # ---- Render sorting frame ----
        if frame_idx < max_frames:
            frame, idx1, idx2 = frames[frame_idx]
            df = pd.DataFrame({
                'index': list(range(len(frame))),
                'value': frame,
                'color': ['red' if i == idx1 or i == idx2 else 'steelblue' for i in range(len(frame))]
            })

            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('index:O', title='Index'),
                y=alt.Y('value:Q'),
                color=alt.Color('color:N', scale=None),
                tooltip=['index', 'value']
            ).properties(height=400)

            chart_container.altair_chart(chart, use_container_width=True)
            frame_idx += 1
            time.sleep(speed)  # user-controlled sorting speed

        if line_idx < len(desc_lines):
            now = time.time()
            if now - last_type_time >= typing_delay:
                line = desc_lines[line_idx]

                if char_idx <= len(line):
                    typed_line = line[:char_idx] + "▌"
                    char_idx += 1

                if char_idx > len(line):
                    typed_lines.append(line)
                    line_idx += 1
                    char_idx = 0
                    typed_line = ""

                # Render the description
                full_description = ""
                for i in range(len(desc_lines)):
                    if i < len(typed_lines):
                        full_description += f"- {typed_lines[i]}<br>"
                    elif i == line_idx:
                        full_description += f"- {typed_line}<br>"

                desc_container.markdown("**Description:**<br>" + full_description, unsafe_allow_html=True)
                last_type_time = now

    desc_container.markdown("**Description:**<br>" + "<br>".join(f"- {line}" for line in desc_lines), unsafe_allow_html=True)
    time.sleep(1.2)
