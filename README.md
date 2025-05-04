# Belief Revision Agent & Mastermind AI

This project was developed for Assignment 2 of the *Introduction to AI* course at DTU. It features a belief revision system based on AGM postulates and a logic-based Mastermind-playing agent.

## 📦 Components

- **`belief_base.py`**: Core class handling belief addition, contraction, revision, and consistency based on AGM theory.
- **`functions.py`**: Helper functions for logic resolution and CNF transformation.
- **`mastermind.py`**: AI agent that plays Mastermind by encoding feedback as beliefs and narrowing down possible codes.
- **`main.py`**: Interface to either interact with the belief base or run the Mastermind AI.

## ▶️ Usage

Select the mode in `main.py` by setting `run = 1` (belief base) or `run = 2` (Mastermind AI). Then run:

```bash
python main.py
```

## 👥 Authors

- Mikel Fernandez Larruzea (s243273)  
- Mateo de Assas Aguirre (s243338)  
- Guillermo Moya Fernandez (s243295)  
- Roger Sala Sisó (s243328)
