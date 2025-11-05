#P: “It is raining” 
#Q: “I will take an umbrella”

from sympy import symbols
from sympy.logic.boolalg import And, Or, Not, Implies, Equivalent
from itertools import product

# Define propositions
P, Q = symbols('P Q')

# Define expressions
expr_and = And(P, Q)           # P ∧ Q
expr_or = Or(P, Q)             # P ∨ Q
expr_not_P = Not(P)             # ¬P
expr_implies = Implies(P, Q)   # P → Q
expr_equiv = Equivalent(P, Q)  # P ↔ Q

# Print header
print("P\tQ\tP∧Q\tP∨Q\t¬P\tP→Q\tP↔Q")

# Generate all combinations of True/False for P and Q
for p_val, q_val in product([True, False], repeat=2):
    # Evaluate each expression
    val_and = expr_and.subs({P: p_val, Q: q_val})
    val_or = expr_or.subs({P: p_val, Q: q_val})
    val_not_P = expr_not_P.subs({P: p_val})
    val_implies = expr_implies.subs({P: p_val, Q: q_val})
    val_equiv = expr_equiv.subs({P: p_val, Q: q_val})
    
    # Print row
    print(f"{p_val}\t{q_val}\t{val_and}\t{val_or}\t{val_not_P}\t{val_implies}\t{val_equiv}")
