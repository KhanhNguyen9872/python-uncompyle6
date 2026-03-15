#  Copyright (c) 2024-2026 by Rocky Bernstein
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Isolate Python 3.12 version-specific semantic actions here.
"""


def customize_for_version312(self, version: tuple):
    """Add semantic table entries for Python 3.12-specific AST nodes."""

    self.TABLE_DIRECT.update(
        {
            # For loops in 3.12:
            # for312 ::= expr get_for_iter store for_block312 _come_froms END_FOR
            #             ^0       ^1         ^2      ^3           ^4        ^5
            # for312 ::= expr get_for_iter store for_block312 END_FOR
            #             ^0       ^1         ^2      ^3        ^4
            "for312": (
                "%|for %c in %c:\n%+%c%-\n\n",
                (2, "store"),
                (0, "expr"),
                (3, "for_block312"),
            ),
            "forelsestmt312": (
                "%|for %c in %c:\n%+%c%-%|else:\n%+%c%-\n\n",
                (2, "store"),
                (0, "expr"),
                (3, "for_block312"),
                -1,
            ),
            # While loops in 3.12:
            # whilestmt312 ::= _come_froms testexpr l_stmts_opt JUMP_BACK
            #                       ^0         ^1        ^2         ^3
            "whilestmt312": (
                "%|while %c:\n%+%c%-\n\n",
                (1, ("bool_op", "testexpr", "testexprc")),
                (2, ("_stmts", "l_stmts", "l_stmts_opt", "pass")),
            ),
            # whileTruestmt312 ::= _come_froms l_stmts JUMP_BACK
            #                          ^0          ^1       ^2
            "whileTruestmt312": (
                "%|while True:\n%+%c%-\n\n",
                (1, ("l_stmts", "pass")),
            ),
            # Return const
            "return_const": ("%|return %c\n", 0),
            # List with const initialization in 3.12
            # list312 ::= BUILD_LIST_0 LOAD_CONST LIST_EXTEND
            "list312": ("%C", (0, 1, "")),
            # If/else with JUMP_FORWARD
            "_ifstmts_jump312": ("%c", 0),
            # Try/except in 3.12 with JUMP_FORWARD separator
            # try_except312 ::= suite_stmts_opt JUMP_FORWARD except_handler312 ...
            "try_except312": (
                "%|try:\n%+%c%-\n%c\n\n",
                (0, ("suite_stmts_opt", "suite_stmts", "_stmts")),
                (2, "except_handler312"),
            ),
            "except_handler312": ("%c%+%c%-", 0, 1),
            "except_cond312": ("%|except %c:\n", (0, "expr")),
            "except_stmts312": ("%c", 0),
            # Inline list comprehension
            "listcomp312": ("[%c]", 2),
            "listcomp312_expr": ("[%c]", 2),
            # match/case in 3.12
            "match_stmt312": (
                "%|match %c:\n%+%c%c%c%-\n\n",
                0,  # subject expr
                1,  # first case
                2,  # mid cases
                3,  # default
            ),
        }
    )

    # Handle return_const node to print properly
    def n_return_const(node):
        const_val = node[0]
        if const_val.attr is None:
            self.write(self.indent, "return\n")
        else:
            self.write(self.indent, "return ")
            self.preorder(node[0])
            self.println("")
        self.prune()

    self.n_return_const = n_return_const

    # Handle list312 node
    def n_list312(node):
        # list312 ::= BUILD_LIST_0 LOAD_CONST LIST_EXTEND
        # list312 ::= BUILD_LIST_0 expr LIST_EXTEND
        # The LOAD_CONST contains the tuple value to convert to list
        child = node[1]
        if hasattr(child, 'attr') and isinstance(child.attr, tuple):
            # Direct tuple constant → render as list literal
            const_val = child.attr
            self.write("[")
            sep = ""
            for item in const_val:
                self.write(sep)
                self.write(repr(item))
                sep = ", "
            self.write("]")
        elif hasattr(child, 'kind') and child.kind == 'LOAD_CONST':
            # Single constant
            self.write("[")
            self.write(repr(child.attr))
            self.write("]")
        else:
            # Fallback: expr node, use preorder
            self.write("[")
            self.preorder(child)
            self.write("]")
        self.prune()

    self.n_list312 = n_list312

    # Handle match statement in 3.12
    def n_match_stmt312(node):
        # node[0] = subject expr
        # node[1] = match_case312_first
        # node[2] = match_cases312_mid (optional)
        # node[3] = match_default312 (optional)
        self.write(self.indent, "match ")
        self.preorder(node[0])
        self.println(":")
        self.indent_more()

        # First case
        self.preorder(node[1])

        # Middle cases (if any)
        for i in range(2, len(node)):
            child = node[i]
            if hasattr(child, 'kind') and child.kind in ('match_cases312_mid', 'match_case312_mid'):
                self.preorder(child)
            elif hasattr(child, 'kind') and child.kind == 'match_default312':
                self.preorder(child)

        self.indent_less()
        self.prune()

    self.n_match_stmt312 = n_match_stmt312

    # Handle first match case  
    def n_match_case312_first(node):
        # COPY expr COMPARE_OP POP_JUMP_IF_FALSE POP_TOP l_stmts_opt _jump
        # node[1] = case value expr
        # node[5] or node[6] = body (l_stmts_opt or l_stmts)
        case_val = node[1]  # the case value
        self.write(self.indent, "case ")
        self.preorder(case_val)
        self.println(":")
        self.indent_more()
        # Find body — it's the l_stmts or l_stmts_opt
        for i in range(4, len(node)):
            child = node[i]
            if hasattr(child, 'kind') and child.kind in ('l_stmts', 'l_stmts_opt',
                                                            'stmts', '_stmts'):
                self.preorder(child)
                break
        self.indent_less()
        self.prune()

    self.n_match_case312_first = n_match_case312_first

    # Handle middle match cases
    def n_match_case312_mid(node):
        # COME_FROM expr COMPARE_OP POP_JUMP_IF_FALSE l_stmts_opt _jump
        # node[1] = case value expr
        case_val = node[1]  # the case value
        self.write(self.indent, "case ")
        self.preorder(case_val)
        self.println(":")
        self.indent_more()
        # Find body
        for i in range(3, len(node)):
            child = node[i]
            if hasattr(child, 'kind') and child.kind in ('l_stmts', 'l_stmts_opt',
                                                            'stmts', '_stmts'):
                self.preorder(child)
                break
        self.indent_less()
        self.prune()

    self.n_match_case312_mid = n_match_case312_mid

    # Handle match cases container
    def n_match_cases312_mid(node):
        for child in node:
            self.preorder(child)
        self.prune()

    self.n_match_cases312_mid = n_match_cases312_mid

    # Handle match default case
    def n_match_default312(node):
        self.write(self.indent, "case _:")
        self.println("")
        self.indent_more()
        # Find body — skip COME_FROM if present
        for child in node:
            if hasattr(child, 'kind') and child.kind in ('l_stmts', 'l_stmts_opt',
                                                            'stmts', '_stmts'):
                self.preorder(child)
                break
        self.indent_less()
        self.prune()

    self.n_match_default312 = n_match_default312

    # Handle inline list comprehension
    def n_listcomp312(node):
        # listcomp312 ::= get_iter listcomp_body312 STORE_FAST STORE_NAME
        # listcomp312 ::= get_iter listcomp_body312 store store
        # listcomp312 ::= get_iter listcomp_body312 store
        # node[0] = get_iter (contains: expr GET_ITER)  
        # node[1] = listcomp_body312
        # Remaining nodes = store targets
        
        # Get the iterable from get_iter node
        get_iter_node = node[0]
        iterable = get_iter_node[0] if len(get_iter_node) > 0 else None
        
        # Get body from listcomp_body312
        body = node[1]
        
        # Find the assignment target variable name
        # Look at the last child node for STORE_NAME
        var_name = None
        for i in range(len(node) - 1, 1, -1):  # skip first 2 (get_iter, body)
            child = node[i]
            if hasattr(child, 'kind'):
                if child.kind == 'STORE_NAME':
                    var_name = child.pattr
                    break
                elif child.kind in ('store', 'STORE_FAST'):
                    # Look for pattr directly
                    if hasattr(child, 'pattr') and child.pattr:
                        var_name = child.pattr
                    # Or look inside store node for terminal
                    elif hasattr(child, '__len__') and len(child) > 0:
                        inner = child[0]
                        if hasattr(inner, 'pattr') and inner.pattr:
                            var_name = inner.pattr
                    break
        
        # Write assignment: varname = [comprehension]
        if var_name:
            self.write(self.indent, var_name, " = ")
        
        self.write("[")
        if hasattr(body, 'kind') and body.kind == 'listcomp_body312':
            # body: BUILD_LIST_0 _come_froms FOR_ITER store inner JUMP_BACK _come_froms END_FOR
            inner = body[4] if len(body) > 4 else None
            store = body[3] if len(body) > 3 else None  # loop var
            if inner and hasattr(inner, 'kind') and inner.kind == 'listcomp_inner312':
                # inner[0] = expr (the result expression)
                self.preorder(inner[0])
            self.write(" for ")
            if store:
                self.preorder(store)
            self.write(" in ")
            if iterable:
                self.preorder(iterable)
        self.write("]")
        self.println("")
        self.prune()

    self.n_listcomp312 = n_listcomp312
    self.n_listcomp312_expr = n_listcomp312

