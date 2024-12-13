from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # If A is a knight, the statement "I am both a knight and a knave" must be true:
    Implication(AKnight, And(AKnight, AKnave)),
    # If A is a knave, the statement "I am both a knight and a knave" must be false:
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # If A is a knight, the statement "We are both knaves" must be true:
    Implication(AKnight, And(AKnave, BKnave)),
    # If A is a knave, the statement "We are both knaves" must be false:
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # If A is a knight, the statement "We are the same kind" must be true:
    Implication(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))),
    # If A is a knave, the statement "We are the same kind" must be false:
    Implication(AKnave, Not(Or(And(AKnave, BKnave), And(AKnight, BKnight)))),
    # If B is a knight, the statement "We are of different kinds" must be true:
    Implication(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave))),
    # If B is a knave, the statement "We are of different kinds" must be false:
    Implication(BKnave, Not(Or(And(AKnave, BKnight), And(AKnight, BKnave))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    # If A is a knave, their statement must be false:
    # A saying "I am a knight" -> AKnight must be false
    # A saying "I am a knave" -> AKnave must be false (self-contradiction)
    Implication(AKnave, Not(AKnave)),

    # If B is a knight, their statement is true:
    Implication(BKnight, AKnave),

    Implication(AKnight, AKnight),
    # If B is a knight, the statement "C is a knave" must be true:
    Implication(BKnight, CKnave),
    # If B is a knave, the statement "C is a knave" must be false:
    Implication(BKnave, CKnight),
    # If B is a knight, the statement "C is a knave" must be true:
    Implication(CKnight, AKnight),
    # If B is a knave, the statement "C is a knave" must be false:
    Implication(CKnave, AKnave)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
