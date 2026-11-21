# TKINTER-QUIZ-SYSTEM
# Solar System Explorer Quiz

**Name:** Adrian J. Tor
**Section:** SE - 3A
**Topic:** The Solar System

## How to Run the Program

1. Make sure Python 3 is installed on your machine (Tkinter comes built-in on Windows and macOS).[span_3](start_span)[span_3](end_span)
2. Open the folder containing `quiz.py` in your terminal or code editor.[span_4](start_span)[span_4](end_span)
3. Run the file using:
   ```bash
   python quiz.py


## Features Completed
- ​10 multiple-choice questions about the Solar System (4 choices each)<br>
- ​Questions shuffle every time you start or restart the quiz<br>
- 15-second countdown timer per question that auto-fails when time runs out
- ​Instant answer checking that locks choices so you can't double-submit
- Progress tracker showing the current question number and remaining time
- Results screen with final score, percentage, and custom feedback message
- Answer review box showing all missed questions and their right answers
- High score saved in high_score.txt so it stays even after closing the app
- Restart button and custom dark-space UI theme

## ​How the Questions Are Stored and Shuffled
​I stored all 10 questions inside a list of dictionaries called QUESTIONS, where each dictionary holds the question text, a list of four choices, and the correct letter. I left out hardcoded numbers in the question strings since the UI handles numbering dynamically. When start_quiz() runs, random.sample() creates a shuffled copy of the list so the order is different every round without messing up the original list.

## ​How the Timer Works
​Each question sets time_left to 15 seconds and calls update_timer(). Instead of time.sleep(), which freezes Tkinter, update_timer() uses root.after(1000, update_timer) to tick down once every second. As soon as you click Submit, stop_timer() cancels the scheduled loop with root.after_cancel(). If the timer hits 0 first, time_up() runs automatically and marks the item wrong.

## ​How the Program Identifies the Correct Answer
​Every Radiobutton stores its option letter (A, B, C, or D) in selected_answer. When you click Submit, submit_answer() checks if an option was picked, locks the buttons so you can't submit twice, and compares your letter against question["answer"]. If they match, you get 1 point; otherwise, the question, your choice, and the right answer get saved to wrong_answers for the review screen.

## ​How the Score and High Score Work
​You earn 1 point per correct answer, and the percentage is computed with (score / total) * 100. For persistence, get_high_score() checks if high_score.txt exists in the same folder as quiz.py and reads the saved integer (or returns 0 if none exists yet). When the quiz ends, save_high_score() overwrites the text file only if your new score beats the old record.

## Function Explanations
​show_start_screen() | | | Clears the frame and loads the title, rules, saved high score, and start button when the app opens.
start_quiz() - Resets the score, question counter, and wrong answers list, then shuffles the questions when Start or Restart is clicked.
3.​show_question() - Displays the current question, choices, progress label, and starts the 15-second timer.
4.​update_timer() - Updates the countdown label every second until you submit an answer or the timer hits 0.
​5.submit_answer() - Stops the timer, locks the radio buttons, checks your selected letter, and enables the Next button.
6.​time_up() - Triggers at 0 seconds to mark the question wrong, show the right answer, and unlock the Next button.
​6.save_high_score() - Checks if your final score is higher than the stored record and writes it to high_score.txt.
7.​show_results() - Calculates your percentage, displays your performance message, and lists missed questions in the review box.

## ​Screenshots
​Challenges I Faced
​The trickiest part was keeping the timer from overlapping or still running in the background after submitting an answer or closing the window. Tracking the active callback with timer_job and cancelling it inside stop_timer() and on_close() fixed the timing bugs and kept the UI responsive.
