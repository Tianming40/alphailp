from logic_ops import unify, is_entailed
from logic import Atom, Clause, Var, Const, Predicate
def meta_interpreter(program, query):
    """
    A simple meta interpreter for first-order logic.

    Args:
    - program (list): A list of logical clauses representing the program.
    - query (logic.Atom): The query to be evaluated.

    Returns:
    - bool: True if the query is entailed by the program, False otherwise.
    """
    # Initialize the set of facts with the program
    facts = program.copy()

    # Perform inference until a fixed point is reached
    while True:
        new_facts = set()

        # Perform one-step forward chaining inference
        for clause in program:
            inferred_atoms = t_p(clause, facts)
            new_facts.update(inferred_atoms)

        # Check if any new facts were inferred
        if len(new_facts.difference(facts)) == 0:
            break

        # Update the set of facts
        facts.update(new_facts)

    # Check if the query is entailed by the facts
    return is_entailed(query, query, facts, n=1)

def t_p(clause, facts):
    """
    One-step forward chaining inference.

    Args:
    - clause (logic.Clause): The clause to be used for inference.
    - facts (set): The set of known facts.

    Returns:
    - set: The set of new facts inferred from the clause.
    """
    new_facts = set()
    for fact in facts:
        flag, thetas = unify([clause.body[0], fact])
        if flag:
            head_fact = subs_list(clause.head, thetas)
            new_facts.add(head_fact)
    return new_facts

# Example usage:
if __name__ == "__main__":
    from logic import Atom

    # Define the program
    program = [
        Clause(Atom(Predicate("parent", 2, [str, str]), [Var("X"), Var("Y")]),
               [Atom(Predicate("father", 2, [str, str]), [Var("X"), Var("Y")])]),
        Clause(Atom(Predicate("father", 2, [str, str]), ["John", "Bob"]), []),
        # Add more clauses as needed
    ]

    # Define the query
    query = Atom(Predicate("parent", 2, [str, str]), ["John", "Bob"])

    # Evaluate the query
    result = meta_interpreter(program, query)
    print("Query result:", result)
