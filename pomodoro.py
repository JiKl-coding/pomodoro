import tkinter as tk
import pygame
from tkinter import messagebox


def load_settings():
    with open("settings.txt") as settings:
        time_settings = settings.readlines()
        return time_settings


time_set = load_settings()

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#5F8D4E"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
MILLI_SECONDS = 1000
WORK_MIN = int(time_set[0])
SHORT_BREAK_MIN = int(time_set[1])
LONG_BREAK_MIN = int(time_set[2])
CHECKMARK_SIGN = "✔"
reps = 0
timer = None
is_running = False

pygame.mixer.init()
pygame.display.set_caption("")
bell_sound = pygame.mixer.Sound("bell sound.wav")


def open_settings():
    # save settings function
    def save_settings():

        work_time = work_time_entry.get()
        short_break = short_break_entry.get()
        long_break = long_break_entry.get()

        if work_time.isdigit() and short_break.isdigit() and long_break.isdigit():
            global WORK_MIN
            global SHORT_BREAK_MIN
            global LONG_BREAK_MIN
            WORK_MIN = int(work_time)
            SHORT_BREAK_MIN = int(short_break)
            LONG_BREAK_MIN = int(long_break)

            with open("settings.txt", "w") as settings:
                settings.write(f"{work_time}\n")
                settings.write(f"{short_break}\n")
                settings.write(f"{long_break}\n")
        else:
            messagebox.showerror(title="Oops!", message="Input valid numbers!")

        settings_window.destroy()

    # settings window
    settings_window = tk.Toplevel()
    settings_window.title("Pomodoro Settings")
    settings_window.config(padx=20, pady=20, bg=YELLOW)

    work_time_label = tk.Label(master=settings_window, pady=10, text="Work time: ", font=(FONT_NAME, 10, "bold"),
                               bg=YELLOW)
    work_time_label.grid(row=0, column=0)

    short_break_label = tk.Label(master=settings_window, pady=10, text="Short break time: ",
                                 font=(FONT_NAME, 10, "bold"),
                                 bg=YELLOW)
    short_break_label.grid(row=1, column=0)

    long_break_label = tk.Label(master=settings_window, pady=10, text="Long break time: ", font=(FONT_NAME, 10, "bold"),
                                bg=YELLOW)
    long_break_label.grid(row=2, column=0)

    work_time_entry = tk.Entry(master=settings_window, bg="white", width=15)
    work_time_entry.grid(row=0, column=1)

    short_break_entry = tk.Entry(master=settings_window, bg="white", width=15)
    short_break_entry.grid(row=1, column=1)

    long_break_entry = tk.Entry(master=settings_window, bg="white", width=15)
    long_break_entry.grid(row=2, column=1)

    save_button = tk.Button(master=settings_window, text="Save Settings", bg=YELLOW, borderwidth=0,
                            font=(FONT_NAME, 12, "bold"), fg=RED, command=save_settings)
    save_button.grid(row=3, column=0, columnspan=1)

    current_settings = load_settings()

    work_time_entry.insert(0, str(int(current_settings[0])))
    short_break_entry.insert(0, str(int(current_settings[1])))
    long_break_entry.insert(0, str(int(current_settings[2])))

    settings_window.mainloop()


def ring_bell():
    bell_sound.play()


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global is_running
    is_running = False
    global reps
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    main_label.config(text="Timer", fg=GREEN)
    checkmark_label.config(text="")
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global is_running
    if not is_running:
        is_running = True
        global reps
        reps += 1
        work_sec = WORK_MIN * 60
        shot_break_sec = SHORT_BREAK_MIN * 60
        long_break_sec = LONG_BREAK_MIN * 60

        if reps % 8 == 0:
            main_label.config(text="Break", fg=RED)
            count_down(long_break_sec)
        elif reps % 2 == 0:
            main_label.config(text="Break", fg=PINK)
            count_down(shot_break_sec)
        else:
            main_label.config(text="Work", fg=GREEN)
            count_down(work_sec)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = count // 60
    count_sec = count % 60
    if count_min < 10:
        count_min = f"0{count_min}"
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    if count > 0:
        global timer
        timer = window.after(MILLI_SECONDS, count_down, count - 1)
    else:
        global is_running
        is_running = False
        ring_bell()
        window.attributes('-topmost', 1)
        start_timer()
        # add slice for each session done
        marks = ""
        work_sessions = reps // 2
        for _ in range(work_sessions):
            marks += CHECKMARK_SIGN
        checkmark_label.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Pomodoro by AkriY")
window.config(padx=100, pady=50, bg=YELLOW)
window.minsize(width=400, height=350)
window.iconbitmap("tomato_icon.ico")

# based on img size
canvas = tk.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
# loading the img using PhotoImage
tomato_img = tk.PhotoImage(file="tomato.png")
# x and y values => in the middle of its size -> if picture is not centred perfectly, you change the x/y value like
# in this case. I used x = 102. Later I set 'highlightthickness' to 0 and changed this back to 100
canvas.create_image(100, 112, image=tomato_img)
canvas.grid(row=1, column=1)
timer_text = canvas.create_text(100, 140, text="00:00", fill="white", font=(FONT_NAME, 25, "bold"))

main_label = tk.Label(bg=YELLOW, fg=GREEN, text="Timer", font=(FONT_NAME, 35, "bold"))
main_label.grid(row=0, column=1)

start_button = tk.Button(text="Start", width=5, height=2, font=(FONT_NAME, 12, "bold"),
                         bg=YELLOW, borderwidth=0, command=start_timer)
start_button.grid(row=2, column=0)

reset_button = tk.Button(text="Reset", width=5, height=2, font=(FONT_NAME, 12, "bold"),
                         bg=YELLOW, borderwidth=0, command=reset_timer)
reset_button.grid(row=2, column=2)

settings_button = tk.Button(text="Settings", width=10, height=2, font=(FONT_NAME, 12, "bold"),
                            bg=YELLOW, borderwidth=0, command=open_settings)
settings_button.grid(row=4, column=1)

checkmark_label = tk.Label(bg=YELLOW, fg=RED, text="", font=(FONT_NAME, 15, "bold"))
checkmark_label.grid(row=3, column=1)

window.mainloop()
