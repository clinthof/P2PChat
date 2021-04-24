import socket as s
import threading as t
import tkinter as tk
import datetime

buf_size = 4096
HOST = 'localhost'
PORT = 1024

client = s.socket(s.AF_INET, s.SOCK_STREAM)
client.connect((HOST, PORT))


class OUI_GUI:

    def __init__(self):
        self.chat_window = tk.Tk()
        self.chat_window.withdraw()
        self.login = tk.Toplevel()
        self.login.title("Login")
        self.login.configure(width=400, height=200)
        self.auth = tk.Label(self.login, text="Please create a username",
                             justify=tk.CENTER, font="Arial 22 bold")
        self.auth.place(relheight=0.15, relx=0.2, rely=0.8)
        self.create_user = tk.Label(
            self.login, text="Username: ", font="Arial 20")
        self.create_user.place(relheight=0.2, relx=0.1, rely=0.2)
        self.name = tk.Entry(self.login, font="Arial 22")
        self.name.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.2)
        self.login_user = tk.Button(self.login, text="log in", font="Arial 22 bold",
                                    command=lambda: self.render_chat_window(self.name.get()))
        self.login_user.place(relx=0.4, rely=0.55)
        self.chat_window.mainloop()

    def render_chat_window(self, username):
        try:
            self.login.destroy()
            self.render_layout(username)
            get = t.Thread(target=self.receive)
            get.start()
        except Exception as e:
            print(f'Error occurred while rendering chat window.  {e}')
            client.close()

    def render_layout(self, username):
        try:
            self.username = username
            self.chat_window.deiconify()
            self.chat_window.title("Felix & Mike App")
            self.chat_window.configure(width=600, height=400, bg="black")
            self.line = tk.Label(self.chat_window, width=450, bg="white")
            self.line.place(relwidth=1, rely=0.07, relheight=0.012)
            self.msg_field = tk.Text(self.chat_window, width=20, height=2,
                                     bg="black", fg="green", font="Arial 22", padx=5, pady=5)
            self.msg_field.place(relheight=0.745, relwidth=1, rely=0.08)
            self.send_field = tk.Label(self.chat_window, bg="white", height=40)
            self.send_field.place(relwidth=1, rely=0.825)
            self.entry_msg = tk.Entry(
                self.send_field, bg="black", fg="green", font="Arial 23")
            self.entry_msg.place(
                relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
            self.entry_msg.focus()
            self.send_btn = tk.Button(self.send_field, text="SEND ➤", font="Arial 20 bold", height=38,
                                      width=18, bg="black", fg="green", command=lambda: self.send_button(self.entry_msg.get()))
            self.send_btn.place(relx=0.77, rely=0.008,
                                relheight=0.06, relwidth=0.22)
            self.msg_field.config(cursor="arrow")
            scroll_bar = tk.Scrollbar(self.msg_field)
            scroll_bar.place(relheight=1, relx=0.974)
            scroll_bar.config(command=self.msg_field.yview)
        except Exception as e:
            print(f'Error in layout.  {e}')
            client.close()

    def send_button(self, msg):
        try:
            self.msg = msg
            self.entry_msg.delete(0, tk.END)
            send_msg = t.Thread(target=self.send)
            send_msg.start()
        except Exception as e:
            print(f'Error while sending (send_button function): {e}')
            client.close()

    def send(self):
        self.msg_field.config(state=tk.DISABLED)
        while True:
            try:
                time = datetime.datetime.now().strftime("%I:%M")
                message = (f'[{self.username}] at {time}: {self.msg}')
                client.send(message.encode("utf-8"))
                break
            except Exception as e:
                print(f'Error occurred sending the message (client): {e}')
                client.close()
                break

    def receive(self):
        while True:
            try:
                message = client.recv(buf_size).decode("utf-8")

                self.msg_field.config(state=tk.NORMAL)
                self.msg_field.insert(tk.END, f'{message}\n\n')
                self.msg_field.config(state=tk.DISABLED)
                self.msg_field.see(tk.END)
            except Exception as e:
                print(f'Error occurred receving the message {e}')
                client.close()
                break


g = OUI_GUI()
