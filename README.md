# Theory of Languages and Automata (TLA) Midterm Project

This project was completed for the Theory of Languages and Automata course at Iran University of Science and Technology (IUST) during the Spring 2023 semester. It aims to explore and implement key concepts in formal languages and automata theory through a series of tasks. The project is divided into five distinct phases:

## Project Phases

### Phase 1: NFA to DFA Conversion
- **Objective**: Convert a Non-deterministic Finite Automaton (NFA) to a Deterministic Finite Automaton (DFA).
- **Details**: This phase involves creating a DFA from an NFA by eliminating non-determinism through the subset construction method. The result is a deterministic machine that accepts the same language as the original NFA.

### Phase 2: DFA Simplification
- **Objective**: Simplify the DFA obtained in Phase 1.
- **Details**: This phase focuses on minimizing the DFA by merging equivalent states. The simplification process ensures that the DFA is in its minimal form, with no redundant states or transitions.

### Phase 3: String Acceptance on FA
- **Objective**: Implement and test string acceptance on a Finite Automaton (FA).
- **Details**: This phase involves creating a procedure to determine if a given string is accepted by the FA (NFA or DFA). It includes designing algorithms to traverse the automaton and check for string acceptance.

### Phase 4: Operations on a Regular Language
- **Objective**: Perform various operations on regular languages.
- **Details**: This phase covers operations such as union, intersection, and complementation of regular languages. It involves applying these operations to the automata and examining the resulting language properties.

### Phase 5: FA to RegEx Conversion using Arden's Lemma
- **Objective**: Convert a Finite Automaton to a Regular Expression (RegEx) using Arden's Lemma.
- **Details**: This phase focuses on deriving a regular expression that represents the language accepted by the FA. Arden's Lemma is used to construct the regular expression from the given automaton.

## Getting Started

To get started with this project, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Bahareh0281/TLA-MidtermProject.git
   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd TLA-MidtermProject
   ```

3. **Set Up the Environment**:
   - **Create a Virtual Environment** (optional but recommended):
     ```bash
     python -m venv venv
     ```
   - **Activate the Virtual Environment**:
     - On Windows:
       ```bash
       venv\Scripts\activate
       ```
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```
   - **Install Dependencies**:
     ```bash
     pip install -r requirements.txt
     ```

4. **Run the Project**:
   Follow the instructions provided in each phase’s directory to run the respective implementations and tests.

## Dependencies

The project dependencies are listed in the `requirements.txt` file. To install them, use the command provided in the "Set Up the Environment" section.
