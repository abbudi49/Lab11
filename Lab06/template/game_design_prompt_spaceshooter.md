# Prompt for Generating a Space Shooter Game

## 1. Objective

Create a complete, single-file Python application for a simple **Space Shooter** game using the **Pygame** library. The game should be easy to run and control, featuring a clean and visually appealing interface.

## 2. Core Gameplay Mechanics

*   **Game World / Environment:**
    *   The game is played in a vertical scrolling window.
    *   Window dimensions: **600x800 pixels**.
    *   The background should be a starfield or space theme.

*   **Player Character (Spaceship):**
    *   The player controls a spaceship at the bottom of the screen.
    *   Spaceship size: **50x40 pixels** (triangle or simple ship sprite).
    *   Starting position: **Bottom center of the screen**.
    *   Movement controls: **Left Arrow and Right Arrow** or **'A' (left) and 'D' (right)**.
    *   The spaceship cannot move off-screen horizontally.
    *   The spaceship can shoot bullets upward.

*   **Shooting:**
    *   Press **Space** to shoot bullets.
    *   Bullets are small rectangles (5x15 pixels) that move upward.
    *   The player can have **multiple bullets on screen** at once.
    *   There can be a small cooldown between shots (e.g., 0.25 seconds).

*   **Enemies:**
    *   Enemies appear from the top of the screen and move downward.
    *   Enemy size: **40x40 pixels** (squares or simple enemy sprites).
    *   Enemies spawn at random horizontal positions.
    *   Spawn rate: **One enemy every 1-2 seconds**.
    *   Enemies can have different colors (red, purple, cyan).

*   **Collisions:**
    *   When a bullet hits an enemy, both disappear.
    *   When an enemy reaches the bottom of the screen, the player loses a life.
    *   When an enemy collides with the player's spaceship, the player loses a life.

*   **Lives:**
    *   The player starts with **3 lives**.
    *   The game ends when all lives are lost.

*   **Scoring / Progression:**
    *   Starting score: **0**.
    *   Each enemy destroyed: **+10 points**.
    *   Optionally, enemy spawn rate can increase as score increases.

*   **Win / Loss Conditions:**
    *   **Loss:** The player runs out of lives. Display "GAME OVER" message.
    *   There is no explicit win condition; the goal is to achieve the highest score.

*   **Game Flow:**
    *   Can restart after game over by pressing the **'R' key**.
    *   Can pause the game by pressing **'P' key**.

## 3. GUI (Graphical User Interface)

*   **Art Style & Graphics:**
    *   Simple, clean, 2D space-themed graphics.
    *   Player spaceship: **White triangle or simple spaceship shape**.
    *   Bullets: **Small white or yellow rectangles/circles**.
    *   Enemies: **Colored squares or simple alien shapes (red, purple, cyan)**.
    *   Background: **Black with white dots representing stars**.

*   **User Interface (UI):**
    *   Display the current score in the **top-left corner**.
    *   Display the number of lives remaining in the **top-right corner** (e.g., "Lives: 3").

*   **Sound & Music:**
    *   No sound required.

## 4. Code Structure and Implementation

*   **Language and Library:**
    *   Use Python 3.
    *   Use the **`pygame`** library.

*   **Structure:**
    *   Organize the code within a **`SpaceShooterGame`** class to encapsulate all game-related logic and data.
    *   Use constants for key game parameters (window dimensions, colors, speeds, spawn rates, etc.).
    *   Consider creating helper classes for `Bullet` and `Enemy` objects to manage their state.
    *   Create separate methods for handling user input, updating the game state (movement, collision detection, spawning), and rendering.
    *   Include a main game loop that controls the flow of the game.
    *   The code should be well-commented to explain the logic.

## 5. Deliverable

A single Python file (`spaceshooter_game.py`) containing the complete, runnable game.
