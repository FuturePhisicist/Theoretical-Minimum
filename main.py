import random
import pickle
import os

import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def load_data(filename):
    with open(filename, 'r') as file:
        data = file.readlines()
    return {int(line.split('.')[0]): line[line.find('.') + 2:-1] for line in data}

def save_known_tasks(known_tasks):
    with open('known_tasks.pkl', 'wb') as f:
        pickle.dump(known_tasks, f)

def load_known_tasks():
    try:
        with open('known_tasks.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return set()

def display_current_task():
    global current_task_number, tasks
    try:
        task_text = tasks[current_task_number]

        figure.clear()
        text = figure.text(0.5, 0.5, f"${task_text}$", fontsize=12, ha='center', va='center')
        canvas.draw()
    except NameError:
        display_next_task()

def display_next_task():
    global current_task_number, tasks, answers
    if known_tasks:
        remaining_tasks = set(tasks.keys()) - known_tasks
    else:
        remaining_tasks = set(tasks.keys())

    if not remaining_tasks:
        lbl_question.config(text="No more tasks or all tasks are known.")
        return

    current_task_number = random.choice(list(remaining_tasks))
    task_text = tasks[current_task_number]

    figure.clear()
    text = figure.text(0.5, 0.5, f"${task_text}$", fontsize=12, ha='center', va='center')
    canvas.draw()

def show_answer():
    try:
        answer_text = answers[current_task_number]
        figure.clear()
        text = figure.text(0.5, 0.5, f"${answer_text}$", fontsize=12, ha='center', va='center')
        canvas.draw()
    except NameError:
        display_next_task()

def known():
    try:
        known_tasks.add(current_task_number)
    except NameError:
        pass

    save_known_tasks(known_tasks)
    display_next_task()

def not_known():
    display_next_task()

def delete_known_tasks():
    try:
        os.remove('known_tasks.pkl')
        global known_tasks
        known_tasks = set()
        lbl_question.config(text="Known tasks reset. Press 'Show Current Task' to continue.")
    except FileNotFoundError:
        lbl_question.config(text="No known tasks file to delete.")

# plt.rcParams['text.usetex'] = True
# plt.rcParams['text.latex.preamble'] = r'\usepackage[T2A]{fontenc}\usepackage[utf8]{inputenc}\usepackage[russian]{babel}\usepackage{amsmath}\usepackage[utf8]{inputenc}'

tasks = load_data('tasks.txt')
# print(tasks)
answers = load_data('answers.txt')
known_tasks = load_known_tasks()

root = tk.Tk()
root.title("Learning Tasks")

btn_frame = tk.Frame(root)
btn_frame.pack(fill=tk.BOTH, expand=True)

btn_current = tk.Button(btn_frame, text="Show Current Task", command=display_current_task)
btn_current.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

btn_answer = tk.Button(btn_frame, text="Show Answer", command=show_answer)
btn_answer.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

btn_known = tk.Button(btn_frame, text="I Know That", command=known)
btn_known.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

btn_unknown = tk.Button(btn_frame, text="I Don't Know It", command=not_known)
btn_unknown.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

btn_delete = tk.Button(btn_frame, text="Delete Known Tasks", command=delete_known_tasks)
btn_delete.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

lbl_question = tk.Label(root, text="Press 'Show Current Task' to start.", font=('Arial', 12))
lbl_question.pack(pady=20)

figure = plt.Figure(figsize=(60, 6))
canvas = FigureCanvasTkAgg(figure, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

root.mainloop()
