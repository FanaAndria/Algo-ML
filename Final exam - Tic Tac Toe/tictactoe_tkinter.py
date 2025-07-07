import tkinter as tk
from tkinter import messagebox
import pickle  # Pour charger les modèles IA
import numpy as np  # Pour préparer l'entrée du modèle unique

# Classe principale du jeu Tic Tac Toe
class TicTacToe:
    def __init__(self, root):
        # Initialisation de la fenêtre principale
        self.root = root
        self.root.title("Tic Tac Toe - Joueur vs IA")
        # Par défaut, le joueur est X et l'IA est O
        self.player_symbol = 'X'  # Symbole du joueur humain
        self.ai_symbol = 'O'      # Symbole de l'IA
        self.current_symbol = self.player_symbol
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_menu()
        self.create_board()
        self.create_restart_button()
        self.ai_starts = False
        self.model_path = 'model/final_tic_tac_toe_model.pkl'  # Chemin du modèle unique
        self.ai_model = None
        self.load_ai_model()  # Charger le modèle IA unique

    def create_menu(self):
        # Menu pour choisir qui commence et qui est l'IA
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        # Ajout d'un sous-menu pour choisir le symbole de l'IA
        ai_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Choix IA", menu=ai_menu)
        ai_menu.add_command(label="IA = X", command=self.ai_first)
        ai_menu.add_command(label="IA = O", command=self.player_first)

    def set_ai_x(self):
        # Fonction pour définir l'IA comme X
        self.ai_symbol = 'X'
        self.player_symbol = 'O'
        self.restart_game()

    def set_ai_o(self):
        # Fonction pour définir l'IA comme O
        self.ai_symbol = 'O'
        self.player_symbol = 'X'
        self.restart_game()

    def load_ai_model(self):
        # Charge le modèle IA unique (pour X et O)
        try:
            with open(self.model_path, 'rb') as f:
                self.ai_model = pickle.load(f)
        except Exception as e:
            self.ai_model = None
            print(f"Erreur lors du chargement du modèle IA : {e}")

    def create_board(self):
        # Création de la grille de boutons
        frame = tk.Frame(self.root)
        frame.pack()
        for i in range(3):
            for j in range(3):
                btn = tk.Button(frame, text='', font=('Arial', 40), width=5, height=2,
                                command=lambda row=i, col=j: self.player_move(row, col))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def create_restart_button(self):
        # Bouton pour recommencer la partie
        restart_btn = tk.Button(self.root, text="Recommencer", font=('Arial', 14), command=self.restart_game)
        restart_btn.pack(pady=10)

    def player_first(self):
        # Fonction appelée si le joueur commence
        self.ai_starts = False
        self.ai_symbol = 'O'  # L'IA joue 'O' si le joueur commence
        self.player_symbol = 'X'
        self.restart_game()

    def ai_first(self):
        # Fonction appelée si l'IA commence
        self.ai_starts = True
        self.ai_symbol = 'X'  # L'IA joue 'X' si elle commence
        self.player_symbol = 'O'
        self.restart_game()
        self.root.after(500, self.ai_move)

    def player_move(self, row, col):
        # Gestion du coup du joueur
        if self.board[row][col] is None and self.current_symbol == self.player_symbol:
            self.make_move(row, col, self.player_symbol)
            if not self.check_game_over():
                self.root.after(500, self.ai_move)

    def ai_move(self):
        # Gestion du coup de l'IA (à remplacer par le modèle plus tard)
        if self.current_symbol == self.ai_symbol:
            row, col = self.get_ai_move()
            if row is not None and col is not None:
                self.make_move(row, col, self.ai_symbol)
                self.check_game_over()

    def get_ai_move(self):
        # Utilise le modèle IA unique pour choisir le coup optimal
        if self.ai_model is None:
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] is None:
                        return i, j
            return None, None
        try:
            # Préparer l'entrée : 0 pour vide, 1 pour X, -1 pour O
            board_state = []
            for i in range(3):
                for j in range(3):
                    val = self.board[i][j]
                    if val == 'X':
                        board_state.append(1)
                    elif val == 'O':
                        board_state.append(-1)
                    else:
                        board_state.append(0)
            # Déterminer le joueur courant pour le modèle : 1 pour X, -1 pour O
            current_player = 1 if self.current_symbol == 'X' else -1
            input_data = np.array(board_state + [current_player]).reshape(1, -1)
            # Prédiction du modèle : retourne l'index de la meilleure case (0-8)
            prediction = self.ai_model.predict(input_data)
            move_idx = prediction[0]
            row, col = divmod(move_idx, 3)
            if self.board[row][col] is None:
                return row, col
        except Exception as e:
            print(f"Erreur IA : {e}")
        # Si erreur, choisir le premier coup libre
        for i in range(3):
            for j in range(3):
                if self.board[i][j] is None:
                    return i, j
        return None, None

    def make_move(self, row, col, symbol):
        # Applique le coup sur la grille
        self.board[row][col] = symbol
        self.buttons[row][col].config(text=symbol, state='disabled')
        self.current_symbol = self.ai_symbol if symbol == self.player_symbol else self.player_symbol

    def check_game_over(self):
        # Vérifie si la partie est terminée (victoire ou égalité)
        winner = self.check_winner()
        if winner:
            messagebox.showinfo("Fin de la partie", f"Le gagnant est : {winner}")
            self.disable_all_buttons()
            return True
        elif all(self.board[i][j] is not None for i in range(3) for j in range(3)):
            messagebox.showinfo("Fin de la partie", "Match nul !")
            self.disable_all_buttons()
            return True
        return False

    def check_winner(self):
        # Détection du gagnant
        lines = []
        # Lignes et colonnes
        for i in range(3):
            lines.append(self.board[i])
            lines.append([self.board[j][i] for j in range(3)])
        # Diagonales
        lines.append([self.board[i][i] for i in range(3)])
        lines.append([self.board[i][2-i] for i in range(3)])
        for line in lines:
            if line[0] and line.count(line[0]) == 3:
                return line[0]
        return None

    def disable_all_buttons(self):
        # Désactive tous les boutons après la fin de la partie
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state='disabled')

    def restart_game(self):
        # Réinitialise la grille et l'état du jeu
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_symbol = self.player_symbol if not self.ai_starts else self.ai_symbol
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text='', state='normal')
        if self.ai_starts:
            self.root.after(500, self.ai_move)

# Lancement de l'application
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop() 