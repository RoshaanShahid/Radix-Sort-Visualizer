import tkinter as tk
from tkinter import ttk
import json


def counting_sort(arr, exp, pass_num, text_widget, all_passes):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1

    for i in range(n):
        arr[i] = output[i]

    pass_output = {f"{ordinal(pass_num)} pass": arr.copy()}
    text_widget.insert(tk.END, json.dumps(pass_output, indent=4) + "\n")

    all_passes.append(arr.copy())


def radix_sort(arr, text_widget, size_entry, array_entry):
    size = int(size_entry.get())
    try:
        arr = [int(x) for x in array_entry.get().split()]
        if len(arr) != size:
            raise ValueError("Invalid array size.")
    except ValueError:
        text_widget.insert(tk.END, "Invalid input. Please enter a valid array.\n")
        return

    max_num = max(arr)
    exp = 1

    text_widget.insert(tk.END, f"The Array: {str(tuple(arr))}\n\n")

    all_passes = []

    # First pass
    counting_sort(arr, exp, 1, text_widget, all_passes)

    # Second pass
    exp *= 10
    counting_sort(arr, exp, 2, text_widget, all_passes)

    # Third pass
    exp *= 10
    counting_sort(arr, exp, 3, text_widget, all_passes)

    text_widget.insert(tk.END, "\nSo the Sorted Array is " + str(tuple(all_passes[-1])) + "\n")

def reset_visualizer(size_entry, array_entry, text_widget):
    size_entry.delete(0, tk.END)
    array_entry.delete(0, tk.END)
    text_widget.delete(1.0, tk.END)

def ordinal(num):
    if 10 <= num % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(num % 10, 'th')
    return f"{num}{suffix}"


def main():
    root = tk.Tk()
    root.title("Radix Sort Visualization")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = 800
    window_height = 600
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    title_label = tk.Label(root, text="Radix Sort", font=("Helvetica", 20, "bold"))
    title_label.pack()

    text_widget = tk.Text(root, height=20, width=70, wrap=tk.WORD)
    text_widget.pack(padx=10, pady=10)

    size_label = tk.Label(root, text="Enter size of the array:")
    size_label.pack()

    size_entry = tk.Entry(root)
    size_entry.pack()

    array_label = tk.Label(root, text="Enter the array (space-separated):")
    array_label.pack()

    array_entry = tk.Entry(root)
    array_entry.pack()

    sort_button = ttk.Button(root, text="Start Sorting",
                             command=lambda: radix_sort([], text_widget, size_entry, array_entry))
    sort_button.pack(pady=10)

    reset_button = ttk.Button(root, text="Reset",
                              command=lambda: reset_visualizer(size_entry, array_entry, text_widget))
    reset_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
