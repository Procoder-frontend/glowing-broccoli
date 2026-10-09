import os
import time
import random
import sys

# --- UI HELPER FUNCTIONS ---
def clear_screen():
    """Clears the terminal screen for a clean, arcade-like UI."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Prints a styled banner for the game menus."""
    print("=" * 50)
    print(f"{title.center(50)}")
    print("=" * 50)


# --- CASINO WALLET CLASS ---
class CasinoWallet:
    """Manages the player's bankroll persistently across games."""
    def __init__(self, initial_balance=1000):
        self.balance = initial_balance

    def add(self, amount):
        self.balance += amount

    def deduct(self, amount):
        if amount > self.balance:
            return False
        self.balance -= amount
        return True


# --- ROULETTE ENGINE ---
class RouletteGame:
    """Handles the American Roulette logic, bets, and animations."""
    def __init__(self, wallet):
        self.wallet = wallet
        # Numbers 1-36, 0, and 00
        self.wheel = [str(i) for i in range(1, 37)] + ["0", "00"]
        self.red_numbers = {"1", "3", "5", "7", "9", "12", "14", "16", "18", "19", "21", "23", "25", "27", "30", "32", "34", "36"}

    def get_color(self, number):
        if number in ["0", "00"]:
            return "Green"
        return "Red" if number in self.red_numbers else "Black"

    def spin_animation(self):
        """Simulates a spinning roulette ball in the terminal."""
        print("\nDropping ball into the wheel...")
        animation_frames = 20
        for i in range(animation_frames):
            simulated_pick = random.choice(self.wheel)
            color = self.get_color(simulated_pick)
            sys.stdout.write(f"\r[ SPINNING ]  ►► {color} {simulated_pick} ◄◄   ")
            sys.stdout.flush()
            # Exponential slowing effect
            time.sleep(0.05 + (i * 0.015))
        print("\n")

    def play(self):
        while True:
            clear_screen()
            print_header("🎰 AMERICAN ROULETTE WHEEL 🎰")
            print(f"Current Balance: ${self.wallet.balance}\n")
            print("1. Bet on a Specific Number (Pays 35:1)")
            print("2. Bet on Red / Black (Pays 1:1)")
            print("3. Bet on Even / Odd (Pays 1:1)")
            print("4. Return to Main Lobby")
            
            choice = input("\nSelect a bet type (1-4): ").strip()
            if choice == '4':
                break
            if choice not in ['1', '2', '3']:
                input("Invalid option. Press Enter to retry...")
                continue

            # Get Bet Amount
            try:
                bet_amount = int(input(f"Enter your bet amount (Max ${self.wallet.balance}): $"))
            except ValueError:
                input("Please enter a valid number. Press Enter...")
                continue

            if bet_amount <= 0 or not self.wallet.deduct(bet_amount):
                input("Invalid bet amount or insufficient funds. Press Enter...")
                continue

            # Process Specific Bet Rules
            bet_target = None
            if choice == '1':
                bet_target = input("Pick a number (0, 00, or 1-36): ").strip()
                if bet_target not in self.wheel:
                    print(f"Invalid wheel number. Refunding ${bet_amount}.")
                    self.wallet.add(bet_amount)
                    time.sleep(2)
                    continue
            elif choice == '2':
                bet_target = input("Choose Color (Red or Black): ").strip().capitalize()
                if bet_target not in ["Red", "Black"]:
                    print(f"Invalid color choice. Refunding ${bet_amount}.")
                    self.wallet.add(bet_amount)
                    time.sleep(2)
                    continue
            elif choice == '3':
                bet_target = input("Choose Parity (Even or Odd): ").strip().capitalize()
                if bet_target not in ["Even", "Odd"]:
                    print(f"Invalid choice. Refunding ${bet_amount}.")
                    self.wallet.add(bet_amount)
                    time.sleep(2)
                    continue

            # Spin and Evaluate
            self.spin_animation()
            winning_number = random.choice(self.wheel)
            winning_color = self.get_color(winning_number)
            
            print("-" * 50)
            print(f"🏆 WINNING OUTCOME: {winning_color} {winning_number} 🏆")
            print("-" * 50)

            won = False
            payout = 0

            if choice == '1' and winning_number == bet_target:
                won = True
                payout = bet_amount * 36 
            elif choice == '2' and winning_color == bet_target:
                won = True
                payout = bet_amount * 2
            elif choice == '3' and winning_number not in ["0", "00"]:
                num_int = int(winning_number)
                if bet_target == "Even" and num_int % 2 == 0:
                    won = True
                elif bet_target == "Odd" and num_int % 2 != 0:
                    won = True
                if won:
                    payout = bet_amount * 2

            if won:
                print(f"🎉 Congratulations! You won ${payout}!")
                self.wallet.add(payout)
            else:
                print("💸 House wins! Better luck next spin.")

            print(f"\nNew Balance: ${self.wallet.balance}")
            if input("\nSpin again? (y/n): ").lower() != 'y':
                break


# --- SLOT MACHINE ENGINE ---
class SlotMachineGame:
    """Manages a 3x3 multi-line slot matrix with probability weights."""
    def __init__(self, wallet):
        self.wallet = wallet
        # Symbols, Weights, and Multipliers
        self.symbols = {
            "🍒": {"weight": 40, "payout": 2},   # Common
            "🍊": {"weight": 25, "payout": 5},   # Medium
            "🍋": {"weight": 18, "payout": 10},  # Rare
            "💎": {"weight": 5,  "payout": 50}   # Ultra Rare
        }
        # Flattened list for random.choice selection matching weights
        self.pool = []
        for sym, data in self.symbols.items():
            self.pool.extend([sym] * data["weight"])

    def generate_matrix(self):
        """Builds a 3x3 matrix representing the slot view."""
        return [[random.choice(self.pool) for _ in range(3)] for _ in range(3)]

    def print_matrix(self, matrix):
        """Displays the 3x3 slot layout cleanly."""
        print("\n\t+---+---+---+")
        for row in matrix:
            print(f"\t| {' | '.join(row)} |")
            print("\t+---+---+---+")
        print("\n")

    def spin_animation(self):
        """Generates a scrolling effect inside the terminal grid."""
        for i in range(12):
            clear_screen()
            print_header("🎰 NEON LIGHTS 3X3 SLOTS 🎰")
            print(f"Wallet Balance: ${self.wallet.balance}\n")
            print("Spinning Reels...")
            self.print_matrix(self.generate_matrix())
            time.sleep(0.05 + (i * 0.03))

    def play(self):
        while True:
            clear_screen()
            print_header("🎰 NEON LIGHTS 3X3 SLOTS 🎰")
            print(f"Current Balance: ${self.wallet.balance}\n")
            print("Paylines Available:")
            print("• Lines 1-3: Horizontal Rows")
            print("• Lines 4-5: Diagonals\n")

            try:
                lines = int(input("How many lines to bet on (1-5): "))
                if lines < 1 or lines > 5:
                    raise ValueError
                
                bet_per_line = int(input("Enter bet per line: $"))
                total_bet = lines * bet_per_line
            except ValueError:
                input("Invalid numbers. Press Enter to retry...")
                continue

            if total_bet <= 0 or not self.wallet.deduct(total_bet):
                input(f"Insufficient funds for a total bet of ${total_bet}. Press Enter...")
                continue

            # Run Matrix Generation
            self.spin_animation()
            matrix = self.generate_matrix()
            
            clear_screen()
            print_header("🎰 SLOT RESULT 🎰")
            print(f"Total Bet Placed: ${total_bet}")
            self.print_matrix(matrix)

            # Define matrix check coordinate patterns
            # Format: (Line Index label, list of (row, col) tuples)
            payline_paths = [
                (1, [(0,0), (0,1), (0,2)]),  # Row 1
                (2, [(1,0), (1,1), (1,2)]),  # Row 2
                (3, [(2,0), (2,1), (2,2)]),  # Row 3
                (4, [(0,0), (1,1), (2,2)]),  # Diagonal Top-Left to Bottom-Right
                (5, [(2,0), (1,1), (0,2)])   # Diagonal Bottom-Left to Top-Right
            ]

            total_won = 0
            lines_hit = []

            # Evaluate only up to active selected lines
            for i in range(lines):
                line_id, path = payline_paths[i]
                symbols_on_line = [matrix[r][c] for r, c in path]

                # Check if all 3 elements in the path match
                if len(set(symbols_on_line)) == 1:
                    match_symbol = symbols_on_line[0]
                    multiplier = self.symbols[match_symbol]["payout"]
                    win_amount = bet_per_line * multiplier
                    total_won += win_amount
                    lines_hit.append((line_id, match_symbol, win_amount))

            # Resolution Output
            if lines_hit:
                print("🎉 WINNING LINES:")
                for l_id, sym, amt in lines_hit:
                    print(f"  ➜ Line {l_id} matched {sym}! Won: ${amt}")
                self.wallet.add(total_won)
                print(f"\nNet Return: +${total_won}")
            else:
                print("💸 No matches. Better luck next spin!")

            print(f"Updated Balance: ${self.wallet.balance}")
            if input("\nSpin again? (y/n): ").lower() != 'y':
                break


