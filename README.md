# Belief Revision Agent & Mastermind AI

This project was developed for Assignment 2 of the *Introduction to AI* course at DTU. It features a belief revision system based on AGM postulates and a logic-based Mastermind-playing agent.

## 📦 Components

- **`belief_base.py`**: Core class handling belief addition, contraction, revision, and consistency based on AGM theory.
- **`functions.py`**: Helper functions for logic resolution and CNF transformation.
- **`mastermind.py`**: AI agent that plays Mastermind by encoding feedback as beliefs and narrowing down possible codes.
- **`mastermind_interface.py`** : A **Pygame-based GUI** that visualizes each guess, feedback, and belief state over time. The AI plays automatically, and guesses are shown every 3 seconds.
- **`main.py`**:   Main script that lets the user:
  - Interact with the **belief base assistant** (add/remove/revise beliefs, check entailment, test AGM postulates).
  - Play Mastermind using the **AI agent in terminal**.
  - Watch the AI solve the game through the **graphical interface**.

## ▶️ Usage

1. Run the project:
   ```bash
   python main.py

2. Choose from the menu:
    1: Interact with the belief base assistant (terminal).

    2: Play Mastermind with the AI in terminal mode.

    3: Play Mastermind with the AI in graphical interface mode.

3. For graphical and terminal mode in the Mastermind:
    - Enter a secret 4-letter code using the characters: r, g, b, y, o, p. (e.g., 'rgop')
    - The GUI will display guesses and feedback step by step every 3 seconds. 

### 🎨 Color Legend (for Mastermind)

Each letter represents a color:

- `r` = Red  
- `g` = Green  
- `b` = Blue  
- `y` = Yellow  
- `o` = Orange  
- `p` = Purple

## 👥 Authors

- Mikel Fernandez Larruzea (s243273)  
- Mateo de Assas Aguirre (s243338)  
- Guillermo Moya Fernandez (s243295)  
- Roger Sala Sisó (s243328)
