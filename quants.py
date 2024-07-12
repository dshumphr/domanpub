import csv
from datetime import datetime, date
import os
import time
import random
import pygame
import argparse

QUANTITIES_CSV = "state/quantities.csv"
CURRENT_SESSION_CSV = "state/quantities_session.csv"
DOTS_DIR = "images/math/dots"

def load_quantities():
    quantities = {}
    if not os.path.exists(QUANTITIES_CSV):
        with open(QUANTITIES_CSV, 'w', newline='') as f:
            writer = csv.writer(f)
            for i in range(101):
                writer.writerow([i, ""])
    with open(QUANTITIES_CSV, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            quantities[int(row[0])] = datetime.strptime(row[1], "%Y-%m-%d").date() if row[1] else None
    return quantities

def save_quantities(quantities):
    with open(QUANTITIES_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        for number, last_taught in quantities.items():
            writer.writerow([number, last_taught.strftime("%Y-%m-%d") if last_taught else ""])

def load_current_session():
    session = {"set": [], "views": 0}
    if os.path.exists(CURRENT_SESSION_CSV):
        with open(CURRENT_SESSION_CSV, 'r') as f:
            reader = csv.reader(f)
            session["set"] = [int(x) for x in next(reader)]
            session["views"] = int(next(reader)[0])
    return session

def save_current_session(session):
    with open(CURRENT_SESSION_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(session["set"])
        writer.writerow([session["views"]])

def update_session(session, quantities):
    if session["views"] >= 3:
        # Remove the lowest two elements
        session["set"] = sorted(session["set"])[2:]
        
        # Add the next two elements (up to 100)
        max_current = max(session["set"]) if session["set"] else 0
        for i in range(max_current + 1, 101):
            if len(session["set"]) < 10:
                session["set"].append(i)
                quantities[i] = date.today()
            else:
                break
        
        session["views"] = 1
    else:
        session["views"] += 1
        if session["views"] > 1:
            random.shuffle(session["set"])
    
    return session, quantities

def display_session(session):
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = screen.get_size()
    pygame.display.set_caption("Quantity Learning")
    
    font = pygame.font.Font(None, 36)
    set_text = font.render(f"{session['set']}", True, (0, 0, 0))
    
    for num in session["set"]:
        image = pygame.image.load(os.path.join(DOTS_DIR, f"{num}.png"))
        aspect_ratio = 800 / 600
        image_height = screen_height - 60
        image_width = int(image_height * aspect_ratio)
        if image_width > screen_width:
            image_width = screen_width
            image_height = int(image_width / aspect_ratio)
        image = pygame.transform.scale(image, (image_width, image_height))
        x = (screen_width - image_width) // 2
        y = (screen_height - image_height) // 2
        screen.fill((255, 255, 255))  # Fill screen with white
        screen.blit(image, (x, y))
        screen.blit(set_text, (10, 10))  # Display current set in top-left corner
        pygame.display.flip()
        
        start_time = time.time()
        while time.time() - start_time < 1.25:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    return

    time.sleep(0.25)
    pygame.quit()

def run_session(rerun=False):
    quantities = load_quantities()
    session = load_current_session()

    if not rerun:
        session, quantities = update_session(session, quantities)
        save_current_session(session)
        save_quantities(quantities)

    display_session(session)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a quantity learning session.")
    parser.add_argument('--rerun', action='store_true', help='Rerun the last session without updating')
    args = parser.parse_args()
    
    run_session(args.rerun)