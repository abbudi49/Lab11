game_design_prompt_snake# Prompt for Generating a Simple Python Game

## 1. Objective

Create a complete, single-file Python application for a classic **Ping Pong** game using the **Pygame** library. The game should be easy to run and control, featuring a clean and well-defined interface for two players.

## 2. Core Gameplay Mechanics

*   **Game World / Environment:**
    *   The game is played in a rectangular window.
    *   Window dimensions: **800x600 pixels**.
    *   Continuous space. A vertical dashed line should be drawn in the center to represent the net.

*   **Player Paddles:**
    *   The game features two paddles, one on the left and one on the right.
    *   Paddles are vertical rectangles.
    *   Player 1 (left paddle) controls: **'W' (up) and 'S' (down)**.
    *   Player 2 (right paddle) controls: **Up Arrow (up) and Down Arrow (down)**.
    *   Paddles are constrained to move vertically and cannot go off-screen.

*   **The Ball:**
    *   A single ball moves continuously across the screen.
    *   The ball bounces off the top and bottom walls.
    *   The ball bounces off the paddles. The angle of reflection can be simple (just reversing the x-direction) or slightly influenced by where it hits the paddle.
    *   When the ball goes past a paddle and hits the left or right wall, a point is scored.

*   **Scoring / Progression:**
    *   Starting score: **0-0**.
    *   If the ball passes the right paddle, the left player scores 1 point.
    *   If the ball passes the left paddle, the right player scores 1 point.
    *   After a point is scored, the ball should reset to the center of the screen and move towards the player who did not score.

*   **Win / Loss Conditions:**
    *   The game ends when a player reaches a score of **11**.
    *   What happens on game over: **A "Player X Wins!" message is displayed in the center of the screen, where X is the winning player's number**.

*   **Game Flow:**
    *   The player can restart the game after a win by pressing the **'R' key**.
    *   There is no pause function required.

## 3. GUI (Graphical User Interface)

*   **Art Style & Graphics:**
    *   Describe the desired aesthetic: **Minimalist, 2D, retro**.
    *   Player paddle appearance: **White rectangles**.
    *   Ball appearance: **A white square**.
    *   Background: **A solid black color**.

*   **User Interface (UI):**
    *   What information should be on screen? **The score for Player 1 and Player 2**.
    *   Where should it be displayed? **Player 1's score on the top-left, Player 2's score on the top-right**.

*   **Sound & Music:**
    *   Sound effects for actions: **No**.
    *   Background music: **No**.

## 4. Code Structure and Implementation

*   **Language and Library:**
    *   Use Python 3.
    *   Use the **`pygame`** library.

*   **Structure:**
    *   Organize the code within a **`PongGame`** class to encapsulate all game-related logic and data.
    *   Use constants for key game parameters (window dimensions, colors, paddle size, ball speed, etc.).
    *   Create separate methods for handling user input, updating the game state, and rendering.
    *   Include a main game loop that controls the flow of the game.
    *   The code should be well-commented to explain the logic.

## 5. Deliverable

A single Python file (`pong_game.py`) containing the complete, runnable game.
