import tkinter as tk
import random
from PIL import Image, ImageTk


class DontClickGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("My First Game")
        self.root.geometry("400x300")

        self.clicks = 0

        self.label = tk.Label(
            self.root,
            text="Don't click the button!",
            font=("Arial", 16)
        )
        self.label.pack(pady=20)

        self.button = tk.Button(
            self.root,
            text="Don't click me",
            command=self.main_button_pressed
        )
        self.button.pack()

        self.root.mainloop()

    # ---------------- MAIN WINDOW ----------------
    def main_button_pressed(self):
        self.clicks += 1

        if self.clicks == 1:
            self.root.config(bg="red")
            self.label.config(text="I said don't!", bg="red")

        elif self.clicks == 2:
            self.label.config(text="Last warning...")

        elif self.clicks == 3:
            self.root.destroy()
            self.open_second_window()

    # ---------------- SECOND WINDOW ----------------
    def open_second_window(self):
        self.second = tk.Toplevel()
        self.second.title("I am tired of being good")
        self.second.geometry("400x300")

        self.second_clicks = 0

        self.moving_button = tk.Button(
            self.second,
            text="Now it's not simple 😈",
            command=self.second_button_pressed
        )
        self.moving_button.place(x=120, y=120)

    def second_button_pressed(self):
        self.second_clicks += 1

        if self.second_clicks == 1:
            tk.Label(self.second, text="lol", font=("Arial", 16)).place(x=185, y=10)

        elif self.second_clicks == 20:
            self.second.destroy()
            self.open_boss_window()
            return

        x = random.randint(50, 300)
        y = random.randint(50, 220)
        self.moving_button.place(x=x, y=y)

    # ---------------- BOSS WINDOW ----------------
    def open_boss_window(self):
        self.boss_window = tk.Toplevel()
        self.boss_window.title("Boss Fight")
        self.boss_window.geometry("400x300")

        # Player stats
        self.player_max_hp = 100
        self.player_hp = 100

        # Boss stats
        self.boss_max_hp = 500
        self.boss_hp = 150
        self.rage_mode = False

        # Player health bar
        self.player_canvas = tk.Canvas(self.boss_window, width=300, height=20)
        self.player_canvas.place(x=50, y=20)
        self.player_canvas.create_rectangle(0, 0, 300, 20, fill="gray")
        self.player_bar = self.player_canvas.create_rectangle(
            0, 0, 300, 20, fill="green"
        )
        self.player_canvas.create_text(150, 10, text="PLAYER HP", fill="white")

        # Boss health bar
        self.boss_canvas = tk.Canvas(self.boss_window, width=300, height=20)
        self.boss_canvas.place(x=50, y=50)
        self.boss_canvas.create_rectangle(0, 0, 300, 20, fill="gray")
        self.boss_bar = self.boss_canvas.create_rectangle(
            0, 0, 300, 20, fill="red"
        )
        self.boss_canvas.create_text(150, 10, text="BOSS HP", fill="white")

        # Load boss image
        image = Image.open("boss.png").resize((140, 140))
        self.boss_image = ImageTk.PhotoImage(image)

        self.boss_button = tk.Button(
            self.boss_window,
            image=self.boss_image,
            command=self.attack_boss
        )
        self.boss_button.place(x=130, y=90)

        # Start boss attacking
        self.boss_attack_loop()

    # ---------------- PLAYER ATTACK ----------------
    def attack_boss(self):
        damage = random.randint(8, 15)

        if self.rage_mode:
            damage -= 4  # boss harder to damage

        self.boss_hp -= damage
        self.boss_hp = max(self.boss_hp, 0)
        self.update_boss_bar()

        if self.boss_hp <= self.boss_max_hp * 0.3:
            self.rage_mode = True

        if self.boss_hp == 0:
            self.win_game()

    # ---------------- BOSS ATTACK LOOP ----------------
    def boss_attack_loop(self):
        if self.player_hp <= 0 or self.boss_hp <= 0:
            return

        # Boss damage increases in rage mode
        damage = random.randint(5, 10) if not self.rage_mode else random.randint(10, 18)
        self.player_hp -= damage
        self.player_hp = max(self.player_hp, 0)
        self.update_player_bar()

        if self.player_hp == 0:
            self.game_over()
            return

        # Attack speed increases in rage mode
        delay = 1200 if not self.rage_mode else 700
        self.boss_window.after(delay, self.boss_attack_loop)

    # ---------------- UPDATE BARS ----------------
    def update_player_bar(self):
        width = int(300 * (self.player_hp / self.player_max_hp))
        self.player_canvas.coords(self.player_bar, 0, 0, width, 20)

    def update_boss_bar(self):
        width = int(300 * (self.boss_hp / self.boss_max_hp))
        self.boss_canvas.coords(self.boss_bar, 0, 0, width, 20)

    # ---------------- END STATES ----------------
    def game_over(self):
        self.boss_button.config(state="disabled")
        tk.Label(
            self.boss_window,
            text="GAME OVER ☠️",
            font=("Arial", 20),
            fg="red"
        ).place(x=120, y=240)

    def win_game(self):
        self.boss_button.config(state="disabled")
        tk.Label(
            self.boss_window,
            text="YOU WIN 🏆",
            font=("Arial", 20),
            fg="green"
        ).place(x=135, y=240)


# ---------------- RUN GAME ----------------
if __name__ == "__main__":
    DontClickGame()
