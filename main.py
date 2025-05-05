from belief_base import BeliefBase
from mastermind import LogicalMastermindAI
import itertools

"""Select what to run"""

print("Welcome! What would you like to run?")
print("1. Belief Base Assistant")
print("2. Logical Mastermind AI")

while True:
    run = input("Enter 1 or 2: ").strip()
    if run == "1" or run == "2":
        break
    print("Invalid selection. Please enter 1 or 2.")



if run == 1:
    bb = BeliefBase()

    while True:
        print("\nBELIEF BASE MENU")
        print("1. Add a belief")
        print("2. Remove a belief")
        print("3. Show belief base")
        print("4. Contract a belief")
        print("5. Revise a belief")
        print("6. Check entailment")
        print("7. Test AGM postulates")
        print("8. Auto-fix inconsistent belief base")
        print("0. Exit")

        choice = input("Choose an option: ")
        show_after = True

        if choice == "1":
            print("Add a belief to the base. Example: A, A->B, A<->B, A&B, A|B, ¬A")
            belief = input("Enter the belief to add: ")
            belief = belief.lower().replace(" ", "").replace("=", "-")
            priority = int(input("Enter the priority (0 for default): ") or 0)
            bb.expand(belief, priority)

        elif choice == "2":
            print("Remove a belief by typing it exactly as it appears in the base.")
            belief = input("Enter the belief to remove: ")
            belief = belief.lower().replace(" ", "").replace("=", "-")
            bb.remove_belief(belief)

        elif choice == "3":
            print("Current belief base:")
            print(bb.get_formulas())
            show_after = False

        elif choice == "4":
            print("Contract the belief base to stop entailing a formula.")
            belief = input("Enter the belief to contract: ")
            belief = belief.lower().replace(" ", "").replace("=", "-")
            bb.contract(belief)

        elif choice == "5":
            print("Revise the belief base by a new belief (Levi identity).")
            belief = input("Enter the belief to revise with: ")
            belief = belief.lower().replace(" ", "").replace("=", "-")
            bb.revise(belief)

        elif choice == "6":
            print("Check if a query is logically entailed by the belief base.")
            query = input("Enter the query to check entailment: ")
            query = query.lower().replace(" ", "").replace("=", "-")
            print("Entails", query, "?", bb.entails(query))

        elif choice == "7":
            print(
                "Tests all AGM postulates (Success, Inclusion, Vacuity, Consistency, Extensionality)."
            )
            belief = input(
                "Enter the belief to test AGM postulates on (or type 'all' to test every belief): "
            )
            belief = belief.lower().replace(" ", "").replace("=", "-")
            if belief.lower() == "all":
                for f in bb.get_formulas():
                    bb.agm_postulates_test(f)
            else:
                bb.agm_postulates_test(belief)

        elif choice == "8":
            print("Automatically fixing inconsistent belief base...")
            bb.auto_fix()

        elif choice == "0":
            print("Exiting.")
            break

        else:
            print("Invalid option. Try again.")
            show_after = False

        if show_after:
            print("\nUpdated belief base:")
            print(bb.get_formulas())

else:
    ai = LogicalMastermindAI(
        colors="rgbyop"
    )  # red, green, blue, yellow, orange, purple
    print("Welcome to the Logical Mastermind AI!")
    print("The AI will try to guess the secret code using logical reasoning.")
    secret_code = input(
        "Enter the secret code (4 colors from rgbyop, e.g., 'rgby'): "
    ).lower()
    secret_code = tuple(secret_code)
    print("\n")

    for turn in range(10):
        guess = ai.make_guess()
        if guess is None:
            print("No consistent guesses left. Belief contradiction?")
            break
        print(f"Turn {turn+1}: AI guesses {guess}")
        fb = ai.feedback(guess, secret_code)
        print(f"Feedback: {fb[0]} black, {fb[1]} white")
        if fb[0] == ai.code_length:
            print("AI solved the code!")
            break
        ai.update_knowledge(guess, fb)

        print("\Belief base:", ai.belief_base.get_formulas(), "\n")
