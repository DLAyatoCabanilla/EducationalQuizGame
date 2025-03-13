from tkinter import *
from tkinter import messagebox as mb
import json

class QuizLogic:
    def __init__(self, data_file):
        with open(data_file) as f:
            self.data = json.load(f)
        
        self.question = self.data['question']
        self.options = self.data['options']
        self.answer = self.data['answer']
        self.q_no = 0
        self.correct = 0

    def check_ans(self, selected_option):
        return selected_option == self.answer[self.q_no]

    def next_question(self, selected_option):
        if self.check_ans(selected_option):
            self.correct += 1
        self.q_no += 1
        return self.q_no < len(self.question)
    
    def get_score(self):
        wrong_count = len(self.question) - self.correct
        score = int(self.correct / len(self.question) * 100)
        return f"Score: {score}%\nCorrect: {self.correct}\nWrong: {wrong_count}"

class QuizGUI:
    def __init__(self, root):
        self.gui = root
        self.gui.geometry("800x450")
        self.gui.title("Technical Quiz")
        
    def display_title(self):
        title = Label(self.gui, text="TECHNICAL QUIZ", width=90, bg="purple", fg="white", font=("ariel", 20, "bold"))
        title.place(x=2, y=2)
    
    def create_buttons(self, next_cmd, quit_cmd):
        next_button = Button(self.gui, text="Next", command=next_cmd, width=10, bg="green", fg="white", font=("ariel", 16, "bold"))
        next_button.place(x=600, y=380)
        
        quit_button = Button(self.gui, text="Quit", command=quit_cmd, width=10, bg="red", fg="white", font=("ariel", 16, "bold"))
        quit_button.place(x=750, y=380)

class Quiz(QuizLogic, QuizGUI):
    def __init__(self, root, data_file):
        QuizLogic.__init__(self, data_file)
        QuizGUI.__init__(self, root)
        
        self.opt_selected = IntVar()
        self.opts = self.create_radio_buttons()
        
        self.display_title()
        self.display_question()
        self.display_options()
        self.create_buttons(self.next_btn, self.gui.destroy)

    def create_radio_buttons(self):
        q_list = []
        y_pos = 150
        for i in range(4):
            radio_btn = Radiobutton(self.gui, text="", variable=self.opt_selected, value=i+1, font=("ariel", 14))
            q_list.append(radio_btn)
            radio_btn.place(x=100, y=y_pos)
            y_pos += 40
        return q_list

    def display_question(self):
        self.q_label = Label(self.gui, text=self.question[self.q_no], width=120, font=("ariel", 16, "bold"), anchor="w")
        self.q_label.place(x=70, y=100)
    
    def display_options(self):
        self.opt_selected.set(0)
        for i, option in enumerate(self.options[self.q_no]):
            self.opts[i]['text'] = option

    def next_btn(self):
        if self.next_question(self.opt_selected.get()):
            self.display_question()
            self.display_options()
        else:
            mb.showinfo("Result", self.get_score())
            self.gui.destroy()

if __name__ == "__main__":
    root = Tk()
    quiz = Quiz(root, "data.json")
    root.mainloop()
