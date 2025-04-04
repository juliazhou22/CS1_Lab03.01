import os


class HighScoreManager:
    """Manages high scores for the game"""

    def __init__(self, filename="high_scores.txt", max_scores=10):
        """Initialize the high score manager

        Args:
            filename (str): Name of the file to store high scores
            max_scores (int): Maximum number of high scores to keep
        """
        self.filename = filename
        self.max_scores = max_scores
        self.scores = []
        self.load_scores()

    def load_scores(self):
        """Load high scores from file"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    for line in file:
                        # Each line format: name,score
                        parts = line.strip().split(',')
                        if len(parts) == 2:
                            name = parts[0]
                            try:
                                score = int(parts[1])
                                self.scores.append((name, score))
                            except ValueError:
                                # Skip invalid scores
                                pass

                # Sort scores (highest first)
                self.scores.sort(key=lambda x: x[1], reverse=True)

                # Trim to max_scores
                self.scores = self.scores[:self.max_scores]
            else:
                print(f"No high score file found. Will create one when saving scores.")
        except Exception as e:
            print(f"Error loading high scores: {e}")
            # Start with empty scores if there's an error
            self.scores = []

    def save_scores(self):
        """Save high scores to file"""
        try:
            with open(self.filename, 'w') as file:
                for name, score in self.scores:
                    file.write(f"{name},{score}\n")
            print(f"High scores saved to {self.filename}")
        except Exception as e:
            print(f"Error saving high scores: {e}")

    def add_score(self, name, score):
        """Add a new score to the high scores list

        Args:
            name (str): Player name
            score (int): Player score

        Returns:
            bool: True if score made it to the high scores, False otherwise
            int: Position in the high scores (0-based, -1 if not in high scores)
        """
        # Check if score is high enough to make the list
        if len(self.scores) < self.max_scores or score > self.scores[-1][1]:
            # Add the new score
            self.scores.append((name, score))

            # Sort scores (highest first)
            self.scores.sort(key=lambda x: x[1], reverse=True)

            # Trim to max_scores
            self.scores = self.scores[:self.max_scores]

            # Save updated scores
            self.save_scores()

            # Find position of the new score
            for i, (n, s) in enumerate(self.scores):
                if n == name and s == score:
                    return True, i

            return True, -1  # Should not happen

        return False, -1

    def is_high_score(self, score):
        """Check if a score qualifies for the high scores list

        Args:
            score (int): Score to check

        Returns:
            bool: True if score qualifies, False otherwise
        """
        return len(self.scores) < self.max_scores or score > self.scores[-1][1]

    def get_scores(self):
        """Get the current high scores

        Returns:
            list: List of (name, score) tuples
        """
        return self.scores.copy()