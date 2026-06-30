import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

logging_enabled = False
key_count = 0
log_data = []


def start_logging():
    global logging_enabled
    logging_enabled = True
    status_label.config(text="Status : Logging", fg="lightgreen")


def stop_logging():
    global logging_enabled
    logging_enabled = False
    status_label.config(text="Status : Stopped", fg="red")


def key_pressed(event):
    global key_count

    if not logging_enabled:
        return

    key = event.keysym

    if key == "space":
        key = "SPACE"
    elif key == "Return":
        key = "ENTER"
    elif key == "BackSpace":
        key = "BACKSPACE"
    elif len(event.char) == 1 and event.char.isprintable():
        key = event.char

    time = datetime.now().strftime("%H:%M:%S")

    line = f"{time}  ->  {key}\n"

    log_data.append(line)

    key_count += 1

    counter_label.config(text=f"Total Keys : {key_count}")

    log_box.config(state="normal")
    log_box.insert(tk.END, line)
    log_box.see(tk.END)
    log_box.config(state="disabled")


def save_log():
    if len(log_data) == 0:
        messagebox.showwarning("Warning", "No log available!")
        return

    file = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text File", "*.txt")]
    )

    if file:
        with open(file, "w") as f:
            f.writelines(log_data)

        messagebox.showinfo("Success", "Log saved successfully.")


def clear_log():
    global key_count

    log_data.clear()
    key_count = 0

    counter_label.config(text="Total Keys : 0")

    log_box.config(state="normal")
    log_box.delete("1.0", tk.END)
    log_box.config(state="disabled")


# ---------------- GUI ----------------

root = tk.Tk()
root.title("Keyboard Event Logger")
root.geometry("750x600")
root.configure(bg="#1e1e1e")

title = tk.Label(
    root,
    text="Keyboard Event Logger",
    font=("Arial", 20, "bold"),
    bg="#1e1e1e",
    fg="white"
)
title.pack(pady=15)

instruction = tk.Label(
    root,
    text="Type inside the box below.\nOnly keys typed in this application are recorded.",
    bg="#1e1e1e",
    fg="lightgray",
    font=("Arial", 11)
)
instruction.pack()

typing_box = tk.Text(
    root,
    height=8,
    width=70,
    font=("Consolas", 12)
)
typing_box.pack(pady=10)

typing_box.bind("<Key>", key_pressed)

counter_label = tk.Label(
    root,
    text="Total Keys : 0",
    bg="#1e1e1e",
    fg="cyan",
    font=("Arial", 11, "bold")
)
counter_label.pack()

status_label = tk.Label(
    root,
    text="Status : Stopped",
    bg="#1e1e1e",
    fg="red",
    font=("Arial", 11, "bold")
)
status_label.pack(pady=5)

frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(pady=10)

tk.Button(
    frame,
    text="Start Logging",
    bg="green",
    fg="white",
    width=15,
    command=start_logging
).grid(row=0, column=0, padx=5)

tk.Button(
    frame,
    text="Stop Logging",
    bg="red",
    fg="white",
    width=15,
    command=stop_logging
).grid(row=0, column=1, padx=5)

tk.Button(
    frame,
    text="Save Log",
    bg="#2196F3",
    fg="white",
    width=15,
    command=save_log
).grid(row=0, column=2, padx=5)

tk.Button(
    frame,
    text="Clear Log",
    bg="#FF9800",
    fg="white",
    width=15,
    command=clear_log
).grid(row=0, column=3, padx=5)

tk.Button(
    root,
    text="Exit",
    width=20,
    bg="gray",
    fg="white",
    command=root.destroy
).pack(pady=10)

log_title = tk.Label(
    root,
    text="Recorded Keys",
    bg="#1e1e1e",
    fg="white",
    font=("Arial", 13, "bold")
)
log_title.pack()

log_box = tk.Text(
    root,
    height=12,
    width=80,
    state="disabled",
    bg="#2b2b2b",
    fg="white",
    font=("Consolas", 10)
)
log_box.pack(pady=10)

root.mainloop()