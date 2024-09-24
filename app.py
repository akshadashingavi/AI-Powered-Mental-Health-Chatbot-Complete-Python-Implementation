import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import chat
import json

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("AI Chatbot")
        self.geometry("400x500")
        self.response = None
        self.user_data = {}  # Create a dictionary to store user data

        self.create_widgets()

    def create_widgets(self):
        self.chat_history = tk.Text(self, width=40, height=20, bg="lightgray")
        self.chat_history.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.input_box = tk.Entry(self)
        self.input_box.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.input_box.focus()

        self.send_button = ttk.Button(self, text="Send", command=self.send)
        self.send_button.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        self.history_update("Hi, I'm the AI Chatbot. How can I help you today?")

        # Bind Enter key to send message
        self.input_box.bind("<Return>", self.send)

    def send(self, event=None):
        user_input = self.input_box.get()
        self.history_update(f"User: {user_input}")

        self.response = chat.get_response(user_input, self.user_data)

        self.history_update(f"AI: {self.response}")

        self.input_box.delete(0, 'end')

    def history_update(self, message):
        self.chat_history.config(state='normal')
        self.chat_history.insert('end', message + "\n")
        self.chat_history.config(state='disabled')

def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()
