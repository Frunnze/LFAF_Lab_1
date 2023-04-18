# Laboratory work nr. 4

### Course: Formal Languages & Finite Automata
### Author: Frunze Vladislav
### Group: FAF-212

----

## Theory:
* Chomsky Normal Form (CNF) - a simplification of a context-free grammar in which the right-side of each production is either a terminal or 2 non-terminals.

* CNF algorithm:
    1. Check if the start symbol S appears on the right side of any production. If it does, create a new start symbol S0, and add the production S0 -> S to the productions set.
    2. Eliminate the epsilon productions.
    3. Eliminate the renaming/unit productions.
    4. Eliminate non-productive non-terminals.
    5. Eliminate inaccessible terminals and non-terminals.
    6. Bring the obtained CFG to the form: A -> BC; C -> a.

* Epsilon production - production in which the right side is the empty string. In this laboratory work, it is denoted as ' '.
* Algorithm for eliminating epsilon productions:
    1. Find the epsilon production and remove it.
    2. Go through each production and find the productions where the right-side contains the left-side of the removed epsilon production.
    3. Derive from the found production all the productions with and without the left-side non-terminal of the removed epsilon production.
    Example: P = {A -> '', B -> AC}, P' = {B -> AC, B -> C}
    4. Repeat 1-3 until there are no epsilon productions.

* Renaming / unit production - production in which the left-side is a non-terminal, and the right-side is also a non-terminal, but different than the left-side one. Example: B -> A.
* Algorithm for eliminating unit productions:
    1. Find the unit production.
    2. Replace the right-side non-terminal with its own right-side productions, that is, the right-sides where it is on the left-side.
    3. If the left-side of the unit production is also a right-side for the right-side in the unit production, then you remove every production with the right-side in the unit production on the left. Also, you remove the left-side of the unit production that will appear when replacing at step 2. In this way, we eliminate the cycles.

* Non-productives - non-terminals that do not generate a string of just terminals.
* Algorithm for eliminating non-productives:
    1. Add the left-side non-terminals of the productions where the right-side is a terminal to the productives set.
    2. If some or all non-terminals, but only them, in the above productives set are found in a right-side of a production, then you add to the productives set the left non-terminal, and go to the first production.
    3. Repeat step 2 until you get to the last production.
    4. Find the set non-productives = non-terminals - productives.
    5. Eliminate every production where any of the non-productives are found.

* Inaccessibles - terminals or non-terminals which cannot be accessed or found from the start symbol.
* Algorithm for eliminating inaccessible symbols:
    1. Initialize the accessibles set with the start symbol.
    2. Add to the accessibles set every symbol of the right-side in the productions where the left-side is a non-terminal in the set.
    3. If there appear other non-terminals in the accessibles set, repeat step 2.
    4. Form the inaccessibles = (terminals + non-terminals) - accessibles 
    5. Eliminate every production where any of the inaccessibles are found.

## Implementation description:
#### My grammar (11).
```
        V_n = ['S', 'A', 'B', 'C', 'D']
        V_t = ['a', 'b']
        P = {
            'S': ['bA', 'AC'],
            'A': ['bS', 'BC', 'AbAa'],
            'B': ['BbaA', 'a', 'bSa'],
            'C': [''],
            'D': ['AB']
        }
```

#### Method to eliminate epsilon productions:
First, we enter a "while" loop which is going to stop only if there are no epsilon productions in the production set. In the loop, the first task is to find the epsilon production, delete it, and remember in the "N_eps" variable the left side non-terminal of the found epsilon production.

```
        while N_eps != None:
            N_eps = None
            for left_side in self.P.keys():
                for right_side in self.P[left_side]:
                    if '' == right_side:
                        # Delete the epsilon productions, if found.
                        self.P[left_side].remove(right_side)
                        N_eps = left_side
                        break
                if N_eps and len(self.P[N_eps]) == 0:
                    del self.P[left_side]
                    break
```

Next, in the same loop, we have to add new productions to offset the epsilon elimination. Thus, we go through each production to find the ones which contain "N_eps" on the right side. If we find such a production, we find all indices where the "N_eps" occurs on the right side, generate all possible combinations of the indices where "N_eps" occurs, and generate all possible productions with or without "N_eps" based on the combinations.
<br/>
```
            if N_eps:
                copy_P = {k: list(v) for k, v in self.P.items()}
                for left_side in self.P.keys():
                    for right_side in self.P[left_side]:
                        if N_eps in right_side:
                            indices = [i for i, char in enumerate(right_side) if char == N_eps]
                            combinations = []
                            for i in range(1, len(indices) + 1):
                                for combination in itertools.combinations(indices, i):
                                    combinations.append(combination)
                            new_productions = []
                            for combination in combinations:
                                temp = right_side
                                for i in combination[::-1]:
                                    temp = temp[:i] + temp[i+1:]
                                new_productions.append(temp)
                            copy_P[left_side].extend(list(dict.fromkeys(new_productions)))
                self.P = {k: list(v) for k, v in copy_P.items()}
```

#### Method to eliminate renamings:
First, in the productions dictionary, we go through each key (left side non-terminal of the production) and each item (right side of the production) of the key's list. We go through the mentioned list in a loop until there are no non-terminal items in it. If an item is the same as the key, we delete the item from the list. If the item is a different non-terminal, we have two cases non-cyclic and cyclic. In the first one, if the item is also key in the dictionary, we replace the item with its own items, otherwise, we just delete it. In the second case, if one of the items of the current item is equal to the current key then we delete this item, replace the current item with its items, and delete the key of the current item.

```
        for left_side in self.P.keys():
            unit_prod = True
            while unit_prod:
                unit_prod = False
                for right_side in self.P[left_side]:
                    if right_side == left_side:
                        self.P[left_side].remove(right_side)
                        unit_prod = True
                    elif right_side in self.V_n:
                        unit_prod = True
                        if right_side not in self.P.keys():
                            self.P[left_side].remove(right_side)
                        elif left_side not in self.P[right_side]:
                            self.P[left_side].remove(right_side)
                            self.P[left_side] += self.P[right_side]
                        elif left_side in self.P[right_side]:
                            while left_side in self.P[right_side]:
                                self.P[right_side].remove(left_side)
                            self.P[left_side].remove(right_side)
                            self.P[left_side] += self.P[right_side]
                            self.P[right_side] = []
                            keys_to_delete.append(right_side)
            self.P[left_side] = list(dict.fromkeys(self.P[left_side]))
        for key in list(self.P.keys()):
            if len(self.P[key]) == 0 or key in keys_to_delete:
                del self.P[key]
```

#### Method to eliminate non-productive in a CFG:
First, we add the left-side non-terminals of the productions where the right-side is a terminal to the productives set.
```
        for left_side in self.P.keys():
            for right_side in self.P[left_side]:
                if right_side in self.V_t:
                    prod.append(left_side)
                    break
```

Second, go through each production. If the right side of the production contains just non-terminals from the productives set, then you add the left side non-terminal to the productives set, if it's not already there. Next, go through the productions dictionary from the beginning, with the updated productives set. This is going to continue until the algorithm gets to the last production.
<br/>
```
        while prod_found:
            prod_found = False
            for left_side in self.P.keys():
                if left_side not in prod:
                    for right_side in self.P[left_side]:
                        count = 0
                        for symbol in right_side:
                            if symbol in self.V_n and symbol not in prod:
                                break
                            count += 1
                        if count == len(right_side):
                            prod.append(left_side)
                            prod_found = True
                            break
                    if prod_found:
                        break
```

Find the set non-productives = non-terminals - productives, and, finally, eliminate every production where any of the non-productives are found.
<br/>
```
        non_prod = list(set(self.V_n) - set(prod))
        for left_side in self.P.keys():
            temp_list = self.P[left_side][:]
            for right_side in self.P[left_side]:
                if any(symbol in right_side for symbol in non_prod):
                    temp_list.remove(right_side)
            self.P[left_side] = temp_list
        for key in non_prod:
            if key in self.P.keys():
                del self.P[key]
        self.V_n = prod
```

#### Method to eliminate inaccessible symbols in a CFG:
Initialize the access list with the start symbol. Add to the accessibles list every symbol of the right side in the productions where the left side is a non-terminal in the list. Determine the inaccessibles list (terminals + non-terminals - accessibles) and delete them from V_n and V_t lists. Delete the keys of the dictionary that are non-terminals in the inaccessibles list. Eliminate every production where any of the inaccessibles are found.

```
        acces = [self.S]
        for symbol in acces:
            if symbol in self.P.keys():
                for right_side in self.P[symbol]:
                    for s in list(right_side):
                        if s not in acces:
                            acces.append(s)

        inacces = list(set(self.V_n + self.V_t) - set(acces))
        self.V_n = [s for s in self.V_n if s not in inacces]
        self.V_t = [s for s in self.V_t if s not in inacces]

        for key in inacces:
            if key in self.P.keys():
                del self.P[key]
        
        for left_side in self.P.keys():
            temp_list = self.P[left_side][:]
            for right_side in self.P[left_side]:
                if any(symbol in right_side for symbol in inacces):
                    temp_list.remove(right_side)
            self.P[left_side] = temp_list
```

#### Method to translate a CFG into the Chomsky Normal Form:

Check if the start symbol S appears on the right side of any production. If it does, create a new start symbol S0, and add the production S0 -> S to the productions set. Also, apply the previously prepared methods.

```
        for left_side in list(self.P.keys()):
            for right_side in self.P[left_side]:
                if right_side == self.S:
                    self.S = 'S0'
                    self.V_n.append('S0')
                    self.P['S0'] = ['S']
                    break
        self.eliminate_eps()
        self.eliminate_renaming()
        self.eliminate_non_productive()
        self.eliminate_inaccessibles()
```

Go through each production except the ones where the right side is just a terminal. Go through each symbol of the right side of the production. Replace the terminal with a new non-terminal and add the last to the productions set.
<br/>
```
        self.P = {k: [list(prod) for prod in v] for k, v in self.P.items()}
        temp_dict = {k: '' for k in self.V_t}
        new_non_terminal = 0
        for left_side in list(self.P.keys()):
            for index, right_side in enumerate(self.P[left_side]):
                if len(right_side) > 1:
                    for i, s in enumerate(right_side):
                        if s in self.V_t:
                            if temp_dict[s] == '':
                                new_non_terminal += 1
                                new_NT = 'X' + str(new_non_terminal)
                                self.P[new_NT] = [[s]]
                                temp_dict[s] = new_NT
                                self.V_n.append(new_NT)
                            else:
                                new_NT = temp_dict[s]
                            self.P[left_side][index][i] = new_NT
```

Go through the productions dictionary. If the right side has more than 2 non-terminals, leave the first non-terminal but replace the rest with a new non-terminal or a new non-terminal created previously with its first value equal to the rest of the right side. If the last does not exist, add the new non-terminal to the productions dictionary with the value as the replaced part.
<br/>
```
        keys_list = list(self.P.keys())
        x_dict = {}
        for left_side in keys_list:
            for index, right_side in enumerate(self.P[left_side]):
                if len(right_side) > 2:
                    new_NT = None
                    for x, v in x_dict.items():
                        if v == self.P[left_side][index][1:]:
                            new_NT = x
                            break
                    if new_NT:
                        del self.P[left_side][index][1:]
                        self.P[left_side][index].append(new_NT)
                    else:
                        new_non_terminal += 1
                        new_NT = 'X' + str(new_non_terminal)
                        self.P[new_NT] = [self.P[left_side][index][1:]]
                        x_dict[new_NT] = self.P[left_side][index][1:]
                        self.V_n.append(new_NT)
                        del self.P[left_side][index][1:]
                        self.P[left_side][index].append(new_NT)
                        keys_list.append(new_NT)
```

## Conclusions / Screenshots / Results
### Results:
Unit tests:
The main file "main_lab_4.py" contains 16 unit tests. You can access it through the path: "LFAF_Labs/src/main_lab_4.py".

It outputs:
```
................
----------------------------------------------------------------------
Ran 16 tests in 0.001s

OK
```

The obtained CNF for my grammar (11):
```
V_n = {'S', 'A', 'B', 'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7'}
V_t = {'a', 'b'}
P = {
    'S': [['X1', 'A'], ['X1', 'S'], ['A', 'X3'], ['B', 'X4'], ['a'], ['X1', 'X5']], 
    'A': [['X1', 'S'], ['A', 'X3'], ['B', 'X4'], ['a'], ['X1', 'X5']], 
    'B': [['B', 'X4'], ['a'], ['X1', 'X5']], 
    'X1': [['b']], 
    'X2': [['a']], 
    'X3': [['X1', 'X6']], 
    'X4': [['X1', 'X7']], 
    'X5': [['S', 'X2']], 
    'X6': [['A', 'X2']], 
    'X7': [['X2', 'A']]
}
```

### Conclusions
* Chomsky Normal Form can simplify the use of a Context-Free Grammar significantly.
* Every CFG can be converted to an equivalent CNF.
* CNFs do not have epsilon or unit productions.
* The CNF method can output different outputs for different implementations, however, the generated strings must be the same.

## References
1. Cojuhari I., Duca L., & Fiodorov I. Formal Languages and Finite Automata Guide for practical lessons. Technical University of Moldova
2. "Chomsky Normal Form" Wikipedia: https://en.wikipedia.org/wiki/Chomsky_normal_form