# TKINTER-QUIZ-SYSTEM
# Solar System Explorer Quiz

**Name:** Adrian J. Tor
**Section:** BS INFORTECH SE-3A
**Topic:** The Solar System

## How to Run the Program
1. Make sure Python 3 (with Tkinter included) is installed on your computer[span_2](start_span)[span_2](end_span).
2. Download or clone the repository and open the project folder containing `quiz.py`[span_3](start_span)[span_3](end_span).
3. Run `quiz.py` from your terminal/command prompt or Python IDE:
   ```bash
   python quiz.py
   
#Features Completed
​[x] 10 multiple-choice questions on the Solar System with four choices (A–D) each
​[x] Random question order every time the quiz starts or restarts
​[x] 15-second countdown timer per question with automatic time-out handling
​[x] Answer checking, double-submission prevention, and score tracking (1 point per correct answer)
​[x] Progress indicator showing the current question number and remaining time
​[x] Results screen displaying final score, percentage, and a score-based performance message
​[x] Answer review listing every incorrect or timed-out question alongside the correct answer
​[x] High score saved persistently in a text file (high_score.txt) across sessions
​[x] Working Restart button and custom dark-space Tkinter interface
​#How the Questions Are Stored and Shuffled
​All 10 Solar System questions are stored inside a list named QUESTIONS, where each item is a dictionary containing "question", "choices" (a list of four lettered options), and "answer" (the single correct letter). Question numbers are not hardcoded into the question text; instead, the UI displays current_question + 1 dynamically. Whenever start_quiz() runs, random.sample(QUESTIONS, len(QUESTIONS)) creates a newly shuffled copy of the questions without modifying the original QUESTIONS list.

​#How the Timer Works
​Each question starts with time_left set to 15 seconds (TIME_LIMIT) and calls update_timer(). update_timer() uses Tkinter's root.after(1000, update_timer) to schedule itself once every second without freezing the GUI. If answered becomes True (when an answer is submitted), update_timer() stops scheduling further ticks and stop_timer() cancels any pending timer_job using root.after_cancel(). If time_left reaches 0 before submission, time_up() is triggered to mark the question wrong automatically and reveal the correct answer.

​#How the Program Identifies the Correct Answer
​Each Radiobutton uses its choice letter ("A", "B", "C", or "D") as its value linked to selected_answer. When submit_answer() runs, it checks that answered is False and that a choice was selected, then sets answered = True, stops the timer, disables the radio buttons and Submit button to block double submission, and compares choice == question["answer"]. Matching answers increment score by 1, while mismatches or time-outs record the question, the user's response, and the full text of the correct choice into wrong_answers for the final review.

#​How the Score and High Score Work
​The player earns 1 point for each question answered correctly before time expires, and the percentage on the results screen is calculated as (score / total) * 100. get_high_score() reads high_score.txt (located beside quiz.py using os.path.dirname(os.path.abspath(__file__))) and returns 0 if the file does not exist yet or contains invalid text. On the results screen, save_high_score(score) compares new_score against the saved high score and overwrites high_score.txt only when new_score > get_high_score().
