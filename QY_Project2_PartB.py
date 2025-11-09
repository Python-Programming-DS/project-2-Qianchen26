
class Board:
    
    def __init__(self):
        """Initialize the board with empty cells."""
        self.c = [[" ", " ", " "],
                  [" ", " ", " "],
                  [" ", " ", " "]]
      
    def printBoard(self):
        BOARD_HEADER = "-----------------\n|R\\C| 0 | 1 | 2 |\n-----------------"
        print(BOARD_HEADER)

        for i in range(3):
            print(f"| {i} | {self.c[i][0]} | {self.c[i][1]} | {self.c[i][2]} |")
            print("-----------------")

    
class Game:

    def __init__(self, human_player='X'):
        """
        Initialize the game with an empty board.
        """
        self.board = Board()
        self.turn = 'X'  # X always goes first
        self.human = human_player
        self.computer = 'O' if human_player == 'X' else 'X'

    def switchPlayer(self):
        """Switch the current player between X and O."""
        if self.turn == 'X':
            self.turn = 'O'
        else:
            self.turn = 'X'
    
    def validateEntry(self, row, col):
        """
        Validate if a move is legal.
        
        Args:
            row (int): Row index (0-2)
            col (int): Column index (0-2)
            
        Returns:
            bool: True if the move is valid, False otherwise
        """
        if row < 0 or row > 2 or col < 0 or col > 2:
            return False
        
        if self.board.c[row][col] != " ":
            return False
        
        return True

    def checkFull(self):
        """
        Check if the board is completely filled.
        
        Returns:
            bool: True if all cells are occupied, False otherwise
        """
        for i in range(3):
            for j in range(3):
                if self.board.c[i][j] == " ":
                    return False
        return True
    
    def checkWin(self):
        """
        Check if there is a winner in the current board state.
        
        Returns:
            bool: True if there is a winner, False otherwise
        """
        # Check rows
        for i in range(3):
            if (self.board.c[i][0] == self.board.c[i][1] == self.board.c[i][2] 
                and self.board.c[i][0] != " "):
                return True
        
        # Check columns
        for j in range(3):
            if (self.board.c[0][j] == self.board.c[1][j] == self.board.c[2][j] 
                and self.board.c[0][j] != " "):
                return True
        
        # Check diagonals
        if (self.board.c[0][0] == self.board.c[1][1] == self.board.c[2][2] 
            and self.board.c[0][0] != " "):
            return True
        
        if (self.board.c[0][2] == self.board.c[1][1] == self.board.c[2][0] 
            and self.board.c[0][2] != " "):
            return True
        
        return False
    
    def getWinner(self):
        """
        Determine the winner of the game.
        
        Returns:
            str: The winning player's mark, or None if no winner
        """
        # Check rows
        for i in range(3):
            if (self.board.c[i][0] == self.board.c[i][1] == self.board.c[i][2] 
                and self.board.c[i][0] != " "):
                return self.board.c[i][0]
        
        # Check columns
        for j in range(3):
            if (self.board.c[0][j] == self.board.c[1][j] == self.board.c[2][j] 
                and self.board.c[0][j] != " "):
                return self.board.c[0][j]
        
        # Check diagonals
        if (self.board.c[0][0] == self.board.c[1][1] == self.board.c[2][2] 
            and self.board.c[0][0] != " "):
            return self.board.c[0][0]
        
        if (self.board.c[0][2] == self.board.c[1][1] == self.board.c[2][0] 
            and self.board.c[0][2] != " "):
            return self.board.c[0][2]
        
        return None
    
    def checkEnd(self):
        """
        Check if the game has reached an end condition.
        
        Returns:
            bool: True if the game is over, False otherwise
        """
        if self.checkWin():
            print(f"Player {self.turn} wins!")
            return True
        
        if self.checkFull():
            print("DRAW! NOBODY WINS!")
            return True
        
        return False
    
    def getAvailableMoves(self):
        """
        Get all available positions on the board.
        
        Returns:
            list: List of tuples (row, col) representing empty cells
        """
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board.c[i][j] == " ":
                    moves.append((i, j))
        return moves
    
    def minimax(self, depth, is_maximizing):
        """
        Minimax algorithm to determine the best move for the computer.
        
        The algorithm recursively evaluates all possible game states:
        - Maximizing player (computer) tries to maximize the score
        - Minimizing player (human) tries to minimize the score
        
        Args:
            depth (int): Current depth in the game tree
            is_maximizing (bool): True if maximizing player's turn, False otherwise
            
        Returns:
            int: Score for the current board state
                 +10 if computer wins, -10 if human wins, 0 for draw
        """
        # Check terminal states
        winner = self.getWinner()
        if winner == self.computer:
            return 10 - depth  # Prefer faster wins
        elif winner == self.human:
            return depth - 10  # Prefer slower losses
        elif self.checkFull():
            return 0  # Draw
        
        if is_maximizing:
            # Computer's turn - maximize score
            max_score = float('-inf')
            for row, col in self.getAvailableMoves():
                # Try this move
                self.board.c[row][col] = self.computer
                score = self.minimax(depth + 1, False)
                # Undo the move
                self.board.c[row][col] = " "
                max_score = max(score, max_score)
            return max_score
        else:
            # Human's turn - minimize score
            min_score = float('inf')
            for row, col in self.getAvailableMoves():
                # Try this move
                self.board.c[row][col] = self.human
                score = self.minimax(depth + 1, True)
                # Undo the move
                self.board.c[row][col] = " "
                min_score = min(score, min_score)
            return min_score
    
    def getBestMove(self):
        """
        Find the best move for the computer using Minimax algorithm.
        
        Returns:
            tuple: (row, col) representing the best move
        """
        best_score = float('-inf')
        best_move = None
        
        # Evaluate all available moves
        for row, col in self.getAvailableMoves():
            # Try this move
            self.board.c[row][col] = self.computer
            score = self.minimax(0, False)
            # Undo the move
            self.board.c[row][col] = " "
            
            # Update best move if this move is better
            if score > best_score:
                best_score = score
                best_move = (row, col)
        
        return best_move

    def playGame(self):
        """
        Main game loop for playing against the computer.
        Human plays as one mark, computer plays as the other using Minimax.
        """
        print("\n=== Welcome to Tic-Tac-Toe vs Computer ===")
        print(f"You are {self.human}, Computer is {self.computer}")
        print(f"{self.turn} goes first!\n")
        
        while True:
            self.board.printBoard()
            
            if self.turn == self.human:
                # Human player's turn
                print(f"\nYour turn ({self.human})")
                while True:
                    try:
                        row = int(input("Enter row (0-2): "))
                        col = int(input("Enter column (0-2): "))
                        
                        if self.validateEntry(row, col):
                            break
                        else:
                            print("Invalid move! Cell is either occupied or out of range.")
                    except ValueError:
                        print("Invalid input! Please enter numbers between 0 and 2.")
                
                self.board.c[row][col] = self.turn
            else:
                # Computer's turn using Minimax
                print(f"\nComputer's turn ({self.computer})...")
                row, col = self.getBestMove()
                self.board.c[row][col] = self.turn
                print(f"Computer chose: Row {row}, Column {col}")
            
            # Check if game has ended
            if self.checkEnd():
                self.board.printBoard()
                break
            
            # Switch players
            self.switchPlayer()


def main():
    """
    Main function to run the Tic-Tac-Toe game with Minimax AI.
    """
    play_again = 'y'

    while play_again.lower() == 'y':
        # Ask player which mark they want to use
        while True:
            choice = input("Do you want to be X or O? (X goes first): ").upper()
            if choice in ['X', 'O']:
                break
            print("Invalid choice! Please enter X or O.")
        
        # Create and play the game
        game = Game(human_player=choice)
        game.playGame()
        
        play_again = input("\nDo you want to play again? (y/n): ")
    
    print("Thank you for playing!")

    
if __name__ == "__main__":
    main()