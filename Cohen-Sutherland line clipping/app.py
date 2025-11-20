import customtkinter as ctk
from tkinter import messagebox


# ======================================================================================================================
INSIDE = 0  # 0000
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8     # 1000

def compute_code(x, y, x_min, y_min, x_max, y_max):
    code = INSIDE
    if x < x_min: code |= LEFT
    elif x > x_max: code |= RIGHT
    if y < y_min: code |= BOTTOM
    elif y > y_max: code |= TOP
    return code

def cohen_sutherland_clip(x1, y1, x2, y2, x_min, y_min, x_max, y_max):
    code1 = compute_code(x1, y1, x_min, y_min, x_max, y_max)
    code2 = compute_code(x2, y2, x_min, y_min, x_max, y_max)
    accept = False

    while True:
        if code1 == 0 and code2 == 0:  
            accept = True
            break
        elif (code1 & code2) != 0:     
            break
        else:
            x, y = 1.0, 1.0
            code_out = code1 if code1 != 0 else code2

            if code_out & TOP:
                x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                y = y_max
            elif code_out & BOTTOM:
                x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                y = y_min
            elif code_out & RIGHT:
                y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                x = x_max
            elif code_out & LEFT:
                y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                x = x_min

            if code_out == code1:
                x1, y1 = x, y
                code1 = compute_code(x1, y1, x_min, y_min, x_max, y_max)
            else:
                x2, y2 = x, y
                code2 = compute_code(x2, y2, x_min, y_min, x_max, y_max)

    if accept:
        return int(round(x1)), int(round(y1)), int(round(x2)), int(round(y2))
    else:
        return None



# ======================================================================================================================
def bresenham_line(x1, y1, x2, y2, canvas, color="black"):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        canvas.create_oval(x1, y1, x1+1, y1+1, fill=color, outline=color)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy



# ======================================================================================================================
def clip_line():
    try:
        x1 = int(entry_x1.get())
        y1 = int(entry_y1.get())
        x2 = int(entry_x2.get())
        y2 = int(entry_y2.get())
        x_min = int(entry_xmin.get())
        y_min = int(entry_ymin.get())
        x_max = int(entry_xmax.get())
        y_max = int(entry_ymax.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid integer values!")
        return

    canvas.delete("all")

    canvas.create_rectangle(x_min, y_min, x_max, y_max, outline="blue", width=2)

    bresenham_line(x1, y1, x2, y2, canvas, color="gray")

    clipped = cohen_sutherland_clip(x1, y1, x2, y2, x_min, y_min, x_max, y_max)
    if clipped:
        bresenham_line(*clipped, canvas, color="red")
    else:
        messagebox.showinfo("Clipping Result", "Line is completely outside the clipping window.")


# ======================================================================================================================
app = ctk.CTk()
app.title("Cohen Sutherland Line Clipping")
app.geometry("800x600")

frame = ctk.CTkFrame(app)
frame.pack(side="left", padx=20, pady=20)

ctk.CTkLabel(frame, text="Line Coordinates").grid(row=0, column=0, columnspan=2, pady=5)
entry_x1 = ctk.CTkEntry(frame, placeholder_text="x1"); entry_x1.grid(row=1, column=0, padx=5, pady=5)
entry_y1 = ctk.CTkEntry(frame, placeholder_text="y1"); entry_y1.grid(row=1, column=1, padx=5, pady=5)
entry_x2 = ctk.CTkEntry(frame, placeholder_text="x2"); entry_x2.grid(row=2, column=0, padx=5, pady=5)
entry_y2 = ctk.CTkEntry(frame, placeholder_text="y2"); entry_y2.grid(row=2, column=1, padx=5, pady=5)

ctk.CTkLabel(frame, text="Clipping Window").grid(row=3, column=0, columnspan=2, pady=5)
entry_xmin = ctk.CTkEntry(frame, placeholder_text="x_min"); entry_xmin.grid(row=4, column=0, padx=5, pady=5)
entry_ymin = ctk.CTkEntry(frame, placeholder_text="y_min"); entry_ymin.grid(row=4, column=1, padx=5, pady=5)
entry_xmax = ctk.CTkEntry(frame, placeholder_text="x_max"); entry_xmax.grid(row=5, column=0, padx=5, pady=5)
entry_ymax = ctk.CTkEntry(frame, placeholder_text="y_max"); entry_ymax.grid(row=5, column=1, padx=5, pady=5)

ctk.CTkButton(frame, text="Clip Line", command=clip_line).grid(row=6, column=0, columnspan=2, pady=10)

canvas = ctk.CTkCanvas(app, width=500, height=500, bg="white")
canvas.pack(side="right", padx=20, pady=20)

app.mainloop()