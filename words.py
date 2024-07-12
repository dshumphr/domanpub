import csv
from datetime import datetime, date
import os
import time
import random
import pygame
import argparse
import hashlib
import json

WORDS_CSV = "state/words.csv"
LAST_SESSION_FILE = "state/words_session.json"

def load_word_sets():
    word_sets = []
    if not os.path.exists(WORDS_CSV):
        print("Failed to find words")
        exit(0)
    with open(WORDS_CSV, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            word_sets.append({
                "name": row[0],
                "words": row[1:6],
                "views": int(row[6])
            })
    return word_sets

def save_word_sets(word_sets):
    with open(WORDS_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        for set_data in word_sets:
            writer.writerow([set_data["name"]] + set_data["words"] + [str(set_data["views"])])

def get_word_set(word_sets, increment_views=True):
    eligible_sets = [s for s in word_sets if s["views"] < 15]
    if len(eligible_sets) > 5:
        eligible_sets = eligible_sets[:5]
    if len(eligible_sets) == 0:
        print("No sets left!")
        return None

    chosen_set = random.choice(eligible_sets)
    if increment_views:
        chosen_set["views"] += 1
    return chosen_set

def display_session(chosen_set):
    pygame.init()
    screen = pygame.display.set_mode((1600, 900), pygame.FULLSCREEN|pygame.SCALED)
    screen_width, screen_height = screen.get_size()
    pygame.display.set_caption("Word Learning")
    
    font = pygame.font.Font(None, 300)  # Increased font size
    
    words = chosen_set["words"]
    set_text = pygame.font.Font(None, 72).render(f"{chosen_set['name']}", True, (0, 0, 0))
    random.shuffle(words)

    for word in words:
        text_surface = font.render(word.upper(), True, (255, 0, 0))  # Display in all caps
        text_rect = text_surface.get_rect(center=(screen_width/2, screen_height/2))
        
        screen.fill((255, 255, 255))
        screen.blit(text_surface, text_rect)
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

def save_last_session(chosen_set):
    with open(LAST_SESSION_FILE, 'w') as f:
        json.dump(chosen_set, f)

def load_last_session():
    if os.path.exists(LAST_SESSION_FILE):
        with open(LAST_SESSION_FILE, 'r') as f:
            return json.load(f)
    return None

def run_session(rerun=False):
    word_sets = load_word_sets()

    if rerun:
        chosen_set = load_last_session()
        if not chosen_set:
            print("No previous session found. Running a new session.")
            rerun = False
    
    if not rerun:
        chosen_set = get_word_set(word_sets, increment_views=True)
        save_last_session(chosen_set)

    seed_value = hashlib.md5(str(word_sets).encode()).hexdigest()
    random.seed(int(seed_value, 16))
    
    if chosen_set:
        if not rerun:
            save_word_sets(word_sets)
        display_session(chosen_set)
    else:
        print("No eligible word sets available.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a word learning session.")
    parser.add_argument('--rerun', action='store_true', help='Rerun the last session without updating')
    args = parser.parse_args()
    
    run_session(args.rerun)