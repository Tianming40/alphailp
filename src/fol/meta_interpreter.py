from logic_ops import *
from logic import *

def meta_interpreter(query, knowledge_base, n):
    """
    Meta-interpreter for performing inference on a query using a knowledge base.

    Parameters:
    query (Atom): The query to be evaluated.
    knowledge_base (list of Clause): The knowledge base containing logical rules.
    n (int): The number of inference steps to perform.

    Returns:
    bool: True if the query is entailed by the knowledge base, False otherwise.
    """
    facts = [clause.head for clause in knowledge_base if len(clause.body) == 0]
    return is_entailed(query, knowledge_base, facts, n)

def is_entailed(query, knowledge_base, facts, n):
    """
    Determines if a query is entailed by a knowledge base using n-step inference.

    Parameters:
    query (Atom): The query to be evaluated.
    knowledge_base (list of Clause): The knowledge base containing logical rules.
    facts (list of Atom): The initial set of facts.
    n (int): The number of inference steps to perform.

    Returns:
    bool: True if the query is entailed by the knowledge base, False otherwise.
    """
    return is_entailed_helper(query, knowledge_base, facts, set(), n)

def is_entailed_helper(query, knowledge_base, facts, visited, n):
    """
    Helper function for determining if a query is entailed by a knowledge base using n-step inference.

    Parameters:
    query (Atom): The query to be evaluated.
    knowledge_base (list of Clause): The knowledge base containing logical rules.
    facts (list of Atom): The current set of facts.
    visited (set of Atom): Set of visited atoms during inference.
    n (int): The number of inference steps remaining.

    Returns:
    bool: True if the query is entailed by the knowledge base, False otherwise.
    """
    if n == 0:
        return False
    if query in facts:
        return True
    visited.add(query)
    for clause in knowledge_base:
        for inferred_fact in t_p_n(clause, facts, 1):
            if inferred_fact not in visited:
                if is_entailed_helper(inferred_fact, knowledge_base, facts, visited, n - 1):
                    return True
    return False

# Example usage:
if __name__ == "__main__":
    # Define some predicates and atoms
    p = Predicate("p", 1, [])
    q = Predicate("q", 1, [])
    r = Predicate("r", 1, [])

    atom1 = Atom(p, [Const("a")])
    atom2 = Atom(q, [Const("b")])
    atom3 = Atom(r, [Var("X")]) # TODO exit???

    # Define some clauses in the knowledge base
    clause1 = Clause(atom1, [])
    clause2 = Clause(atom2, [])
    clause3 = Clause(Atom(p, [Var("X")]), [Atom(q, [Var("X")])])
    clause4 = Clause(atom3, [])

    knowledge_base = [clause1, clause2, clause3, clause4]

    # Define a query
    query = Atom(r, [Const("c")])

    # Perform inference
    n_steps = 3
    result = meta_interpreter(query, knowledge_base, n_steps)
    print("Query entailed:", result)
