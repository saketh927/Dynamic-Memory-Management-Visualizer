# 📂 Dynamic Memory Management Visualizer

# Description:
# This project implements a tool to simulate and visualize memory management techniques like Paging, Segmentation, and Virtual Memory.
# It handles user-defined inputs for memory allocation, page faults, and replacement algorithms (FIFO, LRU).
# Built using Python's standard libraries, matplotlib for visualization, and Tkinter for the user interface.

import matplotlib.pyplot as plt
from typing import List, Dict, Tuple
import tkinter as tk
from tkinter import messagebox
import time


class Page:
    def __init__(self, page_number: int):
        self.page_number = page_number


class Segment:
    def __init__(self, segment_id: int, size: int):
        self.segment_id = segment_id
        self.size = size
        self.base_address = None


def fifo_page_replacement(pages: List[int], frame_count: int) -> Tuple[List[List[int]], int]:
    memory = []
    page_faults = 0
    history = []

    for page in pages:
        if page not in memory:
            if len(memory) < frame_count:
                memory.append(page)
            else:
                memory.pop(0)
                memory.append(page)
            page_faults += 1
        history.append(memory.copy())

    return history, page_faults


def lru_page_replacement(pages: List[int], frame_count: int) -> Tuple[List[List[int]], int]:
    memory = []
    page_faults = 0
    history = []
    recent_usage = []

    for page in pages:
        if page not in memory:
            if len(memory) < frame_count:
                memory.append(page)
                recent_usage.append(0)
            else:
                lru_index = recent_usage.index(max(recent_usage))
                memory[lru_index] = page
                recent_usage[lru_index] = 0
            page_faults += 1
        else:
            recent_usage[memory.index(page)] = 0

        recent_usage = [x + 1 for x in recent_usage]
        history.append(memory.copy())

    return history, page_faults


def segmentation_allocation(segments: List[Segment], memory_size: int) -> Dict[int, int]:
    allocation = {}
    current_address = 0

    for segment in segments:
        if current_address + segment.size <= memory_size:
            segment.base_address = current_address
            allocation[segment.segment_id] = segment.base_address
            current_address += segment.size
        else:
            allocation[segment.segment_id] = -1

    return allocation


def visualize_memory(history: List[List[int]], algorithm_name: str):
    fig, ax = plt.subplots(figsize=(10, 5))
    for i, state in enumerate(history):
        for j, frame in enumerate(state):
            ax.text(i, j, str(frame), va='center', ha='center', fontsize=10,
                    bbox=dict(facecolor='lightblue', edgecolor='black'))

    ax.set_xticks(range(len(history)))
    ax.set_yticks(range(max(len(state) for state in history)))
    ax.set_xlabel('Time Steps')
    ax.set_ylabel('Frames')
    plt.title(f'Memory Allocation Visualization ({algorithm_name})')
    plt.show()


def run_simulation():
    try:
        pages = list(map(int, entry_pages.get().split(',')))
        frame_count = int(entry_frames.get())
        fifo_history, fifo_faults = fifo_page_replacement(pages, frame_count)
        visualize_memory(fifo_history, 'FIFO')
        messagebox.showinfo('FIFO Page Faults', f'Total Page Faults (FIFO): {fifo_faults}')

        lru_history, lru_faults = lru_page_replacement(pages, frame_count)
        visualize_memory(lru_history, 'LRU')
        messagebox.showinfo('LRU Page Faults', f'Total Page Faults (LRU): {lru_faults}')
    except Exception as e:
        messagebox.showerror('Error', f'Invalid input: {e}')


def run_segmentation():
    try:
        memory_size = int(entry_memory_size.get())
        segments = [Segment(i, int(size)) for i, size in enumerate(entry_segments.get().split(','))]
        allocation = segmentation_allocation(segments, memory_size)
        messagebox.showinfo('Segmentation Allocation', f'Segment Allocation: {allocation}')
    except Exception as e:
        messagebox.showerror('Error', f'Invalid input: {e}')


root = tk.Tk()
root.title('Dynamic Memory Management Visualizer')

label_pages = tk.Label(root, text='Enter Pages (comma-separated):')
label_pages.grid(row=0, column=0)

entry_pages = tk.Entry(root, width=30)
entry_pages.grid(row=0, column=1)

label_frames = tk.Label(root, text='Enter Frame Count:')
label_frames.grid(row=1, column=0)

entry_frames = tk.Entry(root, width=10)
entry_frames.grid(row=1, column=1)

label_memory_size = tk.Label(root, text='Enter Memory Size (for Segmentation):')
label_memory_size.grid(row=2, column=0)

entry_memory_size = tk.Entry(root, width=10)
entry_memory_size.grid(row=2, column=1)

label_segments = tk.Label(root, text='Enter Segment Sizes (comma-separated):')
label_segments.grid(row=3, column=0)

entry_segments = tk.Entry(root, width=30)
entry_segments.grid(row=3, column=1)

btn_fifo_lru = tk.Button(root, text='Run FIFO & LRU', command=run_simulation)
btn_fifo_lru.grid(row=4, columnspan=2)

btn_segmentation = tk.Button(root, text='Run Segmentation', command=run_segmentation)
btn_segmentation.grid(row=5, columnspan=2)

root.mainloop()
