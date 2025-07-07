import numpy as np
import random
import os
import joblib
from tensorflow.keras.models import load_model

class TicTacToeAI:
    def __init__(self, model_dir='model'):
        self.model = None
        self.scaler = None

        model_path = os.path.join(model_dir, 'tic_tac_toe_model.h5')
        scaler_path = os.path.join(model_dir, 'scaler.pkl')

        if os.path.exists(model_path) and os.path.exists(scaler_path):
            self.model = load_model(model_path)
            self.scaler = joblib.load(scaler_path)
            print("Modèle et scaler chargés avec succès.")
        else:
            print("Modèle ou scaler manquant.")

    def predict(self, board, current_player=1):
        if self.model and self.scaler:
            # ajout du joueur courant
            input_board = board.flatten()
            input_with_player = np.append(input_board, current_player).reshape(1, -1)

            # scaling
            scaled_input = self.scaler.transform(input_with_player)

            # Prédiction
            predicted_probs = self.model.predict(scaled_input, verbose=0)[0]
            sorted_indices = np.argsort(predicted_probs)[::-1]

            # Sélection du meilleur coup valide
            for idx in sorted_indices:
                row, col = divmod(idx, 3)
                if board[row, col] == 0:
                    return (row, col)

            return None  # Aucun coup valide (plateau plein)
        
        # IA pour eviter une erreur : coup aléatoire
        moves = [(i, j) for i in range(3) for j in range(3) if board[i, j] == 0]
        return random.choice(moves) if moves else None

class TicTacToeGame:
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1  # 1 = joueur humain, -1 = IA

    def reset(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1

    def make_move(self, row, col, player):
        if self.board[row, col] == 0:
            self.board[row, col] = player
            return True
        return False

    def check_winner(self, player):
        for i in range(3):
            if all(self.board[i, :] == player) or all(self.board[:, i] == player):
                return True
        if all(self.board[i, i] == player for i in range(3)) or all(self.board[i, 2 - i] == player for i in range(3)):
            return True
        return False

    def is_full(self):
        return not np.any(self.board == 0)
