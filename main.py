#!/usr/bin/env python3
"""
Main entry point for the Kids 2048 game.
"""
import os
from game import Game

if __name__ == "__main__":
    # Make sure assets directory exists
    os.makedirs(os.path.join("assets", "fonts"), exist_ok=True)
    os.makedirs(os.path.join("assets", "images"), exist_ok=True)
    os.makedirs(os.path.join("assets", "sounds"), exist_ok=True)
    
    game = Game()
    game.run()
