import sys
import random
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PySide6.QtCore import Qt

# Card deck creation and handling
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
CARD_VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

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
        self.play_again_button = QPushButton("Play Again")  # Added Play Again button
        self.hit_button.clicked.connect(self.hit)
        self.stand_button.clicked.connect(self.stand)
        self.play_again_button.clicked.connect(self.play_again)  # Play Again button callback
        
        self.button_layout.addWidget(self.hit_button)
        self.button_layout.addWidget(self.stand_button)
        self.button_layout.addWidget(self.play_again_button)  # Add to the layout
        
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
        
        # Show one card of the dealer's hand initially
        self.dealer_label.setText(f"Dealer's hand: {self.dealer_hand[0]}, ? (Total: ?)")

        # Update the game state
        if self.player_total > 21:
            self.status_label.setText("You busted! Game Over.")
            self.losses += 1
            self.end_game()
        elif self.dealer_total > 21:
            self.status_label.setText("Dealer busted! You win!")
            self.wins += 1
            self.end_game()
        elif self.player_total == 21:
            self.status_label.setText("Blackjack! You win!")
            self.wins += 1
            self.end_game()
        else:
            self.status_label.setText("Your turn! Choose hit or stand.")
        
        # Update the win/loss counters
        self.win_label.setText(f"Wins: {self.wins}")
        self.loss_label.setText(f"Losses: {self.losses}")
        
    def calculate_hand_total(self, hand):
        """Calculate the total value of a hand."""
        total = 0
        aces = 0
        for card in hand:
            value = card.split()[0]
            total += CARD_VALUES[value]
            if value == 'A':
                aces += 1
        # Adjust for aces
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
        # Reveal dealer's second card
        self.dealer_label.setText(f"Dealer's hand: {', '.join(self.dealer_hand)} (Total: {self.dealer_total})")
        
        # Dealer's turn (dealer hits until they have at least 17)
        while self.dealer_total < 17:
            self.dealer_hand.append(self.deck.pop())
            self.dealer_total = self.calculate_hand_total(self.dealer_hand)
        
        self.update_ui()
        
        if self.player_total > 21:
            self.status_label.setText("You busted! Game Over.")
            self.losses += 1
        elif self.dealer_total > 21:
            self.status_label.setText("Dealer busted! You win!")
            self.wins += 1
        elif self.player_total > self.dealer_total:
            self.status_label.setText("You win!")
            self.wins += 1
        elif self.player_total < self.dealer_total:
            self.status_label.setText("Dealer wins!")
            self.losses += 1
        else:
            self.status_label.setText("It's a tie!")
        
        self.end_game()
        
    def end_game(self):
        """End the game and show the Play Again button."""
        # Disable the game action buttons
        self.hit_button.setDisabled(True)
        self.stand_button.setDisabled(True)
        
        # Show the Play Again button
        self.play_again_button.setVisible(True)

    def play_again(self):
        """Reset the game for a new round."""
        self.play_again_button.setHidden(True)  # Hide the Play Again button
        self.reset_game()  # Reset the game to the initial state
        self.hit_button.setEnabled(True)  # Enable the action buttons
        self.stand_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BlackjackGame()
    window.show()
    sys.exit(app.exec())
