import tkinter as tk
from tkinter import messagebox
import random
import json
from datetime import datetime

def main_screen():
    global main_win
    main_win = tk.Tk()
    main_win.title("GAMBLING LES GOOOOO")

    window_width = 1000
    window_height = 750

    screen_width = main_win.winfo_screenwidth()
    screen_height = main_win.winfo_screenheight()

    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    main_win.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    main_win.configure(bg="#1500f7")
    
    main_win.secret_number = random.randint(1, 100)
    main_win.attempts = 0
    main_win.label = tk.Label(main_win, text="1-ээс 100-ийн хооронд тоо таагаарай.", bg="#f0f0f0", font=("Arial", 18))
    main_win.label.pack(pady=10)
        
    main_win.entry = tk.Entry(main_win, font=("Arial", 20), width=20)
    main_win.entry.pack(pady=5)
    main_win.entry.focus_set()
        
    main_win.entry.bind('<Return>', lambda event: check_guess() )
        
    main_win.button = tk.Button(main_win, text="Таах", command = check_guess, bg="#4CAF50", fg="white", font=("Arial", 18, "bold"))
    main_win.button.pack(pady=10)
        
    main_win.result_label = tk.Label(main_win, text="Гарах бол 'q' эсвэл 'quit' гэж бичээрэй", bg="#f0f0f0", fg="gray", font=("Arial",18))
    main_win.result_label.pack(pady=5)
        
    main_win.stats_label = tk.Label(main_win, text="Оролдлого: 0", bg="#f0f0f0", font=("Arial,18"))
    main_win.stats_label.pack(pady=5)
    
    players = load_leader_board()

    title = tk.Label(main_win, text="Leaderboard", font=("Arial", 20))
    title.pack()

    for i, player in enumerate(players):
        text = f"{i+1}. {player['attempt']} attempts - {player['time']}"
        label = tk.Label(main_win, text=text, font=("Arial", 14))
        label.pack()



    main_win.mainloop()

def check_guess():
    guess_input = main_win.entry.get().lower().strip()
    if guess_input == "":
        return
    if guess_input == "q" or guess_input == "quit":
        main_win.destroy()
        return
    try:
            guess = int(guess_input)
            if guess < 1 or guess > 100:
                raise SyntaxError
    except ValueError:
        messagebox.showwarning("Алдаа", "Зөвхөн тоо эсвэл 'q' эсвэд 'quit' гэж оруулна уу.")
        main_win.entry.delete(0, tk.END)
        return
    except SyntaxError:
        messagebox.showwarning("Алдаа", f"{guess} энэхүү тоо нь 1 - 100 гийн хооронд байрлах тоо биш байна.")
        main_win.entry.delete(0, tk.END)
        return
    
    main_win.attempts += 1
    main_win.stats_label.config(text=f"Оролдлого: {main_win.attempts}")
        
    if guess < main_win.secret_number:
        main_win.result_label.config(text="Тоо бага байна.", fg="red")
    elif guess > main_win.secret_number:
        main_win.result_label.config(text="Тоо их байна.", fg="red")
    else:
        main_win.config(bg="green")
        main_win.label.config(bg="green", fg="white")
        main_win.result_label.config(text="Зөв таалаа!", fg="white", bg="green")
        main_win.stats_label.config(bg="green", fg="white")
        add_score(main_win.attempts)
        messagebox.showinfo("Баяр хүргэе!", f"Та {main_win.attempts} оролдлогоор таалаа!")
        reset_game()
            
    main_win.entry.delete(0, tk.END)


def reset_game():
    global main_win
    main_win.secret_number = random.randint(1, 100)
    main_win.attempts = 0
    main_win.config(bg="#1500f7") 
    main_win.label.config(bg="#f0f0f0", fg="black")
    main_win.result_label.config(text="Шинэ тоо үүслээ!", fg="blue", bg="#f0f0f0")
    main_win.stats_label.config(bg="#f0f0f0", fg="black", text="Оролдлого: 0")    
    main_win.entry.delete(0, tk.END)
def load_leader_board():
    try:
        with open("leaderboard.json", "r") as file:
            data = json.load(file)
            return data["leaderboard"]
    except:
        return []

def sort_leaderboard(players):
    return sorted(players, key=lambda x: x["attempt"])

def add_score(attempt):
    try:
        with open("leaderboard.json", "r") as file:
            data = json.load(file)
    except:
        data = {"leaderboard": []}

    now = datetime.now()
    time_string = now.strftime("%Y-%m-%d %H:%M:%S")

    data["leaderboard"].append({
        "attempt": attempt,
        "time": time_string
    })

    with open("leaderboard.json", "w") as file:
        json.dump(data, file, indent=4)
main_screen()