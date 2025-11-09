class Board:
    def __init__(self):
        """Initialize"""
        self.c = [[" ", " ", " "],
                  [" ", " ", " "],
                  [" ", " ", " "]]
      
    def printBoard(self):
        # Print the header showing column indices
        BOARD_HEADER = "-----------------\n|R\\C| 0 | 1 | 2 |\n-----------------"
        print(BOARD_HEADER)

        # Print each row with its index
        for i in range(3):
            print(f"| {i} | {self.c[i][0]} | {self.c[i][1]} | {self.c[i][2]} |")
            print("-----------------")

    
class Game:

    def __init__(self):
        self.board = Board()
        self.turn = 'X'

    def switchPlayer(self):
        if self.turn == 'X':
            self.turn = 'O'
        else:
            self.turn = 'X'
    
    def validateEntry(self, row, col):
        """
        Validate if the user's move is legal.
        """
        # Check if indices are within valid range
        if row < 0 or row > 2 or col < 0 or col > 2:
            return False
        
        # Check if the cell is empty
        if self.board.c[row][col] != " ":
            return False
        
        return True

    def checkFull(self):
        """
        Check if the board is completely filled.
        """
        for i in range(3):
            for j in range(3):
                if self.board.c[i][j] == " ":
                    return False
        return True
    
    def checkWin(self):
        """
        Check if there is a winner in the current board state.
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
        
        # Check diagonal (top-left to bottom-right)
        if (self.board.c[0][0] == self.board.c[1][1] == self.board.c[2][2] 
            and self.board.c[0][0] != " "):
            return True
        
        # Check diagonal (top-right to bottom-left)
        if (self.board.c[0][2] == self.board.c[1][1] == self.board.c[2][0] 
            and self.board.c[0][2] != " "):
            return True
        
        return False
    
    def checkEnd(self):
        """
        Check if the game has reached an end condition.
        """
        # Check if there's a winner
        if self.checkWin():
            print(f"Player {self.turn} wins!")
            return True
        
        # Check if board is full (draw)
        if self.checkFull():
            print("DRAW! NOBODY WINS!")
            return True
        
        return False

    def playGame(self):
        print("\n=== Welcome to Tic-Tac-Toe ===\n")
        
        # Game loop continues until the game ends
        while True:
            # Display the current board
            self.board.printBoard()
            
            # Prompt current player for their move
            print(f"\nPlayer {self.turn}'s turn")
            
            # Get and validate user input
            while True:
                try:
                    row = int(input("Enter row (0-2): "))
                    col = int(input("Enter column (0-2): "))
                    
                    # Validate the entry
                    if self.validateEntry(row, col):
                        break
                    else:
                        print("Invalid move! Cell is either occupied or out of range. Try again.")
                except ValueError:
                    print("Invalid input! Please enter numbers between 0 and 2.")
            
            # Place the mark on the board
            self.board.c[row][col] = self.turn
            
            # Check if the game has ended
            if self.checkEnd():
                # Display final board
                self.board.printBoard()
                break
            
            # Switch to the other player
            self.switchPlayer()


def main():
    # Variable to control game repetition
    play_again = 'y'

    # Loop to allow multiple games
    while play_again.lower() == 'y':
        # Create a new game instance
        game = Game()
        
        # Play the game
        game.playGame()
        
        # Ask if players want to play again
        play_again = input("\nDo you want to play again? (y/n): ")
    
    # Goodbye message
    print("Thank you for playing!")

    
if __name__ == "__main__":
    main()