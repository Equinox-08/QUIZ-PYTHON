# quiz.py
# Solar System Quiz Application using Python Tkinter

import os
import random
import tkinter as tk
from tkinter import messagebox

# 10 SOLAR SYSTEM QUESTIONS (no question numbers inside the question text)
QUESTIONS = [
    {
        "question": "Which planet in our Solar System is closest to the Sun?",
        "choices": ["A. Venus", "B. Mercury", "C. Mars", "D. Earth"],
        "answer": "B"
    },
    {
        "question": "Which planet has a runaway greenhouse effect making it the hottest planet?",
        "choices": ["A. Mercury", "B. Jupiter", "C. Venus", "D. Saturn"],
        "answer": "C"
    },
    {
        "question": "What is the name of the giant storm on Jupiter that has raged for centuries?",
        "choices": ["A. Great Dark Spot", "B. Polar Hexagon", "C. Great Red Spot", "D. Solar Vortex"],
        "answer": "C"
    },
    {
        "question": "Which planet is famous for its prominent, bright ring system made mostly of ice and rock?",
        "choices": ["A. Saturn", "B. Uranus", "C. Neptune", "D. Mars"],
        "answer": "A"
    },
    {
        "question": "Which planet rotates on its side with an axial tilt of about 98 degrees?",
        "choices": ["A. Neptune", "B. Venus", "C. Uranus", "D. Mercury"],
        "answer": "C"
    },
    {
        "question": "Which planet is known as the Red Planet due to iron oxide on its surface?",
        "choices": ["A. Mars", "B. Jupiter", "C. Saturn", "D. Venus"],
        "answer": "A"
    },
    {
        "question": "Where is the main asteroid belt located in our Solar System?",
        "choices": [
            "A. Between Earth and Mars",
            "B. Between Mars and Jupiter",
            "C. Between Saturn and Uranus",
            "D. Beyond Neptune"
        ],
        "answer": "B"
    },
    {
        "question": "Which is the largest moon of Saturn and the only moon known to have a dense atmosphere?",
        "choices": ["A. Europa", "B. Io", "C. Ganymede", "D. Titan"],
        "answer": "D"
    },
    {
        "question": "Which outer planet is the farthest major planet from the Sun and experiences supersonic winds?",
        "choices": ["A. Uranus", "B. Pluto", "C. Neptune", "D. Saturn"],
        "answer": "C"
    },
    {
        "question": "Which region beyond Neptune is home to icy bodies and dwarf planets such as Pluto and Eris?",
        "choices": ["A. Oort Cloud", "B. Kuiper Belt", "C. Asteroid Belt", "D. Van Allen Belt"],
        "answer": "B"
    }
]

# APPLICATION SETTINGS & CUSTOM PALETTE
TIME_LIMIT = 15
HIGH_SCORE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "high_score.txt"
)

BG_SPACE = "#0B1026"
CARD_DARK = "#151D3B"
ACCENT_GOLD = "#F4C95D"
ACCENT_CYAN = "#5CE1E6"
TEXT_LIGHT = "#F2F5FF"
TEXT_MUTED = "#A7B2D6"
CORRECT_GREEN = "#38D399"
WRONG_RED = "#FF5C77"

FONT_TITLE = ("Georgia", 26, "bold")
FONT_HEADING = ("Segoe UI", 16, "bold")
FONT_BODY = ("Segoe UI", 13)
FONT_BOLD = ("Segoe UI", 12, "bold")

# MAIN WINDOW & LAYOUT CONTAINER
root = tk.Tk()
root.title("Solar System Explorer Quiz")
root.geometry("740x660")
root.configure(bg=BG_SPACE)
root.resizable(False, False)

main_frame = tk.Frame(root, bg=BG_SPACE)
main_frame.pack(fill="both", expand=True, padx=32, pady=24)

# QUIZ STATE VARIABLES
quiz_questions = []
current_question = 0
score = 0
time_left = TIME_LIMIT
wrong_answers = []
timer_job = None
answered = False
selected_answer = tk.StringVar()

# DYNAMIC WIDGET REFERENCES
timer_label = None
feedback_label = None
submit_button = None
next_button = None
choice_buttons = []


# HIGH SCORE FILE HANDLING
def get_high_score():
    """Read the saved high score from the text file, or return 0 if missing/invalid."""
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r", encoding="utf-8") as file:
                return int(file.read().strip())
        except ValueError:
            return 0
    return 0


def save_high_score(new_score):
    """Save new_score to high_score.txt if it beats the current record."""
    if new_score > get_high_score():
        with open(HIGH_SCORE_FILE, "w", encoding="utf-8") as file:
            file.write(str(new_score))
        return True
    return False


# HELPER FUNCTIONS
def clear_screen():
    """Remove all widgets inside main_frame before rendering a new screen."""
    for widget in main_frame.winfo_children():
        widget.destroy()


def get_choice_text(question, letter):
    """Return the full choice string matching a single option letter."""
    for choice in question["choices"]:
        if choice.startswith(letter + "."):
            return choice
    return "No answer"


# SCREENS
def show_start_screen():
    """Display the welcome screen, quiz rules, high score, and start button."""
    clear_screen()

    card = tk.Frame(main_frame, bg=CARD_DARK, padx=32, pady=36,
                    highlightbackground=ACCENT_CYAN, highlightthickness=1)
    card.pack(fill="both", expand=True)

    tk.Label(card, text="SOLAR SYSTEM EXPEDITION",
             font=FONT_TITLE, bg=CARD_DARK, fg=ACCENT_GOLD).pack(pady=(20, 8))

    tk.Label(card, text="Test your knowledge of planets, moons, belts, and cosmic phenomena.",
             font=FONT_BODY, bg=CARD_DARK, fg=TEXT_MUTED).pack(pady=(0, 20))

    tk.Label(card,
             text=f"{len(QUESTIONS)} Questions   •   {TIME_LIMIT} Seconds Each   •   1 Point Per Correct Answer",
             font=FONT_BOLD, bg=CARD_DARK, fg=ACCENT_CYAN).pack(pady=8)

    tk.Label(card,
             text=f"All-Time High Score: {get_high_score()} / {len(QUESTIONS)}",
             font=FONT_HEADING, bg=CARD_DARK, fg=TEXT_LIGHT).pack(pady=(18, 28))

    tk.Button(card, text="Launch Quiz", font=FONT_HEADING,
              bg=ACCENT_GOLD, fg=BG_SPACE, activebackground=ACCENT_CYAN,
              activeforeground=BG_SPACE, relief="flat", padx=28, pady=10,
              cursor="hand2", command=start_quiz).pack()


def start_quiz():
    """Reset quiz state, shuffle all 10 questions randomly, and show question 1."""
    global quiz_questions, current_question, score, wrong_answers
    quiz_questions = random.sample(QUESTIONS, len(QUESTIONS))
    current_question = 0
    score = 0
    wrong_answers = []
    show_question()


def show_question():
    """Render the current question, choices, progress/score bar, and start timer."""
    global time_left, answered, timer_label, feedback_label
    global submit_button, next_button, choice_buttons

    clear_screen()
    answered = False
    selected_answer.set("")
    time_left = TIME_LIMIT
    question = quiz_questions[current_question]

    # Top bar: question progress & countdown timer
    header = tk.Frame(main_frame, bg=BG_SPACE)
    header.pack(fill="x", pady=(0, 6))

    tk.Label(header,
             text=f"Question {current_question + 1} of {len(quiz_questions)}",
             font=FONT_BOLD, bg=BG_SPACE, fg=ACCENT_CYAN).pack(side="left")

    timer_label = tk.Label(header, text="", font=FONT_BOLD,
                           bg=BG_SPACE, fg=TEXT_LIGHT)
    timer_label.pack(side="right")

    tk.Label(main_frame, text=f"Current Score: {score}",
             font=FONT_BODY, bg=BG_SPACE, fg=TEXT_MUTED).pack(anchor="w", pady=(0, 14))

    # Question card
    q_card = tk.Frame(main_frame, bg=CARD_DARK, padx=24, pady=22,
                      highlightbackground="#283566", highlightthickness=1)
    q_card.pack(fill="x")

    tk.Label(q_card, text=question["question"],
             font=FONT_HEADING, bg=CARD_DARK, fg=TEXT_LIGHT,
             wraplength=610, justify="left").pack(anchor="w", pady=(0, 16))

    choice_buttons = []
    for choice in question["choices"]:
        letter = choice[0]
        rb = tk.Radiobutton(
            q_card,
            text=choice,
            variable=selected_answer,
            value=letter,
            font=FONT_BODY,
            bg=CARD_DARK,
            fg=TEXT_LIGHT,
            selectcolor=BG_SPACE,
            activebackground=CARD_DARK,
            activeforeground=ACCENT_GOLD,
            anchor="w",
            padx=8,
            pady=5,
            cursor="hand2"
        )
        rb.pack(fill="x", pady=2)
        choice_buttons.append(rb)

    feedback_label = tk.Label(main_frame, text="", font=FONT_BOLD,
                              bg=BG_SPACE, fg=TEXT_LIGHT, wraplength=660)
    feedback_label.pack(pady=14)

    controls = tk.Frame(main_frame, bg=BG_SPACE)
    controls.pack()

    submit_button = tk.Button(
        controls, text="Submit Answer", font=FONT_BOLD,
        bg=ACCENT_CYAN, fg=BG_SPACE, relief="flat",
        width=16, pady=8, cursor="hand2", command=submit_answer
    )
    submit_button.pack(side="left", padx=10)

    is_last = current_question == len(quiz_questions) - 1
    next_button = tk.Button(
        controls,
        text="View Results" if is_last else "Next Question",
        font=FONT_BOLD,
        bg=ACCENT_GOLD,
        fg=BG_SPACE,
        disabledforeground=TEXT_MUTED,
        relief="flat",
        width=16,
        pady=8,
        state="disabled",
        cursor="hand2",
        command=next_question
    )
    next_button.pack(side="left", padx=10)

    update_timer()


# TIMER FUNCTIONS
def update_timer():
    """Decrement timer every 1000 ms until answered or time reaches 0."""
    global time_left, timer_job
    if answered:
        return
    timer_label.config(
        text=f"Time Left: {time_left}s",
        fg=WRONG_RED if time_left <= 5 else ACCENT_GOLD
    )
    if time_left == 0:
        time_up()
        return
    time_left -= 1
    timer_job = root.after(1000, update_timer)


def stop_timer():
    """Cancel any scheduled after() callback so the countdown stops immediately."""
    global timer_job
    if timer_job is not None:
        root.after_cancel(timer_job)
        timer_job = None


# ANSWER EVALUATION & NAVIGATION
def lock_choices():
    """Disable all radio buttons so the player cannot change or resubmit."""
    for button in choice_buttons:
        button.config(state="disabled")


def submit_answer():
    """Validate selection, stop timer, grade answer, and prevent double submission."""
    global score, answered
    if answered:
        return

    choice = selected_answer.get()
    if choice == "":
        messagebox.showwarning("Selection Required", "Please choose an answer before submitting.")
        return

    answered = True
    stop_timer()
    lock_choices()
    submit_button.config(state="disabled")

    question = quiz_questions[current_question]
    correct_letter = question["answer"]

    if choice == correct_letter:
        score += 1
        feedback_label.config(text="Correct! +1 point.", fg=CORRECT_GREEN)
    else:
        wrong_answers.append({
            "question": question["question"],
            "your_answer": get_choice_text(question, choice),
            "correct_answer": get_choice_text(question, correct_letter)
        })
        feedback_label.config(
            text=f"Incorrect. Correct answer: {get_choice_text(question, correct_letter)}",
            fg=WRONG_RED
        )

    next_button.config(state="normal")


def time_up():
    """Mark the current question wrong automatically when the timer reaches 0."""
    global answered
    if answered:
        return

    answered = True
    lock_choices()
    submit_button.config(state="disabled")

    question = quiz_questions[current_question]
    correct_text = get_choice_text(question, question["answer"])

    wrong_answers.append({
        "question": question["question"],
        "your_answer": "No answer (time ran out)",
        "correct_answer": correct_text
    })
    feedback_label.config(
        text=f"Time is up! Correct answer: {correct_text}",
        fg=WRONG_RED
    )
    next_button.config(state="normal")


def next_question():
    """Advance to the next shuffled question or open the final results screen."""
    global current_question
    current_question += 1
    if current_question < len(quiz_questions):
        show_question()
    else:
        show_results()


def show_results():
    """Display final score, percentage, feedback message, high score, and review."""
    clear_screen()
    total = len(quiz_questions)
    percentage = (score / total) * 100
    is_new_record = save_high_score(score)

    if percentage >= 90:
        message = "Mission Commander level! Outstanding Solar System knowledge."
    elif percentage >= 70:
        message = "Great orbit! You know your way around the Solar System."
    elif percentage >= 50:
        message = "Solid flight, though a few orbits need extra study."
    else:
        message = "Lost in deep space—review the topics and launch again!"

    tk.Label(main_frame, text="Mission Debrief", font=FONT_TITLE,
             bg=BG_SPACE, fg=ACCENT_GOLD).pack(pady=(4, 4))

    tk.Label(main_frame, text=f"Final Score: {score} / {total} ({percentage:.0f}%)",
             font=FONT_HEADING, bg=BG_SPACE, fg=TEXT_LIGHT).pack()

    tk.Label(main_frame, text=message, font=FONT_BODY,
             bg=BG_SPACE, fg=TEXT_MUTED).pack(pady=4)

    record_msg = (
        f"New High Score Saved: {get_high_score()} / {total}!"
        if is_new_record
        else f"Saved High Score: {get_high_score()} / {total}"
    )
    tk.Label(main_frame, text=record_msg, font=FONT_BOLD,
             bg=BG_SPACE, fg=CORRECT_GREEN if is_new_record else ACCENT_CYAN).pack(pady=(2, 10))

    tk.Label(main_frame, text="Answer Review (Missed or Timed-Out Questions)",
             font=FONT_BOLD, bg=BG_SPACE, fg=TEXT_LIGHT).pack(anchor="w", pady=(0, 4))

    review_container = tk.Frame(main_frame, bg=CARD_DARK)
    review_container.pack(fill="both", expand=True)

    scrollbar = tk.Scrollbar(review_container)
    scrollbar.pack(side="right", fill="y")

    review_box = tk.Text(
        review_container,
        height=9,
        wrap="word",
        font=FONT_BODY,
        bg=CARD_DARK,
        fg=TEXT_LIGHT,
        relief="flat",
        padx=12,
        pady=10,
        yscrollcommand=scrollbar.set
    )
    review_box.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=review_box.yview)

    if not wrong_answers:
        review_box.insert("end", "Flawless run! Every single question was answered correctly.")
    else:
        for idx, item in enumerate(wrong_answers, start=1):
            review_box.insert("end", f"{idx}. {item['question']}\n")
            review_box.insert("end", f"   Your answer: {item['your_answer']}\n")
            review_box.insert("end", f"   Correct answer: {item['correct_answer']}\n\n")

    review_box.config(state="disabled")

    footer = tk.Frame(main_frame, bg=BG_SPACE)
    footer.pack(pady=(14, 0))

    tk.Button(footer, text="Restart Quiz", font=FONT_BOLD,
              bg=ACCENT_GOLD, fg=BG_SPACE, relief="flat",
              width=15, pady=8, cursor="hand2", command=restart_quiz).pack(side="left", padx=10)

    tk.Button(footer, text="Exit", font=FONT_BOLD,
              bg="#2A355E", fg=TEXT_LIGHT, relief="flat",
              width=15, pady=8, cursor="hand2", command=on_close).pack(side="left", padx=10)


def restart_quiz():
    """Start a fresh round with reshuffled questions and reset score."""
    start_quiz()


def on_close():
    """Stop active timer callbacks before closing the window cleanly."""
    stop_timer()
    root.destroy()


# ENTRY POINT
root.protocol("WM_DELETE_WINDOW", on_close)
show_start_screen()
root.mainloop()