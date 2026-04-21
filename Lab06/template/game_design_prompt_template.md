# Prompt for Generating a Simple Python Game

## 1. Objective

Create a complete, single-file Python application for a classic **[Game Title]** game using the **[Primary Library, e.g., Pygame, Tkinter]** library. The game should be easy to run and control, featuring a clean and well-defined interface.

## 2. Core Gameplay Mechanics

*   **Game World / Environment:**
    *   Describe the main play area.
    *   Window dimensions: **[e.g., 1024x768 pixels]**.
    *   Grid-based or continuous space: **[e.g., 32x32 pixel grid]**.

*   **Player Character:**
    *   Describe the player's representation in the game: **[e.g., A single sprite, a geometric shape]**.
    *   Starting position: **[e.g., Center of the screen]**.
    *   Movement controls: **[e.g., WASD for movement, Space for action]**.
    *   Special abilities or constraints: **[e.g., Can jump, cannot move through walls]**.

*   **Collectibles / Items / Enemies:**
    *   Describe other objects in the game world.
    *   Appearance: **[e.g., Gold coins, red enemy blobs]**.
    *   Behavior: **[e.g., Appear randomly, move towards the player]**.
    *   Interaction: **[e.g., Player collects coins to increase score, touching an enemy results in game over]**.

*   **Scoring / Progression:**
    *   Starting score: **[e.g., 0]**.
    *   How to score points: **[e.g., +10 points for each coin collected]**.
    *   Is there leveling or increasing difficulty? **[e.g., Game speed increases every 100 points]**.

*   **Win / Loss Conditions:**
    *   How the game ends (loss): **[e.g., Player runs out of lives, collides with a hazard]**.
    *   How the game ends (win): **[e.g., Reach a certain score, defeat a boss, survive for a time limit]**.
    *   What happens on game over: **[e.g., A "GAME OVER" message is displayed]**.

*   **Game Flow:**
    *   Can the player restart after a game over? **[e.g., By pressing the 'R' key]**.
    *   Is there a pause function? **[e.g., Pressing 'P' pauses and resumes the game]**.

## 3. GUI (Graphical User Interface)

*   **Art Style & Graphics:**
    *   Describe the desired aesthetic: **[e.g., Simple 2D, 8-bit retro, minimalist]**.
    *   Player character appearance: **[e.g., A blue square with a white outline]**.
    *   Item/Enemy appearance: **[e.g., Spinning gold coins]**.
    *   Background: **[e.g., A static starfield image, a solid dark gray color]**.

*   **User Interface (UI):**
    *   What information should be on screen? **[e.g., Current score, lives remaining, timer]**.
    *   Where should it be displayed? **[e.g., In a status bar at the top of the screen]**.

*   **Sound & Music:**
    *   Sound effects for actions: **[e.g., A 'blip' for collecting a coin, an 'explosion' for game over]**.
    *   Background music: **[e.g., A looping chiptune track]**.

## 4. Code Structure and Implementation

*   **Language and Library:**
    *   Use Python 3.
    *   Use the **[Primary Library, e.g., `pygame`]** library.

*   **Structure:**
    *   Organize the code within a **`[GameClassName]`** class to encapsulate all game-related logic and data.
    *   Use constants for key game parameters (window dimensions, colors, etc.).
    *   Create separate methods for handling user input, updating the game state, and rendering.
    *   Include a main game loop that controls the flow of the game.
    *   The code should be well-commented to explain the logic.

## 5. Deliverable

A single Python file (`[your_game_file].py`) containing the complete, runnable game.
