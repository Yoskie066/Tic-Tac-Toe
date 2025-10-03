import tkinter as tk
import random

class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.player_score = 0
        self.ai_score = 0
        self.current_player = 'Player'  
        self.game_mode = 'gui'  # Change to 'console' for console mode
        self.game_over = False  # To track if the game is over

        # Initialize GUI if selected
        if self.game_mode == 'gui':
            self.init_gui()
        else:
            self.play_game()

    def print_board(self):
        """Prints the current game board and scores."""
        print("Current Board:")
        for row in self.board:
            print(" | ".join(row))
            print("-" * 9)
        print(f"Score - Player: {self.player_score}, AI: {self.ai_score}")

    def check_winner(self):
        """Checks for a winner or a tie."""
        for row in self.board:
            if row.count(row[0]) == 3 and row[0] != ' ':
                return row[0]

        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return self.board[0][col]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]

        if all(cell != ' ' for row in self.board for cell in row):
            return 'Tie'

        return None

    def ai_move(self):
        """AI makes a random valid move."""
        if not self.game_over:  # Only allow AI to move if the game is not over
            available_moves = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' ']
            if available_moves:
                move = random.choice(available_moves)
                self.board[move[0]][move[1]] = 'O'
                if self.game_mode == 'gui':
                    self.buttons[move[0]][move[1]].config(text='O')

    def play_game(self):
        """Main function to run the Tic-Tac-Toe game in console mode."""
        while True:
            self.print_board()

            if self.current_player == 'Player':
                try:
                    row = int(input("Player, enter the row (0, 1, 2): "))
                    col = int(input("Player, enter the column (0, 1, 2): "))
                    if self.board[row][col] == ' ':
                        self.board[row][col] = 'X'
                    else:
                        print("Invalid move. Try again.")
                        continue
                except (IndexError, ValueError):
                    print("Invalid input. Try again.")
                    continue

            else:
                print("AI is making a move...")
                self.ai_move()

            winner = self.check_winner()
            if winner:
                self.print_board()
                if winner == 'X':
                    print("Player wins!")
                    self.player_score += 1
                elif winner == 'O':
                    print("AI wins!")
                    self.ai_score += 1
                else:
                    print("It's a tie!")

                play_again = input("Play again? (y/n): ").lower()
                if play_again == 'y':
                    self.board = [[' ' for _ in range(3)] for _ in range(3)]
                    self.current_player = 'Player'  # Reset to player start
                    self.game_over = False  # Reset game over status
                else:
                    break

    def init_gui(self):
        """Initializes the GUI with a neon color scheme."""
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.configure(bg='black')  


        self.frame = tk.Frame(self.window, bg='black')
        self.frame.pack(expand=True) 

        self.label = tk.Label(self.frame, text=f"{self.current_player}'s turn", font=("Helvetica", 20), bg='black', fg='cyan')
        self.label.grid(row=0, column=0, columnspan=3, pady=(10, 20)) 

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                self.buttons[row][col] = tk.Button(self.frame, text='', font=("Helveltica", 50), width=4, height=1,
                                                    bg='darkblue', fg='cyan',
                                                    activebackground='blue', activeforeground='yellow',
                                                    command=lambda r=row, c=col: self.set_tile(r, c))
                self.buttons[row][col].grid(row=row + 1, column=col, padx=5, pady=5) 

        self.score_label = tk.Label(self.frame, text=f"Score - Player: {self.player_score}, AI: {self.ai_score}",
                                     font=("Consolas", 16), bg='black', fg='cyan')
        self.score_label.grid(row=4, column=0, columnspan=3, pady=(20, 10))  

        self.restart_button = tk.Button(self.frame, text="Restart", font=("Consolas", 20), bg='darkblue', fg='cyan',
                                         activebackground='blue', activeforeground='yellow',
                                         command=self.new_game)
        self.restart_button.grid(row=5, column=0, columnspan=3, pady=(10, 20)) 

        self.frame.pack()
        self.window.mainloop()

    def set_tile(self, row, column):
        """Sets the tile for the player in GUI mode."""
        if not self.game_over:  # Allow move only if the game is not over
            if self.board[row][column] == ' ':
                self.board[row][column] = 'X'
                self.buttons[row][column].config(text='X')
                winner = self.check_winner()
                if winner:
                    self.handle_winner(winner)
                else:
                    self.current_player = 'AI'  # Change current player to AI
                    self.label.config(text="AI's turn")
                    self.ai_move()
                    winner = self.check_winner()
                    if winner:
                        self.handle_winner(winner)

    def handle_winner(self, winner):
        """Handles the winner scenario in GUI mode."""
        self.game_over = True  # Set the game as over
        if winner == 'X':
            self.label.config(text="Player wins!")
            self.player_score += 1
        elif winner == 'O':
            self.label.config(text="AI wins!")
            self.ai_score += 1
        else:
            self.label.config(text="It's a tie!")

        self.score_label.config(text=f"Score - Player: {self.player_score}, AI: {self.ai_score}")

    def new_game(self):
        """Starts a new game in GUI mode."""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'Player'  # Reset current player to Player
        self.game_over = False  # Reset game over status
        self.label.config(text=f"{self.current_player}'s turn")

        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text='')

# Run the game in either console or GUI mode
if __name__ == "__main__":
    TicTacToe()

