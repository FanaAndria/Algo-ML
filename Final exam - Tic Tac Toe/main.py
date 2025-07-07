import tkinter as tk
from tkinter import messagebox
from logic import TicTacToeAI, TicTacToeGame

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - Utilisateur vs IA")
        self.root.configure(bg="#22223b")
        self.center_window(520, 540)
        self.game = TicTacToeGame()
        self.ai = TicTacToeAI()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_widgets()
        self.update_board()
        self.update_status()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        # Création du cadre principal
        frame = tk.Frame(self.root, bg="#22223b")
        frame.pack(padx=20, pady=20)
        for i in range(3):
            for j in range(3):
                btn = tk.Button(frame, text="", font=("Arial", 36, "bold"), width=4, height=2,
                                bg="#4a4e69", fg="#f2e9e4", activebackground="#9a8c98",
                                command=lambda row=i, col=j: self.user_move(row, col),
                                relief="groove", bd=3)
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = btn
        self.status_label = tk.Label(self.root, text="", font=("Arial", 18, "bold"), bg="#22223b", fg="#f2e9e4")
        self.status_label.pack(pady=10)
        self.reset_btn = tk.Button(self.root, text="Rejouer", font=("Arial", 14), command=self.reset_board,
                                   bg="#c9ada7", fg="#22223b", activebackground="#f2e9e4", relief="ridge")
        self.reset_btn.pack(pady=5)

    def user_move(self, row, col):
        # Gestion du coup du joueur
        if self.game.board[row, col] == 0 and self.game.current_player == 1:
            self.game.make_move(row, col, 1)
            self.update_board()
            if self.game.check_winner(1):
                self.end_game("Félicitations, vous avez gagné !")
                return
            elif self.game.is_full():
                self.end_game("Match nul !")
                return
            self.game.current_player = -1
            self.root.after(500, self.ai_move)

    def ai_move(self):
        # Gestion du coup de l'IA
        move = self.ai.predict(self.game.board)
        if move:
            row, col = move
            self.game.make_move(row, col, -1)
            self.update_board()
            if self.game.check_winner(-1):
                self.end_game("L'IA a gagné !")
                return
            elif self.game.is_full():
                self.end_game("Match nul !")
                return
        self.game.current_player = 1
        self.update_status()

    def update_board(self):
        # Met à jour l'affichage des boutons selon l'état du plateau
        for i in range(3):
            for j in range(3):
                if self.game.board[i, j] == 1:
                    self.buttons[i][j]["text"] = "X"
                    self.buttons[i][j]["state"] = "disabled"
                    self.buttons[i][j]["bg"] = "#3849dd"  
                    self.buttons[i][j]["fg"] = "#ffffff"
                elif self.game.board[i, j] == -1:
                    self.buttons[i][j]["text"] = "O"
                    self.buttons[i][j]["state"] = "disabled"
                    self.buttons[i][j]["bg"] = "#e76f51"  
                    self.buttons[i][j]["fg"] = "#ffffff"
                else:
                    self.buttons[i][j]["text"] = ""
                    self.buttons[i][j]["state"] = "normal"
                    self.buttons[i][j]["bg"] = "#4a4e69"
                    self.buttons[i][j]["fg"] = "#f2e9e4"
        self.update_status()

    def update_status(self):
        if self.game.current_player == 1:
            self.status_label["text"] = "À vous de jouer (X)"
        else:
            self.status_label["text"] = "..."

    def end_game(self, message):
        self.update_board()
        answer = messagebox.askyesno("Fin de partie", f"{message}\n\nVoulez-vous rejouer ?")
        if answer:
            self.reset_board()
        else:
            for i in range(3):
                for j in range(3):
                    self.buttons[i][j]["state"] = "disabled"
            self.status_label["text"] = message

    def reset_board(self): 
        self.game.reset()
        self.update_board()
        self.update_status()

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
