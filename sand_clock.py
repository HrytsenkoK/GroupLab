import tkinter as tk             
from tkinter import ttk             
import time                         

duration = 10                       
remaining = duration                
running = False                     
last_update = time.time()          

def start_timer():
    global duration, remaining, running
    try:
        duration = int(duration_entry.get())  
        if duration <= 0:                     
            raise ValueError
        remaining = duration                  
        running = True                        
        flip_btn.config(state=tk.DISABLED)    
    except ValueError:
        duration_entry.delete(0, tk.END)      
        duration_entry.insert(0, str(duration))  

def flip_clock():
    global remaining, running
    remaining = duration                     
    running = True                           
    flip_btn.config(state=tk.DISABLED)       

def draw_hourglass():
    canvas.delete("all")  

    canvas.create_polygon(100, 100, 300, 100, 200, 250, fill="", outline="black", width=2)
    canvas.create_polygon(100, 400, 300, 400, 200, 250, fill="", outline="black", width=2)

    progress = (duration - remaining) / duration
    progress = max(0.0, min(1.0, progress))  

    top_sand_height = 150 * (1 - progress)     
    side_sand_width = (progress * 2) / 3       

    if top_sand_height > 0:
        canvas.create_polygon(
            100 + (150 * side_sand_width), 100 - top_sand_height + 150,  
            300 - (150 * side_sand_width), 100 - top_sand_height + 150,  
            200, 100 + 150,                                               
            fill="goldenrod", outline=""                                  
        )

    bottom_sand_height = 150 * progress
    if bottom_sand_height > 0:
        canvas.create_polygon(
            100, 400,                       
            300, 400,                       
            200, 400 - bottom_sand_height,  
            fill="goldenrod", outline=""
        )

    
    if running and remaining > 0:
        canvas.create_line(200, 250, 200, 400, fill="goldenrod", width=2)

    canvas.create_text(200, 470, text=f"{int(remaining)} сек", font=("Arial", 20))

def animate():
    global remaining, running, last_update
    now = time.time()                  
    if running:
        delta = now - last_update       
        remaining -= delta              
        if remaining <= 0:              
            remaining = 0
            running = False
            flip_btn.config(state=tk.NORMAL)  
    last_update = now
    draw_hourglass()                   
    root.after(50, animate)            

root = tk.Tk()                         
root.title("Піщаний годинник")         
root.geometry("400x600")               
root.resizable(False, False)           

canvas = tk.Canvas(root, width=400, height=500, bg="white")  
canvas.pack()

controls = ttk.Frame(root)             
controls.pack(pady=10)

ttk.Label(controls, text="Тривалість (сек):").grid(row=0, column=0, padx=5)

duration_entry = ttk.Entry(controls, width=5)
duration_entry.insert(0, str(duration))  
duration_entry.grid(row=0, column=1)


start_btn = ttk.Button(controls, text="Старт", command=start_timer)
start_btn.grid(row=0, column=2, padx=5)


flip_btn = ttk.Button(controls, text="Перевернути", command=flip_clock, state=tk.DISABLED)
flip_btn.grid(row=0, column=3, padx=5)


animate()             
root.mainloop()
