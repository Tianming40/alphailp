from logic import *
from logic_ops import unify

def unify_list(terms1, terms2):
    if len(terms1) != len(terms2):
        return None
    unifier = []
    for t1, t2 in zip(terms1, terms2):
        flag, theta = unify([t1, t2])
        if not flag:
            return None
        unifier.extend(theta)
    return unifier

def apply_substitution(term, substitution):
    for var, const in substitution:
        term = subs(term, var, const)
    return term

def evaluate(atom, facts, rules):
    if atom in facts:
        return True
    for clause in rules:
        if clause.head.pred == atom.pred:
            unifier = unify_list(clause.head.terms, atom.terms)
            if unifier is not None:
                new_body = [apply_substitution(body_atom, unifier) for body_atom in clause.body]
                if all([evaluate(new_body_atom, facts, rules) for new_body_atom in new_body]):
                    return True
    return False

def meta_interpreter(query, facts, rules):
    return evaluate(query, facts, rules)

# 示例使用：
if __name__ == "__main__":
    # 定义一些事实和规则
    fact1 = Atom(Predicate("parent", 2, [str, str]), [Const("alice"), Const("bob")])
    fact2 = Atom(Predicate("parent", 2, [str, str]), [Const("bob"), Const("charlie")])
    fact3 = Atom(Predicate("parent", 2, [str, str]), [Const("charlie"), Const("david")])
    rule = Clause(Atom(Predicate("ancestor", 2, [str, str]), [Var("X"), Var("Y")]),
                  [Atom(Predicate("parent", 2, [str, str]), [Var("X"), Var("Y")])])
    # 定义查询
    query = Atom(Predicate("ancestor", 2, [str, str]), [Const("alice"), Var("Z")])
    # 调用元解释器
    result = meta_interpreter(query, [fact1, fact2, fact3], [rule])
    print("查询是否为真:", result)
