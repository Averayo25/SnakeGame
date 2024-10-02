import tkinter as tk
import random

CELL_SIZE = 20
GAME_WIDTH = 30
GAME_HEIGHT = 20

class SnakeGame:
    def __init__(self, frame):
        self.canvas = tk.Canvas(frame, width=GAME_WIDTH * CELL_SIZE, height=GAME_HEIGHT * CELL_SIZE, bg="black")
        self.canvas.pack()

        self.score = 0
        self.high_score = 0
        
        score_frame = tk.Frame(frame, bg="white")
        score_frame.pack(side=tk.TOP, anchor="nw", padx=10, pady=5)
        
        self.score_label = tk.Label(score_frame, text=f"Score: {self.score}", font=("Arial", 14), bg="white", fg="black")
        self.score_label.pack(side=tk.LEFT)

        self.spacer_label = tk.Label(score_frame, text="                                                                                                             ", bg="white")
        self.spacer_label.pack(side=tk.LEFT)

        self.high_score_label = tk.Label(score_frame, text=f"High Score: {self.high_score}", font=("Arial", 14), bg="white", fg="black")
        self.high_score_label.pack(side=tk.RIGHT)

        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.direction = "Right"
        self.food = None
        self.is_game_over = False

        self.create_food()
        self.move_speed = 100
        self.speed_increment_score_threshold = 20

        frame.bind_all("<KeyPress>", self.on_key_press)

        self.title_label = tk.Label(frame, text="Snake Game", font=("Helvetica", 48, "bold"), bg="white", fg="#00FF00")
        self.title_label.place(x=(GAME_WIDTH * CELL_SIZE) // 2 - 100, y=(GAME_HEIGHT * CELL_SIZE) // 2 - 100)
        
        self.canvas.create_text(GAME_WIDTH * CELL_SIZE // 2 - 2, GAME_HEIGHT * CELL_SIZE // 2 - 102, text="Snake Game", fill="#004400", font=("Helvetica", 48, "bold"), tags="shadow")
        
        self.subtitle_label = tk.Label(frame, text="by Averayo", font=("Helvetica", 20), bg="white", fg="#A9A9A9")
        self.subtitle_label.place(x=(GAME_WIDTH * CELL_SIZE) // 2 - 50, y=(GAME_HEIGHT * CELL_SIZE) // 2 - 50)

        self.start_button = tk.Button(frame, text="Play", command=self.start_game, font=("Arial", 14), width=10, bg="#008CBA", fg="white", activebackground="#005f6b", activeforeground="white")
        self.start_button.place(x=(GAME_WIDTH * CELL_SIZE) // 2 - 50, y=(GAME_HEIGHT * CELL_SIZE) // 2 + 20)

        # Define a list of colors for the explosion effect
        self.colors = ["white", "lightgray", "lightblue", "lightgreen", "lightpink", "yellow", "orange", "purple"]

    def start_game(self):
        self.start_button.place_forget()
        self.title_label.place_forget()
        self.subtitle_label.place_forget()
        self.canvas.delete("shadow")
        self.move_snake()
    
    def create_food(self):
        if self.food:
            self.canvas.delete("food")

        while True:
            self.food = (random.randint(0, GAME_WIDTH - 1), random.randint(0, GAME_HEIGHT - 1))
            if self.food not in self.snake:
                break

        self.draw_food()
    
    def draw_food(self):
        x, y = self.food
        self.canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill="red", tags="food")

    def draw_snake(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill="green", tags="snake")

    def move_snake(self):
        if self.is_game_over:
            return

        head_x, head_y = self.snake[0]
        if self.direction == "Left":
            head_x -= 1
        elif self.direction == "Right":
            head_x += 1
        elif self.direction == "Up":
            head_y -= 1
        elif self.direction == "Down":
            head_y += 1

        if (head_x, head_y) in self.snake or head_x < 0 or head_x >= GAME_WIDTH or head_y < 0 or head_y >= GAME_HEIGHT:
            self.game_over()
            return

        self.snake.insert(0, (head_x, head_y))

        if (head_x, head_y) == self.food:
            self.score += 10
            self.update_score()
            self.create_food()
            if self.score % self.speed_increment_score_threshold == 0:
                self.move_speed = max(50, self.move_speed - 5)
        else:
            self.snake.pop()

        self.draw_snake()
        self.canvas.after(self.move_speed, self.move_snake)

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_label.config(text=f"High Score: {self.high_score}")

    def on_key_press(self, event):
        if self.is_game_over:
            self.restart_game()
            return

        new_direction = event.keysym
        if (new_direction == "Left" and self.direction != "Right") or \
           (new_direction == "Right" and self.direction != "Left") or \
           (new_direction == "Up" and self.direction != "Down") or \
           (new_direction == "Down" and self.direction != "Up"):
            self.direction = new_direction

    def explode(self, x, y):
        explosion_effects = []
        for i in range(15):  # Create 15 explosion circles for more variation
            radius = random.randint(10, 30)  # Wider range for radius
            # Randomly displace the smoke for a more natural effect
            displacement_x = random.randint(-5, 5)
            displacement_y = random.randint(-5, 5)
            color = random.choice(self.colors)  # Select a random color for each puff
            explosion_circle = self.canvas.create_oval(
                x - radius + displacement_x, y - radius + displacement_y, 
                x + radius + displacement_x, y + radius + displacement_y,
                fill=color, outline="", tags="explosion"
            )
            explosion_effects.append(explosion_circle)

        # Animate the explosion effects with varying opacities and durations
        for i in range(len(explosion_effects)):
            self.canvas.after(i * 50, lambda idx=i: self.expand_explosion(explosion_effects[idx], random.uniform(0.3, 1.0)))

    def expand_explosion(self, explosion_circle, opacity):
        # Change the fill color and size to simulate fading out
        self.canvas.itemconfig(explosion_circle, fill="", outline="")
        self.canvas.scale(explosion_circle, 0, 0, 1.5, 1.5)  # Increase size
        # Adjust the duration before removal based on opacity
        self.canvas.after(int(opacity * 200), lambda: self.canvas.delete(explosion_circle))  # Remove after some time

    def game_over(self):
        self.is_game_over = True

        # Get head position for explosion
        head_x, head_y = self.snake[0]
        self.explode(head_x * CELL_SIZE + CELL_SIZE // 2, head_y * CELL_SIZE + CELL_SIZE // 2)  # Center explosion

        self.canvas.create_text(GAME_WIDTH * CELL_SIZE // 2, GAME_HEIGHT * CELL_SIZE // 2, 
                                 text="GAME OVER", fill="white", font=("Arial", 24), tags="gameover")
        self.canvas.create_text(GAME_WIDTH * CELL_SIZE // 2, GAME_HEIGHT * CELL_SIZE // 2 + 30, 
                                 text="Press any key to restart", fill="white", font=("Arial", 16), tags="gameover")

    def restart_game(self):
        self.canvas.delete("snake")
        self.canvas.delete("food")
        self.canvas.delete("explosion")
        self.canvas.delete("gameover")
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.direction = "Right"
        self.is_game_over = False
        self.score = 0
        self.move_speed = 100
        self.update_score()
        self.create_food()
        self.move_snake()

def main():
    root = tk.Tk()
    root.title("Python Game by: Averayo")
    desired_width = 900
    desired_height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = min(desired_width, screen_width)
    window_height = min(desired_height, screen_height)
    position_x = int((screen_width / 2) - (window_width / 2))
    position_y = int((screen_height / 2) - (window_height / 2))
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
    border_frame = tk.Frame(root, borderwidth=5, relief="solid")
    border_frame.pack(padx=10, pady=10, expand=True)
    game = SnakeGame(border_frame)
    root.mainloop()

if __name__ == "__main__":
    main()
