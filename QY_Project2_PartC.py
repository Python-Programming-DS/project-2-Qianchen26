"""
Tic-Tac-Toe Game with Machine Learning Player

This program implements Tic-Tac-Toe where a human plays against an ML-based AI.
The AI uses a trained dataset to predict optimal moves.

Dataset format:
- Intermediate boards (tictac_single.txt): x0,x1,...,x8,y where y is the best move index
- Endgame positions (tictac_final.txt): x0,x1,...,x8,y where y is the winner
- Board encoding: +1 for X, -1 for O, 0 for empty

Board positions:
    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8

Author: QC
Date: November 2025
"""

import random


class Board:
    """
    Board class represents the Tic-Tac-Toe game board.
    
    Attributes:
        c (list): A 3x3 grid representing the board cells
    """
    
    def __init__(self):
        """Initialize the board with empty cells."""
        self.c = [[" ", " ", " "],
                  [" ", " ", " "],
                  [" ", " ", " "]]
      
    def printBoard(self):
        """Display the current state of the game board."""
        BOARD_HEADER = "-----------------\n|R\\C| 0 | 1 | 2 |\n-----------------"
        print(BOARD_HEADER)

        for i in range(3):
            print(f"| {i} | {self.c[i][0]} | {self.c[i][1]} | {self.c[i][2]} |")
            print("-----------------")
    
    def getBoardState(self):
        """
        Convert the current board to a list format for ML prediction.
        
        Returns:
            list: Board state as a list of 9 integers (+1 for X, -1 for O, 0 for empty)
        """
        state = []
        for i in range(3):
            for j in range(3):
                if self.c[i][j] == 'X':
                    state.append(1)
                elif self.c[i][j] == 'O':
                    state.append(-1)
                else:
                    state.append(0)
        return state
    
    def indexToRowCol(self, index):
        """
        Convert a board index (0-8) to row and column.
        
        Args:
            index (int): Board position index (0-8)
            
        Returns:
            tuple: (row, col) coordinates
        """
        row = index // 3
        col = index % 3
        return row, col


class MLPlayer:
    """
    Machine Learning player that uses a dataset to make predictions.
    
    Attributes:
        dataset (list): List of board states and their optimal moves
        dataset_type (str): Type of dataset ('single' or 'final')
    """
    
    def __init__(self, dataset_file):
        """
        Initialize the ML player by loading the dataset.
        
        Args:
            dataset_file (str): Path to the dataset file
        """
        self.dataset = []
        self.dataset_type = self.loadDataset(dataset_file)
        print(f"Loaded {len(self.dataset)} examples from dataset")
    
    def loadDataset(self, filename):
        """
        Load the dataset from a file.
        
        Args:
            filename (str): Path to the dataset file
            
        Returns:
            str: Type of dataset loaded ('single' or 'final')
        """
        try:
            with open(filename, 'r') as f:
                for line in f:
                    # Parse each line: x0 x1 ... x8 y (space-separated)
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue
                    values = [int(x) for x in line.split()]
                    if len(values) == 10:  # 9 board positions + 1 output
                        board_state = values[:9]
                        output = values[9]
                        self.dataset.append((board_state, output))
            
            # Determine dataset type based on filename
            if 'single' in filename.lower():
                return 'single'
            elif 'final' in filename.lower():
                return 'final'
            else:
                return 'single'  # Default
                
        except FileNotFoundError:
            print(f"Warning: Dataset file '{filename}' not found.")
            print("ML player will use random moves.")
            return 'single'
    
    def findBestMove(self, current_state):
        """
        Find the best move for the given board state using the dataset.
        
        For intermediate boards dataset:
        - Looks for exact match in dataset and returns the optimal move
        
        For endgame dataset:
        - Uses k-nearest neighbors approach to find similar positions
        
        Args:
            current_state (list): Current board state (9 integers)
            
        Returns:
            int: Index of the best move (0-8), or None if not found
        """
        if not self.dataset:
            return None
        
        if self.dataset_type == 'single':
            # For intermediate boards, look for exact match
            for board_state, best_move in self.dataset:
                if board_state == current_state:
                    return best_move
        
        elif self.dataset_type == 'final':
            # For endgame dataset, use similarity-based approach
            # Find most similar board states
            similar_moves = self.findSimilarBoardMoves(current_state)
            if similar_moves:
                # Return most common move from similar boards
                return max(set(similar_moves), key=similar_moves.count)
        
        return None
    
    def findSimilarBoardMoves(self, current_state, k=5):
        """
        Find moves from k most similar board states.
        
        Args:
            current_state (list): Current board state
            k (int): Number of similar boards to consider
            
        Returns:
            list: Moves from similar board states
        """
        similarities = []
        
        for board_state, output in self.dataset:
            # Calculate similarity (number of matching positions)
            similarity = sum(1 for i in range(9) if current_state[i] == board_state[i])
            similarities.append((similarity, board_state, output))
        
        # Sort by similarity and get top k
        similarities.sort(reverse=True, key=lambda x: x[0])
        top_k = similarities[:k]
        
        # For final dataset, we need to infer good moves from similar positions
        # This is a simplified approach - in practice, you'd want more sophisticated logic
        moves = []
        for sim, board, winner in top_k:
            # Find differences between boards (potential moves)
            for i in range(9):
                if current_state[i] == 0 and board[i] != 0:
                    moves.append(i)
        
        return moves


class Game:
    """
    Game class implements the Tic-Tac-Toe game logic with ML player.
    
    Attributes:
        board (Board): The game board object
        turn (str): Current player's mark ('X' or 'O')
        human (str): Human player's mark
        computer (str): Computer player's mark
        ml_player (MLPlayer): The machine learning player
    """

    def __init__(self, human_player='X', dataset_file='tictac_single.txt'):
        """
        Initialize the game with an empty board and ML player.
        
        Args:
            human_player (str): The mark for the human player ('X' or 'O')
            dataset_file (str): Path to the ML dataset file
        """
        self.board = Board()
        self.turn = 'X'  # X always goes first
        self.human = human_player
        self.computer = 'O' if human_player == 'X' else 'X'
        self.ml_player = MLPlayer(dataset_file)

    def switchPlayer(self):
        """Switch the current player between X and O."""
        self.turn = 'O' if self.turn == 'X' else 'X'
    
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
            list: List of indices (0-8) representing empty cells
        """
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board.c[i][j] == " ":
                    moves.append(i * 3 + j)
        return moves
    
    def getMLMove(self):
        """
        Get the computer's move using ML prediction.
        Falls back to random move if ML prediction not available.
        
        Returns:
            tuple: (row, col) representing the chosen move
        """
        # Get current board state
        current_state = self.board.getBoardState()
        
        # Try to get ML prediction
        best_move_index = self.ml_player.findBestMove(current_state)
        
        # If ML found a valid move, use it
        if best_move_index is not None:
            available_moves = self.getAvailableMoves()
            if best_move_index in available_moves:
                print("(Using ML prediction)")
                return self.board.indexToRowCol(best_move_index)
        
        # Fallback: use random move for early game or when ML can't predict
        print("(Using random move - early game or no ML match)")
        available_moves = self.getAvailableMoves()
        random_index = random.choice(available_moves)
        return self.board.indexToRowCol(random_index)

    def playGame(self):
        """
        Main game loop for playing against the ML computer.
        Human plays as one mark, computer plays using ML predictions.
        """
        print("\n=== Welcome to Tic-Tac-Toe vs ML Computer ===")
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
                # Computer's turn using ML
                print(f"\nComputer's turn ({self.computer})...")
                row, col = self.getMLMove()
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
    Main function to run the Tic-Tac-Toe game with ML player.
    """
    print("=== Tic-Tac-Toe with Machine Learning ===\n")
    
    # Ask for dataset file
    print("Available datasets:")
    print("1. tictac_single.txt (Intermediate boards - optimal play)")
    print("2. tictac_final.txt (Endgame positions)")
    
    while True:
        choice = input("\nSelect dataset (1 or 2): ").strip()
        if choice == '1':
            dataset_file = 'tictac_single.txt'
            break
        elif choice == '2':
            dataset_file = 'tictac_final.txt'
            break
        else:
            print("Invalid choice! Please enter 1 or 2.")
    
    play_again = 'y'

    while play_again.lower() == 'y':
        # Ask player which mark they want to use
        while True:
            player_choice = input("\nDo you want to be X or O? (X goes first): ").upper()
            if player_choice in ['X', 'O']:
                break
            print("Invalid choice! Please enter X or O.")
        
        # Create and play the game
        game = Game(human_player=player_choice, dataset_file=dataset_file)
        game.playGame()
        
        play_again = input("\nDo you want to play again? (y/n): ")
    
    print("Thank you for playing!")

     
if __name__ == "__main__":
    main()