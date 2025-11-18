"""
Proyecto LFC - Gramáticas LL(1) y SLR(1)
Integrantes: Mariana Sanchez, Sebastian Cañon
"""

class Grammar:
    
    def __init__(self, productions):
        self.productions = productions
        self.nonterminals = set()
        self.terminals = set()
        
        # Extract terminals and nonterminals
        for nt, prods in self.productions.items():
            self.nonterminals.add(nt)
            for prod in prods:
                for symbol in prod:
                    if symbol.isupper():
                        self.nonterminals.add(symbol)
                    elif symbol != 'e':
                        self.terminals.add(symbol)
        
        # Add end-of-input marker
        self.terminals.add('$')
        
        self.first_sets = {}
        self.follow_sets = {}
        self.compute_first_sets()
        self.compute_follow_sets()
    
    def compute_first_sets(self):
        """Compute FIRST sets for all nonterminals and terminals"""
        
        # Initialize FIRST sets
        for nt in self.nonterminals:
            self.first_sets[nt] = set()
        
        # Initialize FIRST sets for terminals
        for t in self.terminals:
            self.first_sets[t] = {t}
        
        # Special case for epsilon
        self.first_sets['e'] = {'e'}
        
        # Compute FIRST sets
        changed = True
        while changed:
            changed = False
            for nt, prods in self.productions.items():
                for prod in prods:
                    # If production is epsilon, add epsilon to FIRST
                    if len(prod) == 1 and prod[0] == 'e':
                        if 'e' not in self.first_sets[nt]:
                            self.first_sets[nt].add('e')
                            changed = True
                        continue
                    
                    # For each symbol in the production
                    curr_idx = 0
                    can_derive_epsilon = True
                    
                    while curr_idx < len(prod) and can_derive_epsilon:
                        symbol = prod[curr_idx]
                        can_derive_epsilon = False
                        
                        # If symbol is a terminal
                        if not symbol.isupper():
                            if symbol != 'e':
                                if symbol not in self.first_sets[nt]:
                                    self.first_sets[nt].add(symbol)
                                    changed = True
                            break
                        
                        # Symbol is a nonterminal
                        # Add all non-epsilon terminals from FIRST(symbol) to FIRST(nt)
                        for s in self.first_sets[symbol]:
                            if s != 'e' and s not in self.first_sets[nt]:
                                self.first_sets[nt].add(s)
                                changed = True
                        
                        # Check if symbol can derive epsilon
                        if 'e' in self.first_sets[symbol]:
                            can_derive_epsilon = True
                            curr_idx += 1
                    
                    # If all symbols can derive epsilon, add epsilon to FIRST(nt)
                    if curr_idx == len(prod) and can_derive_epsilon:
                        if 'e' not in self.first_sets[nt]:
                            self.first_sets[nt].add('e')
                            changed = True
    
    def first_of_string(self, string):
        """Compute FIRST set for a string of symbols"""
        
        if not string or (len(string) == 1 and string[0] == 'e'):
            return {'e'}
        
        result = set()
        curr_idx = 0
        can_derive_epsilon = True
        
        while curr_idx < len(string) and can_derive_epsilon:
            symbol = string[curr_idx]
            can_derive_epsilon = False
            
            # Add all non-epsilon terminals from FIRST(symbol) to result
            if symbol in self.first_sets:
                for s in self.first_sets[symbol]:
                    if s != 'e':
                        result.add(s)
            
            # Check if symbol can derive epsilon
            if symbol in self.first_sets and 'e' in self.first_sets[symbol]:
                can_derive_epsilon = True
                curr_idx += 1
        
        # If all symbols can derive epsilon, add epsilon to result
        if curr_idx == len(string) and can_derive_epsilon:
            result.add('e')
        
        return result
    
    def compute_follow_sets(self):
        """Compute FOLLOW sets for all nonterminals"""
        
        # Initialize FOLLOW sets
        for nt in self.nonterminals:
            self.follow_sets[nt] = set()
        
        # Start symbol has $ in its FOLLOW set
        self.follow_sets['S'].add('$')
        
        # Compute FOLLOW sets
        changed = True
        while changed:
            changed = False
            for nt, prods in self.productions.items():
                for prod in prods:
                    if len(prod) == 1 and prod[0] == 'e':  # Skip epsilon productions
                        continue
                    
                    # Process each symbol in the production
                    for i, symbol in enumerate(prod):
                        if symbol in self.nonterminals:  # Only interested in nonterminals
                            # Compute FIRST set of the rest of the production
                            beta = prod[i+1:] if i < len(prod) - 1 else []
                            if not beta:
                                first_beta = {'e'}
                            else:
                                first_beta = self.first_of_string(beta)
                            
                            # Add all non-epsilon symbols from FIRST(beta) to FOLLOW(symbol)
                            for s in first_beta:
                                if s != 'e' and s not in self.follow_sets[symbol]:
                                    self.follow_sets[symbol].add(s)
                                    changed = True
                            
                            # If epsilon is in FIRST(beta), add all of FOLLOW(nt) to FOLLOW(symbol)
                            if 'e' in first_beta:
                                for s in self.follow_sets[nt]:
                                    if s not in self.follow_sets[symbol]:
                                        self.follow_sets[symbol].add(s)
                                        changed = True
    
    def check_ll1(self):
        """Check if grammar is LL(1)"""
        
        # Create parsing table
        table = {}
        for nt in self.nonterminals:
            table[nt] = {}
        
        # Try to fill the parsing table without conflicts
        for nt, prods in self.productions.items():
            for i, prod in enumerate(prods):
                first_prod = self.first_of_string(prod)
                
                # For each terminal in FIRST(prod)
                for terminal in first_prod - {'e'}:
                    if terminal in table[nt]:
                        # Conflict detected
                        return False
                    table[nt][terminal] = i
                
                # If epsilon is in FIRST(prod), add entries for terminals in FOLLOW(nt)
                if 'e' in first_prod:
                    for terminal in self.follow_sets[nt]:
                        if terminal in table[nt]:
                            # Conflict detected
                            return False
                        table[nt][terminal] = i
        
        return True
    
    def parse_ll1(self, input_string):
        """Parse a string using LL(1) algorithm"""
        
        # Create parsing table
        table = {}
        for nt in self.nonterminals:
            table[nt] = {}
        
        # Fill the parsing table
        for nt, prods in self.productions.items():
            for i, prod in enumerate(prods):
                first_prod = self.first_of_string(prod)
                
                # For each terminal in FIRST(prod)
                for terminal in first_prod - {'e'}:
                    table[nt][terminal] = (i, prod)
                
                # If epsilon is in FIRST(prod), add entries for terminals in FOLLOW(nt)
                if 'e' in first_prod:
                    for terminal in self.follow_sets[nt]:
                        table[nt][terminal] = (i, prod)
        
        # Add end marker if not present
        if input_string and input_string[-1] != '$':
            input_string = input_string + '$'
        elif not input_string:
            input_string = '$'
        
        # Initialize stack with end marker and start symbol
        stack = ['$', 'S']
        position = 0
        
        # Start parsing
        while stack:
            top = stack[-1]
            
            # Get current input symbol
            current = input_string[position] if position < len(input_string) else '$'
            
            # If top is a terminal or $
            if top not in self.nonterminals:
                if top == current:
                    stack.pop()
                    position += 1
                    if top == '$':
                        return position == len(input_string)
                else:
                    return False  # Mismatch
            
            # Top is a nonterminal
            elif current in table[top]:
                prod_idx, prod = table[top][current]
                stack.pop()
                
                # Push production in reverse order
                if not (len(prod) == 1 and prod[0] == 'e'):  # Skip epsilon
                    for symbol in reversed(prod):
                        stack.append(symbol)
            else:
                return False  # No production found
        
        return position == len(input_string)
    
    def check_slr1(self):
        """Check if grammar is SLR(1)"""
        
        try:
            # Get augmented grammar
            augmented_prods = self.productions.copy()
            augmented_prods["S'"] = [['S']]
            
            # Get canonical collection of LR(0) items
            items = []
            goto = {}
            
            # Initialize with the closure of {S' -> .S}
            initial_item = ("S'", 0, 0)
            initial_state = self._closure({initial_item}, augmented_prods, set(self.nonterminals) | {"S'"})
            items.append(initial_state)
            
            # Build the canonical collection
            i = 0
            while i < len(items):
                state = items[i]
                
                # Find symbols after the dot in this state
                symbols = set()
                for nt, prod_idx, dot_pos in state:
                    if dot_pos < len(augmented_prods[nt][prod_idx]):
                        symbol = augmented_prods[nt][prod_idx][dot_pos]
                        if not (symbol == 'e'):  # Skip epsilon
                            symbols.add(symbol)
                
                # Process each symbol
                for symbol in symbols:
                    # Get the next state using GOTO
                    next_state = set()
                    for nt, prod_idx, dot_pos in state:
                        if (dot_pos < len(augmented_prods[nt][prod_idx]) and 
                            augmented_prods[nt][prod_idx][dot_pos] == symbol):
                            next_state.add((nt, prod_idx, dot_pos + 1))
                    
                    # Get closure of the next state
                    next_state = self._closure(next_state, augmented_prods, set(self.nonterminals) | {"S'"})
                    
                    # Add next_state to items if it's new
                    if next_state:
                        if next_state not in items:
                            items.append(next_state)
                            goto[(i, symbol)] = len(items) - 1
                        else:
                            goto[(i, symbol)] = items.index(next_state)
                
                i += 1
            
            # Create parsing table
            action = {}
            for i in range(len(items)):
                action[i] = {}
            
            # Set up shift and goto actions
            for (state_idx, symbol), next_state in goto.items():
                if symbol in self.terminals:
                    action[state_idx][symbol] = ('shift', next_state)
            
            # Set up reduce actions
            for i, state in enumerate(items):
                for nt, prod_idx, dot_pos in state:
                    # If the item is [A -> α.] (dot at the end), add reduce action
                    if nt != "S'" and dot_pos == len(augmented_prods[nt][prod_idx]):
                        for terminal in self.follow_sets[nt]:
                            # Check for conflicts
                            if terminal in action[i]:
                                return False  # Conflict detected
                            action[i][terminal] = ('reduce', (nt, prod_idx))
                    
                    # If the item is [S' -> S.], add accept action
                    if nt == "S'" and dot_pos == 1:
                        if '$' in action[i]:
                            return False  # Conflict
                        action[i]['$'] = ('accept', None)
            
            return True
            
        except:
            return False
    
    def _closure(self, items, augmented_prods, all_nonterminals):
        """Compute closure of a set of LR(0) items"""
        result = set(items)
        
        changed = True
        while changed:
            changed = False
            new_items = set()
            
            for nt, prod_idx, dot_pos in result:
                # If dot is before a nonterminal
                if dot_pos < len(augmented_prods[nt][prod_idx]):
                    next_symbol = augmented_prods[nt][prod_idx][dot_pos]
                    if next_symbol in all_nonterminals:
                        # Add productions of this nonterminal to the closure
                        if next_symbol in augmented_prods:
                            for i, prod in enumerate(augmented_prods[next_symbol]):
                                new_item = (next_symbol, i, 0)
                                if new_item not in result:
                                    new_items.add(new_item)
                                    changed = True
            
            result.update(new_items)
        
        return result
    
    def parse_slr1(self, input_string):
        """Parse a string using SLR(1) algorithm"""
        try:
            # Get augmented grammar
            augmented_prods = self.productions.copy()
            augmented_prods["S'"] = [['S']]
            
            # Get canonical collection
            items = []
            goto = {}
            
            # Initialize with the closure of {S' -> .S}
            initial_item = ("S'", 0, 0)
            initial_state = self._closure({initial_item}, augmented_prods, set(self.nonterminals) | {"S'"})
            items.append(initial_state)
            
            # Build the canonical collection
            i = 0
            while i < len(items):
                state = items[i]
                
                # Find symbols after the dot in this state
                symbols = set()
                for nt, prod_idx, dot_pos in state:
                    if dot_pos < len(augmented_prods[nt][prod_idx]):
                        symbol = augmented_prods[nt][prod_idx][dot_pos]
                        if not (symbol == 'e'):
                            symbols.add(symbol)
                
                # Process each symbol
                for symbol in symbols:
                    # Get the next state using GOTO
                    next_state = set()
                    for nt, prod_idx, dot_pos in state:
                        if (dot_pos < len(augmented_prods[nt][prod_idx]) and 
                            augmented_prods[nt][prod_idx][dot_pos] == symbol):
                            next_state.add((nt, prod_idx, dot_pos + 1))
                    
                    # Get closure of the next state
                    next_state = self._closure(next_state, augmented_prods, set(self.nonterminals) | {"S'"})
                    
                    # Add next_state to items if it's new
                    if next_state:
                        if next_state not in items:
                            items.append(next_state)
                            goto[(i, symbol)] = len(items) - 1
                        else:
                            goto[(i, symbol)] = items.index(next_state)
                
                i += 1
            
            # Create parsing table
            action = {}
            goto_table = {}
            for i in range(len(items)):
                action[i] = {}
                goto_table[i] = {}
            
            # Set up shift and goto actions
            for (state_idx, symbol), next_state in goto.items():
                if symbol in self.terminals:
                    action[state_idx][symbol] = ('shift', next_state)
                else:
                    goto_table[state_idx][symbol] = next_state
            
            # Set up reduce actions
            for i, state in enumerate(items):
                for nt, prod_idx, dot_pos in state:
                    # If the item is [A -> α.] (dot at the end), add reduce action
                    if nt != "S'" and dot_pos == len(augmented_prods[nt][prod_idx]):
                        for terminal in self.follow_sets[nt]:
                            action[i][terminal] = ('reduce', (nt, prod_idx))
                    
                    # If the item is [S' -> S.], add accept action
                    if nt == "S'" and dot_pos == 1:
                        action[i]['$'] = ('accept', None)
            
            # Add end marker if not present
            if input_string and input_string[-1] != '$':
                input_string = input_string + '$'
            elif not input_string:
                input_string = '$'
            
            # Parse input
            stack = [0]  # Start with state 0
            position = 0
            
            while True:
                current_state = stack[-1]
                current_symbol = input_string[position] if position < len(input_string) else '$'
                
                if current_symbol not in action[current_state]:
                    return False
                
                act, value = action[current_state][current_symbol]
                
                if act == 'shift':
                    stack.append(current_symbol)
                    stack.append(value)
                    position += 1
                elif act == 'reduce':
                    nt, prod_idx = value
                    prod = augmented_prods[nt][prod_idx]
                    
                    # Pop 2 * len(prod) items from stack (symbol and state for each symbol)
                    if not (len(prod) == 1 and prod[0] == 'e'):
                        stack = stack[:-2*len(prod)]
                    
                    # Get current state after popping
                    current_state = stack[-1]
                    
                    # Push nonterminal and goto state
                    if nt not in goto_table[current_state]:
                        return False
                    stack.append(nt)
                    stack.append(goto_table[current_state][nt])
                elif act == 'accept':
                    return True
                else:
                    return False
            
        except Exception as e:
            return False


def parse_grammar():
    """Parse grammar from user input"""
    
    # Read number of nonterminals
    n = int(input())
    
    productions = {}
    
    # Read productions
    for _ in range(n):
        line = input().strip()
        parts = line.split(' -> ')
        nt = parts[0]
        rules = parts[1].split()
        
        if nt not in productions:
            productions[nt] = []
        
        for rule in rules:
            productions[nt].append(list(rule))
    
    return Grammar(productions)


def parse_strings(grammar, parser_type):
    """Parse strings using the specified parser"""
    
    while True:
        try:
            string = input()
            if not string:
                break
            
            if parser_type == 'LL1':
                result = grammar.parse_ll1(string)
            else:  # SLR1
                result = grammar.parse_slr1(string)
            
            print("yes" if result else "no")
        except EOFError:
            break


def main():
    """Main function"""
    
    grammar = parse_grammar()
    
    # Check if grammar is LL(1) and/or SLR(1)
    is_ll1 = grammar.check_ll1()
    is_slr1 = grammar.check_slr1()
    
    if is_ll1 and is_slr1:
        print("Select a parser (T: for LL(1), B: for SLR(1), Q: quit):")
        
        while True:
            try:
                choice = input().strip().upper()
                if choice == 'T':
                    parse_strings(grammar, 'LL1')
                    print("Select a parser (T: for LL(1), B: for SLR(1), Q: quit):")
                elif choice == 'B':
                    parse_strings(grammar, 'SLR1')
                    print("Select a parser (T: for LL(1), B: for SLR(1), Q: quit):")
                elif choice == 'Q':
                    break
            except EOFError:
                break
    elif is_ll1:
        print("Grammar is LL(1).")
        parse_strings(grammar, 'LL1')
    elif is_slr1:
        print("Grammar is SLR(1).")
        parse_strings(grammar, 'SLR1')
    else:
        print("Grammar is neither LL(1) nor SLR(1).")


if __name__ == "__main__":
    main()