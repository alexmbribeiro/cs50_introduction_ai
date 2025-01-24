import sys

from crossword import *
from collections import deque


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.domains:
            for word in self.domains[variable].copy():
                # making sure that every value in a variable’s domain has the same number of letters as the variable’s length.
                if (variable.length != len(word)):
                    self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable x arc consistent with variable y.
        Remove values from self.domains[x] that are inconsistent with self.domains[y].

        Return True if a revision was made; False otherwise.
        """
        revised = False
        overlap = self.crossword.overlaps[x, y]  # Get the overlap between x and y

        # If there is no overlap, the variables are not connected
        if overlap is None:
            return False

        i, j = overlap  # Positions where x and y overlap

        to_remove = set()
        for x_word in self.domains[x]:
            # Check if any y_word satisfies the overlap condition
            if not any(x_word[i] == y_word[j] for y_word in self.domains[y]):
                to_remove.add(x_word)

        # Remove inconsistent words from x's domain
        if to_remove:
            self.domains[x] -= to_remove
            revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        queue = deque(arcs if arcs != None else [
            (x, y) for x in self.domains for y in self.crossword.neighbors(x)
        ])

        while queue:
            x, y = queue.popleft()

            # If, in the process of enforcing arc consistency, you remove all of the remaining values from a domain, return False (this means it’s impossible to solve the problem, since there are no more possible values for the variable)
            if not self.domains[x] or len(self.domains[x]) == 0:
                return False
            
            # Any time you make a change to a domain, you may need to add additional arcs to your queue to ensure that other arcs stay consistent.
            if (self.revise(x, y)):
                for neighbor in self.crossword.neighbors(x):
                    if y != neighbor:
                        queue.append((x, neighbor))
        
        return True
    
    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if assignment.keys() is None:
            return False

        if self.crossword.variables != assignment.keys():
            return False
         
        for variable in assignment.keys():
            if assignment[variable] is None:
                return False
            
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        seen = set()

        for variable in assignment.keys():
            if assignment[variable] == None:
                return True
            
            # Return true if all values are distinct
            if assignment[variable] in seen:
                return False
            
            # Return true if every value is the correct length
            if variable.length != len(assignment[variable]):
                return False
            
            # Return true if there are no conflicts between neighboring variables
            for neighbor in self.crossword.neighbors(variable):
                if neighbor in assignment.keys() and assignment[neighbor] != None:
                    x_pos, y_pos = self.crossword.overlaps[variable, neighbor]

                    if (assignment[variable][x_pos] != assignment[neighbor][y_pos]):
                        return False
            
            seen.add(assignment[variable])
            
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a dict of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the dict, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        order_dic = dict()

        for value in self.domains[var]:     # iterate over all values in the domain
            count = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment.keys():   # check which neighbors haven't been assigned yet
                    for neighbor_value in self.domains[neighbor]:
                        x_pos, y_pos = self.crossword.overlaps[var, neighbor]
                        # count how many values in neighbors domain will be removed
                        if (value[x_pos] != neighbor_value[y_pos]):
                            count += 1
            
            order_dic[value] = count

        return list(dict(sorted(order_dic.items(), key=lambda item: item[1])).keys())    # sort the dict by count and make it a list

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_vars = [
            var for var in self.crossword.variables if assignment.get(var) is None
        ]

        if not unassigned_vars:
            return None

        return min(
            unassigned_vars,
            key=lambda var: (len(self.domains[var]), -len(self.crossword.neighbors(var)))
        )  

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if len(assignment.keys()) == 0:
            for var in self.crossword.variables:
                assignment[var] = None
                
        if self.assignment_complete(assignment):
            if self.consistent(assignment):
                return assignment
            return None
        
        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            assignment[var] = value

            if self.consistent(assignment):
                result = self.backtrack(assignment)  # Recurse
                if result is not None:  # If solution found, return it
                    return result
                
            assignment[var] = None
    
        return None
    

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
