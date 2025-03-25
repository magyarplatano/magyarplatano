import tkinter as tk
import random
import time
import pytz
from datetime import datetime

# Time zones
time_zones = {
    "UTC": "UTC",
    "New York": "America/New_York",
    "London": "Europe/London",
    "Tokyo": "Asia/Tokyo",
    "Sydney": "Australia/Sydney",
    "Budapest": "Europe/Budapest",
    "Texas": "America/Chicago",
    "Spain": "Europe/Madrid",
    "Moscow": "Europe/Moscow",
    "Kyiv": "Europe/Kiev",
    "Poland": "Europe/Warsaw",
    "Israel": "Asia/Jerusalem",
    "Germany": "Europe/Berlin",
    "Austria": "Europe/Vienna",
    "Netherlands": "Europe/Amsterdam",
    "Chile": "America/Santiago",
    "Dominican Republic": "America/Santo_Domingo",
    "Mexico": "America/Mexico_City",
    "Panama": "America/Panama",
    "Brazil": "America/Sao_Paulo",
    "Italy": "Europe/Rome",
    "Greenland": "America/Godthab",
    "Alaska": "America/Anchorage",
    "Iran": "Asia/Tehran",
    "South Korea": "Asia/Seoul",
    "China": "Asia/Shanghai",
    "Philippines": "Asia/Manila",
    "Vietnam": "Asia/Ho_Chi_Minh",
    "India": "Asia/Kolkata",
    "Pakistan": "Asia/Karachi",
    "Iraq": "Asia/Baghdad",
    "North Korea": "Asia/Pyongyang",
    "France": "Europe/Paris",
    "Sweden": "Europe/Stockholm",
    "California": "America/Los_Angeles"
}

# --- Fireworks Configuration ---
FIREWORK_CHANCE = 0.05  # Increased chance
COLORS = ["red", "orange", "yellow", "green", "blue", "purple", "white"]
FIREWORK_SPEED = 5
GRAVITY = 0.05
EXPLOSION_SIZE = 10


class FireworkParticle:
    def __init__(self, x, y, color, speed_x, speed_y):
        self.x = x
        self.y = y
        self.color = color
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.age = 0

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.speed_y += GRAVITY
        self.age += 1

    def draw(self, canvas):
        canvas.create_oval(self.x - 2, self.y - 2, self.x + 2, self.y + 2, fill=self.color, width=0, tag="firework")


# --- Main Window and Clock Code ---
root = tk.Tk()
root.title("Digital Clock with Fireworks")
root.configure(bg="black")
root.geometry("800x600")

# Canvas for fireworks (placed behind the labels)
canvas = tk.Canvas(root, bg="black", highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

label_style = {
    "font": ("Helvetica", 24),
    "bg": "black",
    "fg": "cyan",
    "padx": 20,
    "pady": 10
}

# Frame to hold the clock labels
clock_frame = tk.Frame(root, bg="black")  # Create a frame for the clocks
clock_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the frame

rows = []
for i in range(0, len(time_zones), 4):
    frame = tk.Frame(clock_frame, bg="black")
    frame.pack(side=tk.TOP, fill=tk.X, pady=5)
    rows.append(frame)


labels = {}
row_index = 0
col_index = 0

for zone in list(time_zones.keys()):
    if col_index == 4:
        row_index += 1
        col_index = 0
    try:
        labels[zone] = tk.Label(rows[row_index], **label_style)
        labels[zone].pack(side=tk.LEFT, padx=20, pady=5)
        col_index += 1
    except IndexError as e:
        print(f"Error creating label for {zone}: {e}")

fireworks = []


def create_firework():
    # More variety in the firework origin
    side = random.choice(["top", "bottom", "left", "right", "center"])
    if side == "top":
        x = random.randint(0, canvas.winfo_width())
        y = 0
    elif side == "bottom":
        x = random.randint(0, canvas.winfo_width())
        y = canvas.winfo_height()
    elif side == "left":
        x = 0
        y = random.randint(0, canvas.winfo_height())
    elif side == "right":
        x = canvas.winfo_width()
        y = random.randint(0, canvas.winfo_height())
    else:  # center
        x = random.randint(canvas.winfo_width() // 4, canvas.winfo_width() * 3 // 4) # Keep near center
        y = random.randint(canvas.winfo_height() // 4, canvas.winfo_height() * 3 // 4)


    color = random.choice(COLORS)

    particles = []
    for _ in range(random.randint(50, 150)):
        angle = random.uniform(0, 360)
        speed = random.uniform(1, FIREWORK_SPEED)
        speed_x = speed * (angle / 57.29)
        speed_y = speed * ((angle - 90) / 57.29)
        particles.append(FireworkParticle(x, y, color, speed_x, speed_y))
    return particles


def update_fireworks():
    global fireworks
    new_fireworks = []
    for particles in fireworks:
        new_particles = []
        for particle in particles:
            particle.move()
            particle.draw(canvas)
            if particle.y < canvas.winfo_height() or particle.age < 150:
                new_particles.append(particle)
        if len(new_particles) > 0:
            new_fireworks.append(new_particles)

    fireworks = new_fireworks

    if random.random() < FIREWORK_CHANCE:
        fireworks.append(create_firework())


def update_clock():
    for zone, tz in list(time_zones.items()):
        try:
            tz_time = datetime.now(pytz.timezone(tz))
            time_str = tz_time.strftime("%H:%M:%S")
            labels[zone].config(text=f"{zone}: {time_str}")
        except pytz.exceptions.UnknownTimeZoneError:
            print(f"Error: Invalid time zone: {tz}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


def update():
    canvas.delete("firework")  # Clear only the fireworks by tag. This is far more efficient!
    update_fireworks()
    update_clock()
    root.after(30, update)


# Ensure labels are created before starting the animation loop
update_clock()  # Initialize the clock display
update()

# Run the main event loop
root.mainloop()