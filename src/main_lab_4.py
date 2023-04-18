import unittest
import grammar

class UnitTests(unittest.TestCase):
    def test1_eliminate_eps(self):
        # My grammar (11).
        V_n = ['S', 'A', 'B', 'C', 'D']
        V_t = ['a', 'b']
        P = {
            'S': ['bA', 'AC'],
            'A': ['bS', 'BC', 'AbAa'],
            'B': ['BbaA', 'a', 'bSa'],
            'C': [''],
            'D': ['AB']
        }
        solution = {
            'S': {'bA', 'AC', 'A'},
            'A': {'bS', 'BC', 'AbAa', 'B'},
            'B': {'BbaA', 'a', 'bSa'},
            'D': {'AB'}
        }
        grammar_11 = grammar.Grammar(V_n, V_t, P, 'S')
        my_solution = grammar_11.eliminate_eps()
        my_solution = {k: set(v) for k, v in my_solution.items()}
        self.assertDictEqual(solution, my_solution)

    def test2_eliminate_eps(self):
        # Example from the guide "3.1 Elimination of eps – productions p. 55"
        V_n = ['S', 'A', 'B', 'C', 'D']
        V_t = ['a', 'b']
        P = {
            'S': ['aAb'],
            'A': ['abBCBaD', 'B'],
            'B': ['bB', ''],
            'D': ['AB'],
            'C': ['a']
        }
        solution = {
            'S': {'aAb', 'ab'},
            'A': {'abBCBaD', 'abBCBa', 'abCBaD', 'abCBa', 'abBCaD', 'abBCa', 'abCaD', 'abCa', 'B'},
            'B': {'bB', 'b'},
            'D': {'AB', 'B', 'A'},
            'C': {'a'}
        }
        grammar_11 = grammar.Grammar(V_n, V_t, P, 'S')
        my_solution = grammar_11.eliminate_eps()
        my_solution = {k: set(v) for k, v in my_solution.items()}
        self.assertDictEqual(solution, my_solution)


    def test3_eliminate_eps(self):
        # Example from "Chomsky Normal Form normalization example" given for laboratory work #4.
        V_n = ['S', 'A', 'B', 'C', 'D']
        V_t = ['a', 'b']
        P = {
            'S': ['AC', 'bA', 'B', 'aA'],
            'A': ['', 'aS', 'ABAb'],
            'B': ['a', 'AbSA'],
            'C': ['abC'],
            'D': ['AB']
        }
        solution = {
            'S': {'AC', 'bA', 'B', 'aA', 'C', 'b', 'a'},
            'A': {'aS', 'ABAb', 'BAb', 'ABb', 'Bb'},
            'B': {'a', 'AbSA', 'bSA', 'AbS', 'bS'},
            'C': {'abC'},
            'D': {'AB', 'B'}
        }
        grammar_11 = grammar.Grammar(V_n, V_t, P, 'S')
        my_solution = grammar_11.eliminate_eps()
        my_solution = {k: set(v) for k, v in my_solution.items()}
        self.assertDictEqual(solution, my_solution)

    
    def test1_eliminate_renaming(self):
        # My grammar (11) with eliminated epsilon productions.
        V_n = ['S', 'A', 'B', 'C', 'D']
        V_t = ['a', 'b']
        P = {
            'S': ['bA', 'AC', 'A'], 
            'A': ['bS', 'BC', 'AbAa', 'B'], 
            'B': ['BbaA', 'a', 'bSa'], 
            'D': ['AB']
        }
        solution = {
            'S': {'bA', 'AC', 'bS', 'BC', 'AbAa', 'BbaA', 'a', 'bSa'}, 
            'A': {'bS', 'BC', 'AbAa', 'BbaA', 'a', 'bSa'}, 
            'B': {'BbaA', 'a', 'bSa'},
            'D': {'AB'}
        }
        grammar_11 = grammar.Grammar(V_n, V_t, P, 'S')
        my_solution = grammar_11.eliminate_renaming()
        my_solution = {k: set(v) for k, v in my_solution.items()}
        self.assertDictEqual(solution, my_solution)

    
    def test2_eliminate_renaming(self):
        # Example from the guide "3.2 Elimination of the Unit Productions p. 59"
        V_n = ['S', 'A', 'B', 'C', 'D', 'E']
        V_t = ['a', 'b']
        P = {
            'S': ['ACD', 'AD', 'AC', 'A'],
            'A': ['a'],
            'C': ['ED', 'E'],
            'D': ['BC', 'b', 'B', 'C'],
            'E': ['b'],
            'B': ['a']
        }
        solution = {
            'S': {'ACD', 'AD', 'AC', 'a'},
            'A': {'a'},
            'C': {'ED', 'b'},
            'D': {'BC', 'b', 'a', 'ED', 'b'},
            'E': {'b'},
            'B': {'a'}
        }
        grammar_11 = grammar.Grammar(V_n, V_t, P, 'S')
        my_solution = grammar_11.eliminate_renaming()
        my_solution = {k: set(v) for k, v in my_solution.items()}
        self.assertDictEqual(solution, my_solution)


    def test3_eliminate_renaming(self):
        # Example with cycle from theme 4 slide 25.
        V_n = ['S', 'R', 'T']
        V_t = ['0', '1']
        P = {
            'S': ['0S1', '1S0S', 'T'],
            'T': ['S', 'R', ''],
            'R': ['0SR']
        }
        solution = {
            'S': {'0S1', '1S0S', '0SR', ''},
            'R': {'0SR'}
        }
        grammar_11 = grammar.Grammar(V_n, V_t, P, 'S')
        my_solution = grammar_11.eliminate_renaming()
        my_solution = {k: set(v) for k, v in my_solution.items()}
        self.assertDictEqual(solution, my_solution)

    
    def test4_eliminate_renaming(self):
        # Above example modified with more cycles.
        V_n = ['S', 'R', 'T']
        V_t = ['0', '1']
        P = {
            'S': ['0S1', '1S0S', 'T'],
            'T': ['S', 'R', ''],
            'R': ['0SR', 'S']
        }
        solution = {
            'S': {'0S1', '1S0S', '0SR', '', '0SR'}
        }
        grammar_11 = grammar.Grammar(V_n, V_t, P, 'S')
        my_solution = grammar_11.eliminate_renaming()
        my_solution = {k: set(v) for k, v in my_solution.items()}
        self.assertDictEqual(solution, my_solution)

    
    def test5_eliminate_renaming(self):
        # Example from "Chomsky Normal Form normalization example"
        # given for laboratory work #4, without epsilon productions.
        V_n = ['S', 'A', 'B', 'C', 'D']
        V_t = ['a', 'b']
        P = {
            'S': ['AC', 'bA', 'B', 'aA', 'C', 'b', 'a'], 
            'A': ['aS', 'ABAb', 'BAb', 'ABb', 'Bb'], 
            'B': ['a', 'AbSA', 'bSA', 'AbS', 'bS'], 
            'C': ['abC'], 
            'D': ['AB', 'B']
        }
        solution = {
            'S': {'AC', 'bA', 'AbSA', 'bSA', 'AbS', 'bS', 'aA', 'abC', 'b', 'a'}, 
            'A': {'aS', 'ABAb', 'BAb', 'ABb', 'Bb'}, 
            'B': {'a', 'AbSA', 'bSA', 'AbS', 'bS'}, 
            'C': {'abC'}, 
            'D': {'AB', 'a', 'AbSA', 'bSA', 'AbS', 'bS'}
        }
        grammar_11 = grammar.Grammar(V_n, V_t, P, 'S')
        my_solution = grammar_11.eliminate_renaming()
        my_solution = {k: set(v) for k, v in my_solution.items()}
        self.assertDictEqual(solution, my_solution)

    
    def test1_eliminate_non_productive(self):
        # My grammar (11) with eliminated epsilons and renamings.
        V_n = ['S', 'A', 'B', 'C', 'D']
        V_t = ['a', 'b']
        P = {
            'S': ['bA', 'AC', 'bS', 'BC', 'AbAa', 'BbaA', 'a', 'bSa'], 
            'A': ['bS', 'BC', 'AbAa', 'BbaA', 'a', 'bSa'], 
            'B': ['BbaA', 'a', 'bSa'],
            'D': ['AB']
        }
        solution = {
            'S': {'bA', 'bS', 'AbAa', 'BbaA', 'a', 'bSa'}, 
            'A': {'bS', 'AbAa', 'BbaA', 'a', 'bSa'}, 
            'B': {'BbaA', 'a', 'bSa'},
            'D': {'AB'}
        }
        expected_V_n = {'S', 'A', 'B', 'D'}

        grammar_11 = grammar.Grammar(V_n, V_t, P, 'S')
        my_solution, V_N = grammar_11.eliminate_non_productive(), set(grammar_11.V_n)
        my_solution = {k: set(v) for k, v in my_solution.items()}
        self.assertDictEqual(solution, my_solution)
        self.assertSetEqual(expected_V_n, V_N)


    def test2_eliminate_non_productive(self):
        # Example from "Chomsky Normal Form normalization example" without epsilons and renamings.
        V_n = ['S', 'A', 'B', 'C', 'D']
        V_t = ['a', 'b']
        P = {
            'S': ['AbS', 'bA', 'b', 'bS', 'abC', 'AC', 'a', 'AbSA', 'bSA', 'aA'], 
            'A': ['Bb', 'aS', 'ABb', 'BAb', 'ABAb'], 
            'B': ['AbS', 'bS', 'a', 'AbSA', 'bSA'], 
            'C': ['abC'], 
            'D': ['AbS', 'bS', 'AB', 'a', 'AbSA', 'bSA']
        }
        solution = {
            'S': {'a', 'bA', 'aA', 'b', 'AbSA', 'bSA', 'AbS', 'bS'}, 
            'A': {'aS', 'ABAb', 'BAb', 'ABb', 'Bb'}, 
            'B': {'a', 'AbSA', 'bSA', 'AbS', 'bS'},
            'D': {'bSA', 'AB', 'a', 'AbS', 'bS', 'AbSA'}
        }
        expected_V_n = {'S', 'A', 'B', 'D'}

        grammar_11 = grammar.Grammar(V_n, V_t, P, 'S')
        my_solution, V_N = grammar_11.eliminate_non_productive(), set(grammar_11.V_n)
        my_solution = {k: set(v) for k, v in my_solution.items()}
        self.assertDictEqual(solution, my_solution)
        self.assertSetEqual(expected_V_n, V_N)

    
    def test3_eliminate_non_productive(self):
        # Example from the guide "3.4 Elimination of the Non-Productive Symbols p. 62"
        V_n = ['S', 'A', 'B', 'C', 'D', 'E']
        V_t = ['a', 'b']
        P = {
            'S': ['ACD'],
            'A': ['a'],
            'C': ['ED'],
            'D': ['BC', 'b'],
            'E': ['b']
        }
        expected_V_n = {'S', 'A', 'C', 'D', 'E'}
        solution = {
            'S': {'ACD'},
            'A': {'a'},
            'C': {'ED'},
            'D': {'b'},
            'E': {'b'}
        }

        grammar_11 = grammar.Grammar(V_n, V_t, P, 'S')
        my_solution, V_N = grammar_11.eliminate_non_productive(), set(grammar_11.V_n)
        my_solution = {k: set(v) for k, v in my_solution.items()}
        self.assertDictEqual(solution, my_solution)
        self.assertSetEqual(expected_V_n, V_N)


    def test1_eliminate_inaccessibles(self):
        # My grammar (11) with eliminated epsilons, renamings and non-productives.
        V_n = ['S', 'A', 'B', 'D']
        V_t = ['a', 'b']
        P = {
            'S': ['a', 'bSa', 'AbAa', 'bS', 'bA', 'BbaA'], 
            'A': ['a', 'bSa', 'AbAa', 'bS', 'BbaA'], 
            'B': ['a', 'bSa', 'BbaA'], 
            'D': ['AB']
        }
        expected_V_n = {'S', 'A', 'B'}
        expected_V_t = {'a', 'b'}
        solution = {
            'S': {'bA', 'bS', 'AbAa', 'BbaA', 'a', 'bSa'}, 
            'A': {'bS', 'AbAa', 'BbaA', 'a', 'bSa'}, 
            'B': {'BbaA', 'a', 'bSa'},
        }

        grammar_11 = grammar.Grammar(V_n, V_t, P, 'S')
        my_solution, V_N, V_T = grammar_11.eliminate_inaccessibles(), set(grammar_11.V_n), set(grammar_11.V_t)
        my_solution = {k: set(v) for k, v in my_solution.items()}
        self.assertDictEqual(solution, my_solution)
        self.assertSetEqual(expected_V_n, V_N)
        self.assertSetEqual(expected_V_t, V_T)

    
    def test2_eliminate_inaccessibles(self):
        # Example from "Chomsky Normal Form normalization example" without epsilons, renamings, non-prods.
        V_n = ['S', 'A', 'B', 'D']
        V_t = ['a', 'b']
        P = {
            'S': ['AbS', 'bA', 'b', 'bS', 'a', 'AbSA', 'bSA', 'aA'], 
            'A': ['Bb', 'aS', 'ABb', 'BAb', 'ABAb'], 
            'B': ['AbS', 'bS', 'a', 'AbSA', 'bSA'], 
            'D': ['AbS', 'bS', 'AB', 'a', 'AbSA', 'bSA']
        }
        solution = {
            'S': {'a', 'bA', 'aA', 'b', 'AbSA', 'bSA', 'AbS', 'bS'}, 
            'A': {'aS', 'ABAb', 'BAb', 'ABb', 'Bb'}, 
            'B': {'a', 'AbSA', 'bSA', 'AbS', 'bS'},
        }
        expected_V_n = {'S', 'A', 'B'}
        expected_V_t = {'a', 'b'}

        grammar_11 = grammar.Grammar(V_n, V_t, P, 'S')
        my_solution, V_N, V_T = grammar_11.eliminate_inaccessibles(), set(grammar_11.V_n), set(grammar_11.V_t)
        my_solution = {k: set(v) for k, v in my_solution.items()}
        self.assertDictEqual(solution, my_solution)
        self.assertSetEqual(expected_V_n, V_N)
        self.assertSetEqual(expected_V_t, V_T)


    def test3_eliminate_inaccessibles(self):
        # Example from the guide "3.3 Elimination of the Inaccessible Symbols p. 60"
        V_n = ['S', 'A', 'B', 'C', 'D', 'E']
        V_t = ['a', 'b']
        P = {
            'S': ['AC'],
            'A': ['a'],
            'B': ['b'],
            'C': ['Ea'],
            'D': ['BC', 'b'],
            'E': ['b']
        }
        solution = {
            'S': {'AC'},
            'A': {'a'},
            'C': {'Ea'},
            'E': {'b'}
        }
        expected_V_n = {'S', 'A', 'C', 'E'}
        expected_V_t = {'a', 'b'}

        grammar_11 = grammar.Grammar(V_n, V_t, P, 'S')
        my_solution, V_N, V_T = grammar_11.eliminate_inaccessibles(), set(grammar_11.V_n), set(grammar_11.V_t)
        my_solution = {k: set(v) for k, v in my_solution.items()}
        self.assertDictEqual(solution, my_solution)
        self.assertSetEqual(expected_V_n, V_N)
        self.assertSetEqual(expected_V_t, V_T)


    def test1_to_CNF(self):
        # My grammar (11).
        V_n = ['S', 'A', 'B', 'C', 'D']
        V_t = ['a', 'b']
        P = {
            'S': ['bA', 'AC'],
            'A': ['bS', 'BC', 'AbAa'],
            'B': ['BbaA', 'a', 'bSa'],
            'C': [''],
            'D': ['AB']
        }
        expected_V_n = {'S', 'A', 'B', 'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7'}
        expected_V_t = {'a', 'b'}
        solution = {
            'S': {('X1', 'S'), ('X1', 'X5'), ('A', 'X3'), ('B', 'X4'), ('a',), ('X1', 'A')}, 
            'A': {('X1', 'S'), ('X1', 'X5'), ('A', 'X3'), ('B', 'X4'), ('a',)}, 
            'B': {('a',), ('X1', 'X5'), ('B', 'X4')}, 
            'X1': {('b',)}, 
            'X2': {('a',)}, 
            'X3': {('X1', 'X6')}, 
            'X4': {('X1', 'X7')}, 
            'X5': {('S', 'X2')}, 
            'X6': {('A', 'X2')}, 
            'X7': {('X2', 'A')}
        }

        grammar_11 = grammar.Grammar(V_n, V_t, P, 'S')
        my_solution, V_N, V_T = grammar_11.to_CNF(), set(grammar_11.V_n), set(grammar_11.V_t)
        my_solution = {k: {tuple(x) for x in v} for k, v in my_solution.items()}
        self.assertDictEqual(solution, my_solution)
        self.assertSetEqual(expected_V_n, V_N)
        self.assertSetEqual(expected_V_t, V_T)


    def test2_to_CNF(self):
        # Example from "Chomsky Normal Form normalization example".
        V_n = ['S', 'A', 'B', 'C', 'D']
        V_t = ['a', 'b']
        P = {
            'S': ['AC', 'bA', 'B', 'aA'],
            'A': ['', 'aS', 'ABAb'],
            'B': ['a', 'AbSA'],
            'C': ['abC'],
            'D': ['AB']
        }
        expected_V_n = {'S', 'A', 'B', 'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8'}
        expected_V_t = {'a', 'b'}
        solution = {
            'S': {('b',), ('A', 'X5'), ('X1', 'A'), ('X1', 'X4'), ('X2', 'A'), ('A', 'X3'), ('a',), ('X1', 'S')}, 
            'A': {('A', 'X6'), ('B', 'X1'), ('X2', 'S'), ('A', 'X8'), ('B', 'X7')}, 
            'B': {('A', 'X5'), ('X1', 'X4'), ('A', 'X3'), ('a',), ('X1', 'S')}, 
            'X1': {('b',)}, 
            'X2': {('a',)}, 
            'X3': {('X1', 'X4')}, 
            'X4': {('S', 'A')}, 
            'X5': {('X1', 'S')}, 
            'X6': {('B', 'X7')}, 
            'X7': {('A', 'X1')}, 
            'X8': {('B', 'X1')}
        }

        grammar_11 = grammar.Grammar(V_n, V_t, P, 'S')
        my_solution, V_N, V_T = grammar_11.to_CNF(), set(grammar_11.V_n), set(grammar_11.V_t)
        my_solution = {k: {tuple(x) for x in v} for k, v in my_solution.items()}
        self.assertDictEqual(solution, my_solution)
        self.assertSetEqual(expected_V_n, V_N)
        self.assertSetEqual(expected_V_t, V_T)


if __name__ == '__main__':
    unittest.main()