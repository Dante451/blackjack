import sys
import random
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QDialog
from PySide6.QtCore import Qt

# Card deck creation and handling
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
CARD_VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

class StatisticsWindow(QDialog):
    def __init__(self, wins, losses, last_games):
        super().__init__()
        
        self.setWindowTitle("Game Statistics")
        
        layout = QVBoxLayout()
        
        # Display win/loss ratio
        win_loss_ratio = f"Win/Loss Ratio: {wins}/{losses} ({wins / (wins + losses) if (wins + losses) > 0 else 0:.2f})"
        self.win_loss_label = QLabel(win_loss_ratio)
        layout.addWidget(self.win_loss_label)
        
        # Display results of the last 5 games
        self.last_games_label = QLabel("Results of Last 5 Games:")
        layout.addWidget(self.last_games_label)
        
        last_games_text = "\n".join([f"Game {i+1}: {result}" for i, result in enumerate(last_games)])
        self.last_games_display = QLabel(last_games_text)
        layout.addWidget(self.last_games_display)
        
        # Close button
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)
        
        self.setLayout(layout)

class RulesWindow(QDialog):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Game Rules")
        
        layout = QVBoxLayout()
        
        self.rules_label = QLabel("Blackjack Rules:\n\n- Aim to get a hand total of 21 or as close as possible.\n"
                                   "- Face cards (J, Q, K) are worth 10 points.\n- Aces are worth 1 or 11 points.\n"
                                   "- The player and dealer are each dealt two cards.\n"
                                   "- The player can choose to 'Hit' to take another card or 'Stand' to keep their hand.\n"
                                   "- The dealer must 'Hit' if their total is below 17 and 'Stand' if it is 17 or higher.")
        layout.addWidget(self.rules_label)
        
        # Close button
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)
        
        self.setLayout(layout)

class IntroScreen(QWidget):
    def __init__(self, game_window):
        super().__init__()
        
        self.game_window = game_window  # Reference to the main Blackjack game window
        
        # Set up Introductory Screen UI
        self.setWindowTitle("Welcome to Blackjack!")
        
        layout = QVBoxLayout()
        
        # Title label
        self.title_label = QLabel("Welcome to the Blackjack Game!")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)
        
        # Description label
        self.desc_label = QLabel("Learn how to play and try your luck!")
        self.desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.desc_label)

        # Version label
        self.vers_label = QLabel("The current version is v1.4")
        self.vers_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.vers_label)
        
        # Start button
        self.start_button = QPushButton("Start Game")
        self.start_button.clicked.connect(self.start_game)
        layout.addWidget(self.start_button)
        
        # View Rules button
        self.view_rules_button = QPushButton("View Rules")
        self.view_rules_button.clicked.connect(self.view_rules)
        layout.addWidget(self.view_rules_button)
        
        self.setLayout(layout)
        
    def start_game(self):
        """Hide the intro screen and show the main game."""
        self.hide()  # Hide the Intro Screen
        self.game_window.show()  # Show the main Blackjack game window
    
    def view_rules(self):
        """Show the rules window."""
        self.rules_window = RulesWindow()  # Create an instance of the Rules window
        self.rules_window.show()  # Show the rules window

class BlackjackGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blackjack Game")
        
        # Initialize game state and counters
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.player_total = 0
        self.dealer_total = 0
        self.wins = 0
        self.losses = 0
        self.last_games = []  # Store results of last 5 games
        
        # Create the UI components
        self.init_ui()
        
    def init_ui(self):
        self.layout = QVBoxLayout()
        
        # Display area
        self.status_label = QLabel("Welcome to Blackjack!")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label)
        
        # Player and dealer hand labels
        self.player_label = QLabel("Your hand: ")
        self.dealer_label = QLabel("Dealer's hand: ")
        self.layout.addWidget(self.player_label)
        self.layout.addWidget(self.dealer_label)
        
        # Win and Loss counters
        self.win_label = QLabel(f"Wins: {self.wins}")
        self.loss_label = QLabel(f"Losses: {self.losses}")
        self.layout.addWidget(self.win_label)
        self.layout.addWidget(self.loss_label)
        
        # Button layout
        self.button_layout = QHBoxLayout()
        self.hit_button = QPushButton("Hit")
        self.stand_button = QPushButton("Stand")
        self.play_again_button = QPushButton("Play Again")
        self.statistics_button = QPushButton("Statistics")
        
        self.hit_button.clicked.connect(self.hit)
        self.stand_button.clicked.connect(self.stand)
        self.play_again_button.clicked.connect(self.play_again)
        self.statistics_button.clicked.connect(self.show_statistics)  # New connection to statistics window
        
        self.button_layout.addWidget(self.hit_button)
        self.button_layout.addWidget(self.stand_button)
        self.button_layout.addWidget(self.play_again_button)
        self.button_layout.addWidget(self.statistics_button)  # Add the Statistics button
        
        self.layout.addLayout(self.button_layout)
        
        # Initially hide the Play Again button
        self.play_again_button.setHidden(True)
        
        # Reset the game
        self.reset_game()
        
        self.setLayout(self.layout)
        
    def create_deck(self):
        """Create and shuffle the deck."""
        deck = [f'{value} of {suit}' for suit in SUITS for value in VALUES]
        random.shuffle(deck)
        return deck

    def reset_game(self):
        """Reset the game to initial state."""
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.player_total = 0
        self.dealer_total = 0
        
        # Deal initial cards
        self.player_hand.append(self.deck.pop())
        self.dealer_hand.append(self.deck.pop())
        self.player_hand.append(self.deck.pop())
        self.dealer_hand.append(self.deck.pop())
        
        # Calculate totals immediately after dealing
        self.player_total = self.calculate_hand_total(self.player_hand)
        self.dealer_total = self.calculate_hand_total(self.dealer_hand)
        
        # Update the UI to show both hands' totals
        self.update_ui()

    def update_ui(self):
        """Update the UI labels with the current hands and totals."""
        self.player_label.setText(f"Your hand: {', '.join(self.player_hand)} (Total: {self.player_total})")
        self.dealer_label.setText(f"Dealer's hand: {self.dealer_hand[0]}, ? (Total: ?)")
        
        # Update the game state
        if self.player_total > 21:
            self.status_label.setText("You busted! Game Over.")
            self.losses += 1
            self.last_games.append("Loss")
            self.end_game()
        elif self.dealer_total > 21:
            self.status_label.setText("Dealer busted! You win!")
            self.wins += 1
            self.last_games.append("Win")
            self.end_game()
        elif self.player_total == 21:
            self.status_label.setText("Blackjack! You win!")
            self.wins += 1
            self.last_games.append("Win")
            self.end_game()
        else:
            self.status_label.setText("Your turn! Choose hit or stand.")
        
        # Update the win/loss counters
        self.win_label.setText(f"Wins: {self.wins}")
        self.loss_label.setText(f"Losses: {self.losses}")
        
        # Keep the last 5 game results
        if len(self.last_games) > 5:
            self.last_games.pop(0)

    def calculate_hand_total(self, hand):
        """Calculate the total value of a hand."""
        total = 0
        aces = 0
        for card in hand:
            value = card.split()[0]
            total += CARD_VALUES[value]
            if value == 'A':
                aces += 1
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total
    
    def hit(self):
        """Player hits and draws a card."""
        self.player_hand.append(self.deck.pop())
        self.player_total = self.calculate_hand_total(self.player_hand)
        self.update_ui()

    def stand(self):
        """Player stands. Dealer plays."""
        self.dealer_label.setText(f"Dealer's hand: {', '.join(self.dealer_hand)} (Total: {self.dealer_total})")
        
        while self.dealer_total < 17:
            self.dealer_hand.append(self.deck.pop())
            self.dealer_total = self.calculate_hand_total(self.dealer_hand)
        
        self.update_ui()
        
        if self.player_total > 21:
            self.status_label.setText("You busted! Game Over.")
            self.losses += 1  # Ensure loss is registered here
            self.last_games.append("Loss")
        elif self.dealer_total > 21:
            self.status_label.setText("Dealer busted! You win!")
            self.wins += 1  # Ensure win is registered here
            self.last_games.append("Win")
        elif self.player_total > self.dealer_total:
            self.status_label.setText("You win!")
            self.wins += 1
            self.last_games.append("Win")
        elif self.player_total < self.dealer_total:
            self.status_label.setText("Dealer wins!")
            self.losses += 1
            self.last_games.append("Loss")
        else:
            self.status_label.setText("It's a tie!")
        
        self.end_game()
        
    def end_game(self):
        """End the game and show the Play Again button.""" 
        self.hit_button.setDisabled(True)
        self.stand_button.setDisabled(True)
        self.play_again_button.setVisible(True)

    def play_again(self):
        """Reset the game for a new round.""" 
        self.play_again_button.setHidden(True)
        self.reset_game()
        self.hit_button.setEnabled(True)
        self.stand_button.setEnabled(True)

    def show_statistics(self):
        """Show the statistics window."""
        _window = StatisticsWindow(self.wins, self.losses, self.last_games)
        _window.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create the main Blackjack game window
    game_window = BlackjackGame()
    
    # Create the intro screen and pass the game window to it
    intro_screen = IntroScreen(game_window)
    
    # Show the intro screen first
    intro_screen.show()
    
    sys.exit(app.exec())