import random
import pandas
from tkinter import *
from tkinter import scrolledtext

# Declare Global / Multi-use Variables
timer_id = None  # Variable to store the timer ID
BACKGROUND_COLOR = "#B1DDC6"
correct_words = []
incorrect_words = []
correct_count = 0
incorrect_count = 0

# --------- Read Files ----------- #
with open("data\German_Words.csv", "r") as data_file:
    data = pandas.read_csv(data_file)
    print(data)
    # Turn data to list
    german_words = data["German"].to_list()
    english_words = data["English"].to_list()


# -------- Timer Apparatus --------- #
def start_timer(count):
    global picked_word_num, timer_id

    canvas.itemconfig(timer_text, text=f"{count}", fill=BACKGROUND_COLOR)
    if count > 0:
        timer_id = window.after(800, start_timer, count - 1)
    else:
        canvas.itemconfig(language_text, text="English", fill="white")
        canvas.itemconfig(flashcard, image=back_card)
        canvas.itemconfig(timer_text, text="0", fill="white")
        canvas.itemconfig(word_text, text=f"{english_words[picked_word_num]}", fill="white")
        # timer_id = None


#----------------------- Card Functionality --------------------------- #
def right_press():
    global picked_word_num, correct_words, correct_count
    correct_count += 1
    canvas.itemconfig(count_text, text=f"Correct: {correct_count}\nIncorrect: {incorrect_count}", )
    correct_words.append(f"{german_words[picked_word_num]}: {english_words[picked_word_num]}")
    reset_card()

def wrong_press():
    global incorrect_count, incorrect_words
    incorrect_count += 1
    canvas.itemconfig(count_text, text=f"Correct: {correct_count}\nIncorrect: {incorrect_count}", )
    incorrect_words.append(f"{german_words[picked_word_num]}: {english_words[picked_word_num]}")
    reset_card()

#----------------------- Card Reset Function --------------------------- #
def reset_card():
    global picked_word_num, timer_id
    if timer_id:
        window.after_cancel(timer_id)
        timer_id = None
    # else:
    del german_words[picked_word_num]
    del english_words[picked_word_num]
    # Ensure there are still words left to pick
    if len(german_words) > 0:
        picked_word_num = random.randint(0, len(german_words) - 1)
        # Graphic Items
        canvas.itemconfig(language_text, text="German", fill="black")
        canvas.itemconfig(flashcard, image=front_card)
        canvas.itemconfig(timer_text, text="3", fill="black")  # Timer reset
        canvas.itemconfig(word_text, text=f"{german_words[picked_word_num]}", fill="black")
        start_timer(3)
    else:
        canvas.itemconfig(word_text, text="No more\nwords left!")
        stop_cards()

# --------- Start & Pause Flashcards ---------- #
def start_cards():
    canvas.itemconfig(language_text, text="German", fill="black")
    canvas.itemconfig(flashcard, image=front_card)
    canvas.itemconfig(timer_text, text="0", fill="black")
    canvas.itemconfig(word_text, text=f"{german_words[picked_word_num]}", fill="Black")
    start_timer(3)

def stop_cards():
    print(f"You got {correct_count}/{incorrect_count + correct_count} words right")
    with open("Session_Report.txt", "w") as f:
        f.write("You knew the following terms: (German Term: English Term)\n")
        for i in correct_words:
            f.write(f"\n{i}")
        f.write("\n \nYou didn't know the following terms: (German Term: English Term)\n")
        for j in incorrect_words:
            f.write(f"\n{j}")
    with open("Session_Report.txt", "r") as r:
        session_report = r.read()
    top = Toplevel(window)  ##
    top.title("Session Report")
    text_area = scrolledtext.ScrolledText(top, wrap=WORD, width=50, height=15)
    text_area.insert(END, f"{session_report}")  # Example long text
    text_area.pack(expand=True, fill='both')

# ----------------------------- UI Structure -------------------------------- #

window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

front_card = PhotoImage(file="images/card_front.png")
back_card = PhotoImage(file="images/card_back.png")
right_mark = PhotoImage(file="images/right.png")
wrong_mark = PhotoImage(file="images/wrong.png")
end_session = PhotoImage(file="images/END SESSION.png")
start_session = PhotoImage(file="images/START SESSION.png")

canvas = Canvas(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
flashcard = canvas.create_image(400, 263, image=front_card)
language_text = canvas.create_text(400, 120, text="German", font=("Courier", 30, "italic"), tags="language")
timer_text = canvas.create_text(720, 450, text=f"", font=("Arial", 40, "bold"))

picked_word_num = random.randint(0, len(german_words))

count_text = canvas.create_text(120, 450, text=f"Correct: {correct_count}\nIncorrect: {incorrect_count}",
                                font=("Courier", 20, "bold"))

word_text = canvas.create_text(400, 270, text=f"", font=("Courier", 70, "bold"), tags="display_word")
canvas.grid(column=0, row=1, columnspan=2)

right_button = Button(image=right_mark, command=right_press, borderwidth=0, highlightthickness=0, bg=BACKGROUND_COLOR)
right_button.config(height=100, width=100)
right_button.grid(column=0, row=2)

wrong_button = Button(image=wrong_mark, command=wrong_press, borderwidth=0, highlightthickness=0)
wrong_button.config(height=100, width=100)
wrong_button.grid(column=1, row=2)

start_session_button = Button(image=start_session, command=start_cards, borderwidth=0, bg=BACKGROUND_COLOR)
start_session_button.config(height=100, width=100)
start_session_button.grid(column=0, row=0)

end_session_button = Button(image=end_session, command=stop_cards, borderwidth=0, highlightthickness=0,
                            bg=BACKGROUND_COLOR)
end_session_button.config(height=100, width=100)
end_session_button.grid(column=1, row=0)

window.mainloop()