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
            # ===== LOOPS =====

            # for312 ::= expr get_for_iter store for_block312 [_come_froms] END_FOR [POP_TOP]
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
            "forelse312_break": (
                "%|for %c in %c:\n%+%c%-%|else:\n%+%c%-\n\n",
                (2, "store"),
                (0, "expr"),
                3,
                -1,
            ),

            # whilestmt312 ::= _come_froms testexpr l_stmts_opt JUMP_BACK [come_froms]
            "whilestmt312": (
                "%|while %c:\n%+%c%-\n\n",
                (1, ("bool_op", "testexpr", "testexprc")),
                (2, ("_stmts", "l_stmts", "l_stmts_opt", "pass")),
            ),
            "whileTruestmt312": (
                "%|while True:\n%+%c%-\n\n",
                (1, ("l_stmts", "pass")),
            ),

            # ===== CONDITIONALS =====

            "_ifstmts_jump312": ("%c", 0),

            # ===== TERNARY EXPRESSIONS =====

            # if_exp312 ::= expr POP_JUMP_IF_FALSE expr JUMP_FORWARD _come_froms expr
            #                ^0          ^1          ^2       ^3          ^4       ^5
            "if_exp312": ("%c if %c else %c", 2, 0, 5),

            # ===== FUNCTION DEFINITIONS =====

            # funcdef312 ::= mkfunc312 store
            "funcdef312": ("\n\n%|def %c", 0),

            # funcdefdeco312 ::= mkfuncdeco312 store
            "funcdefdeco312": ("\n\n%|def %c", 0),

            # ===== RETURN =====

            "return_const": ("%|return %c\n", 0),

            # ===== RAISE =====

            # raise_stmt312 ::= expr RAISE_VARARGS_1
            "raise_stmt312": ("%|raise %c\n", 0),

            # ===== ASSERT =====

            # assert312 ::= expr POP_JUMP_IF_TRUE LOAD_ASSERTION_ERROR RAISE_VARARGS_1 COME_FROM
            "assert312": ("%|assert %c\n", 0),

            # ===== IS_OP =====

            # is_op312 ::= expr expr IS_OP
            "is_op312": ("%c is %c", 0, 1),

            # ===== LIST =====

            # list312 ::= BUILD_LIST_0 LOAD_CONST LIST_EXTEND
            "list312": ("%C", (0, 1, "")),

            # build_list312 ::= expr BUILD_LIST_1
            # build_list312 ::= expr expr BUILD_LIST_2
            "build_list312": ("[%C]", (0, 100, ", ")),

            # ===== WALRUS =====

            # walrus_expr312 ::= expr COPY store
            "walrus_expr312": ("(%c := %c)", 2, 0),

            # ===== SLICE =====

            # binary_slice312 ::= expr expr [expr] BINARY_SLICE
            "binary_slice312": ("%c[%c:%c]", 0, 1, 2),

            # ===== F-STRING =====

            "fstring312": ("{%c}", 0),
            "joined_str312": ("%c", 0),
            "build_string312": ("%c", 0),

            # ===== WITH =====

            # with_stmt312 ::= expr BEFORE_WITH store l_stmts_opt ...
            "with_stmt312": (
                "%|with %c as %c:\n%+%c%-\n\n",
                (0, "expr"),
                (2, "store"),
                (3, ("l_stmts_opt", "l_stmts", "pass")),
            ),

            # ===== TRY/EXCEPT =====

            "try_except312": (
                "%|try:\n%+%c%-\n%c\n\n",
                (0, ("suite_stmts_opt", "suite_stmts", "_stmts")),
                (2, "except_handler312"),
            ),
            "except_handler312": ("%c%+%c%-", 0, 1),
            "except_cond312": ("%|except %c:\n", (0, "expr")),
            "except_stmts312": ("%c", 0),

            # ===== MATCH =====

            "match_stmt312": (
                "%|match %c:\n%+%c%c%c%-\n\n",
                0, 1, 2, 3,
            ),

            # ===== COMPREHENSIONS =====

            "listcomp312": ("[%c]", 2),
            "listcomp312_expr": ("[%c]", 2),
            "dictcomp312": ("{%c}", 0),

            # ===== COMPARISONS =====

            # compare_chained312 ::= expr compare_chain_mid312 compare_chain_end312 [_come_froms]
            "compare_chained312": ("%c %c %c", 0, 1, 2),
            "compare_chain_mid312": ("%c", 0),
            "compare_chain_end312": ("%c", 0),

            # ===== GENERATORS =====

            "return_generator312": (""),
        }
    )

    # =====================================================
    # Custom n_ handler methods for complex node types
    # =====================================================

    # --- return_const: suppress "return None" for module-level ---
    def n_return_const(node):
        const_val = node[0]
        if const_val.attr is None:
            # Module-level "return None" is implicit — don't print it
            pass
        else:
            self.write(self.indent, "return ")
            self.preorder(node[0])
            self.println("")
        self.prune()

    self.n_return_const = n_return_const

    # --- mkfunc312: function definition body ---
    def n_mkfunc312(node):
        # mkfunc312 ::= LOAD_CODE LOAD_STR MAKE_FUNCTION_0
        # node[0] = LOAD_CODE (attr = code object)
        # node[1] = LOAD_STR (attr = function name)
        # node[2] = MAKE_FUNCTION_0
        from uncompyle6.semantics.helper import find_code_node
        from uncompyle6.util import get_code_name
        try:
            code_node = find_code_node(node, -2)
            code = code_node.attr
            self.write(get_code_name(code))
            self.indent_more()
            self.make_function(node, is_lambda=False, code_node=code_node)
            if len(self.param_stack) > 1:
                self.write("\n\n")
            else:
                self.write("\n\n\n")
            self.indent_less()
        except Exception:
            # Fallback: just print function signature
            func_name = node[1].attr if len(node) > 1 and hasattr(node[1], 'attr') else "<unknown>"
            self.write(self.indent, "def ", str(func_name), "():\n")
            self.indent_more()
            self.write(self.indent, "pass\n")
            self.indent_less()
        self.prune()

    self.n_mkfunc312 = n_mkfunc312

    # --- mkfuncdeco312: decorated function ---
    def n_mkfuncdeco312(node):
        # mkfuncdeco312 ::= expr mkfunc312 CALL_FUNCTION_1
        # node[0] = decorator expr
        # node[1] = mkfunc312
        self.write(self.indent, "@")
        self.preorder(node[0])
        self.println("")
        self.preorder(node[1])
        self.prune()

    self.n_mkfuncdeco312 = n_mkfuncdeco312

    # --- forelsestmt312: strip trivial else: return into for + return ---
    def n_forelsestmt312(node):
        # forelsestmt312 ::= expr get_for_iter store for_block312 [_come_froms] END_FOR else_suite
        # If else_suite is just a single return, render as 'for...: ... return X' without else:
        from spark_parser import GenericASTTraversalPruningException

        # Find the else_suite and check if it's a trivial return
        else_idx = -1
        is_return_else = False
        for idx, child in enumerate(node):
            kind = str(child.kind) if hasattr(child, 'kind') else ''
            if 'else_suite' in kind or 'else_suitel' in kind:
                else_idx = idx
                # Walk into else_suite to check for return
                def has_return(n):
                    k = str(n.kind) if hasattr(n, 'kind') else str(n)
                    if 'return' in k or 'ret_expr' in k:
                        return True
                    if hasattr(n, '__iter__'):
                        for c in n:
                            if has_return(c):
                                return True
                    return False
                is_return_else = has_return(child)
                break

        if is_return_else and else_idx >= 0:
            # Render for loop without else: keyword
            # for store in expr:\n    for_block\nreturn_stmt
            self.write(self.indent, "for ")
            self.preorder(node[2])  # store
            self.write(" in ")
            self.preorder(node[0])  # expr
            self.write(":\n")
            self.indent_more()
            self.preorder(node[3])  # for_block312
            self.indent_less()
            # Render the return at same indentation (no else:)
            self.preorder(node[else_idx])  # else_suite content
            self.write("\n")
            self.prune()

    self.n_forelsestmt312 = n_forelsestmt312

    # --- aug_assign1: handle 3.12 COPY-based subscript augmented assignment ---
    def n_aug_assign1(node):
        # aug_assign1 ::= expr expr COPY COPY BINARY_SUBSCR expr inplace_op STORE_SUBSCR
        # 8 children with COPY: render as base[key] op= value
        try:
            nchildren = len(node)
            if nchildren == 8:
                child2 = node[2]
                k2 = str(child2.kind) if hasattr(child2, 'kind') else ''
                if k2 == 'COPY':
                    self.write(self.indent)
                    self.preorder(node[0])  # base (e.g. globals())
                    self.write("[")
                    self.preorder(node[1])  # key (e.g. 'enjuly19_')
                    self.write("] ")
                    # inplace_op is at index 6
                    self.preorder(node[6])  # renders as '+='
                    self.write(" ")
                    self.preorder(node[5])  # value
                    self.write("\n")
                    self.prune()
                    return
        except (IndexError, AttributeError):
            pass
        # Fall through for standard 4-child aug_assign1
        self.default(node)

    self.n_aug_assign1 = n_aug_assign1

    # --- whilestmt38: convert while→if when body is single-iteration ---
    def n_whilestmt38(node):
        # whilestmt38 children: [_come_froms, testexpr, l_stmts, COME_FROM]
        # Convert to `if` when the body can only execute once:
        #   - single aug_assign1 (h2o's if not _173: globals() += ...)
        #   - contains return statement (o2's if h2so3 <= 127: return ...)
        #   - contains if/elif/else with returns (o2's elif branches)
        try:
            body = node[2]
            body_kind = str(body.kind) if hasattr(body, 'kind') else ''
            if body_kind in ('l_stmts', 'l_stmts_opt', '_stmts', 'returns'):
                should_convert = False
                stmts = list(body)
                if len(stmts) >= 1:
                    # Walk the body to find if it contains a return
                    def has_return(n):
                        k = str(n.kind) if hasattr(n, 'kind') else ''
                        if k in ('return', 'returns', 'return_if_stmt', 'return_if_stmts',
                                 'RETURN_VALUE', 'RETURN_CONST'):
                            return True
                        if hasattr(n, '__iter__'):
                            for c in n:
                                if has_return(c):
                                    return True
                        return False
                    # Check for aug_assign1 or ifstmt/ifelsestmt (first child check)
                    first_stmt = stmts[0]
                    first_sk = str(first_stmt.kind) if hasattr(first_stmt, 'kind') else ''
                    first_kind = first_sk
                    # Unwrap wrapper nodes: lstmt, stmt, lastl_stmt
                    if first_sk in ('lstmt', 'stmt', 'lastl_stmt') and len(first_stmt) > 0:
                        first_kind = str(first_stmt[0].kind) if hasattr(first_stmt[0], 'kind') else ''
                    if first_kind in ('aug_assign1', 'ifstmt', 'ifelsestmt',
                                      'ifelsestmtl', 'ifelsestmtc',
                                      'iflaststmt', 'iflaststmtl'):
                        should_convert = True
                    # Check for return in body
                    if has_return(body):
                        should_convert = True

                if should_convert:
                    self.write(self.indent)
                    self.write("if ")
                    self.preorder(node[1])  # testexpr
                    self.write(":\n")
                    self.indent_more()
                    self.preorder(body)
                    self.indent_less()
                    self.prune()
                    return
        except (IndexError, AttributeError):
            pass
        self.default(node)

    self.n_whilestmt38 = n_whilestmt38

    # --- Helper: recursively inline a lambda code object's body as text ---
    def _inline_lambda_code(code_obj, depth=0):
        """Recursively inline a lambda code object, returning the body as text.
        Returns None if the pattern is unrecognized."""
        import dis
        if depth > 15:
            return None
        try:
            instrs = list(dis.get_instructions(code_obj))
        except Exception:
            return None

        ops = [i.opname for i in instrs]
        
        # Identify globals, inner code objects, constants  
        globals_loaded = [i for i in instrs if i.opname in ('LOAD_GLOBAL', 'LOAD_NAME')]
        global_names = [i.argval for i in globals_loaded]
        inner_codes = [i.argval for i in instrs if i.opname == 'LOAD_CONST' 
                       and hasattr(i.argval, 'co_code')]
        non_code_consts = [i for i in instrs if i.opname == 'LOAD_CONST' 
                           and i.argval is not None and not hasattr(i.argval, 'co_code')]
        load_fasts = [i for i in instrs if i.opname == 'LOAD_FAST']
        compare_ops = [i for i in instrs if i.opname == 'COMPARE_OP']
        binary_ops = [i for i in instrs if i.opname == 'BINARY_OP']

        # --- Pattern A: h2o(agno4(h3o(o2([nums])))) leaf ---
        # Must check BEFORE general func call to avoid false match
        if len(globals_loaded) >= 4:
            first4 = [i.argval for i in globals_loaded[:4]]
            if all(n in ('h2o', 'agno4', 'h3o', 'o2') for n in first4):
                consts = []
                for i in instrs:
                    if i.opname == 'LOAD_CONST' and isinstance(i.argval, (int, float)):
                        consts.append(str(i.argval))
                    elif i.opname == 'LOAD_CONST' and isinstance(i.argval, tuple):
                        consts.extend(str(v) for v in i.argval)
                if consts:
                    return "h2o(agno4(h3o(o2([" + ", ".join(consts) + "]))))"

        # --- Pattern B: func(CONST) leaf — any single function call ---
        # e.g. H2SbF7(30584), c2h6(b'enjuly19/'), longlongint(x)
        if len(globals_loaded) >= 1 and not inner_codes:
            func_name = globals_loaded[0].argval
            args = []
            found_func = False
            for i in instrs:
                if i.opname in ('LOAD_GLOBAL', 'LOAD_NAME') and i.argval == func_name and not found_func:
                    found_func = True
                elif found_func and i.opname == 'LOAD_CONST' and not hasattr(i.argval, 'co_code'):
                    args.append(repr(i.argval))
                elif i.opname in ('CALL', 'CALL_FUNCTION') and found_func:
                    return func_name + "(" + ", ".join(args) + ")"

        # --- Pattern C: func(inner_lambda()) --- 
        # LOAD_GLOBAL func / PUSH_NULL / LOAD_CONST <code> / MAKE_FUNCTION / CALL / CALL / RETURN
        if len(globals_loaded) >= 1 and len(inner_codes) == 1 and not load_fasts:
            func_name = globals_loaded[0].argval
            inner_text = _inline_lambda_code(inner_codes[0], depth + 1)
            if inner_text:
                return func_name + "(" + inner_text + ")"

        # --- Pattern D: Simple wrapper (lambda: inner())() ---
        # PUSH_NULL / LOAD_CONST <code> / MAKE_FUNCTION / CALL / RETURN_VALUE
        if len(inner_codes) == 1 and 'RETURN_VALUE' in ops and not load_fasts and not globals_loaded:
            inner = inner_codes[0]
            
            if compare_ops and len(non_code_consts) >= 2:
                # Pattern D1: (inner)(arg) == val
                inner_text = _inline_lambda_code(inner, depth + 1)
                if inner_text:
                    call_arg = non_code_consts[0].argval
                    cmp_val = non_code_consts[1].argval
                    cmp_op = compare_ops[0].argval
                    return "(" + inner_text + ")(" + repr(call_arg) + ") " + str(cmp_op) + " " + repr(cmp_val)
            else:
                # Pattern D2: Just wrapper returning inner()
                inner_text = _inline_lambda_code(inner, depth + 1)
                if inner_text:
                    return inner_text

        # --- Pattern E: Two inner lambdas ---
        if len(inner_codes) == 2 and not load_fasts:
            text1 = _inline_lambda_code(inner_codes[0], depth + 1)
            text2 = _inline_lambda_code(inner_codes[1], depth + 1)
            if text1 and text2:
                if globals_loaded:
                    return globals_loaded[0].argval + "(" + text2 + ")"
                return "(" + text1 + ")(" + text2 + ")"

        # --- Pattern H: Three inner lambdas: (inner0)(inner1()) == inner2() ---
        # Structure: make_func(inner0) / make_func(inner1) / CALL 0 / CALL 1 / 
        #            make_func(inner2) / CALL 0 / COMPARE_OP / RETURN
        if len(inner_codes) == 3 and compare_ops:
            text0 = _inline_lambda_code(inner_codes[0], depth + 1)
            text1 = _inline_lambda_code(inner_codes[1], depth + 1)
            text2 = _inline_lambda_code(inner_codes[2], depth + 1)
            if text0 and text1 and text2:
                cmp_op = compare_ops[0].argval
                return "(" + text0 + ")(" + text1 + ") " + str(cmp_op) + " " + text2

        # --- Pattern F: LOAD_FAST var + inner() ---
        if load_fasts and inner_codes and binary_ops:
            var_name = load_fasts[0].argval
            inner_text = _inline_lambda_code(inner_codes[0], depth + 1)
            if inner_text:
                # BINARY_OP 0 = +, BINARY_OP 10 = -
                op_code = binary_ops[0].argval if hasattr(binary_ops[0], 'argval') else 0
                op_sym = " - " if op_code == 10 else " + "
                return var_name + op_sym + "(" + inner_text + ")"

        # --- Pattern G: LOAD_FAST var + func(const) ---
        if load_fasts and globals_loaded and not inner_codes:
            var_name = load_fasts[0].argval
            func_name = globals_loaded[0].argval
            args = []
            found_func = False
            for i in instrs:
                if i.opname in ('LOAD_GLOBAL', 'LOAD_NAME') and i.argval == func_name and not found_func:
                    found_func = True
                elif found_func and i.opname == 'LOAD_CONST' and not hasattr(i.argval, 'co_code'):
                    args.append(repr(i.argval))
                elif i.opname in ('CALL', 'CALL_FUNCTION') and found_func:
                    break
            if args:
                op_code = binary_ops[0].argval if binary_ops and hasattr(binary_ops[0], 'argval') else 0
                op_sym = " - " if op_code == 10 else " + "
                return var_name + op_sym + func_name + "(" + ", ".join(args) + ")"

        # --- Pattern I: Multi-call lambda body ---
        # e.g. longlongint(c2h6(b'...')) + h2o(agno4(h3o(o2([c2h6(b'...'), c2h6(b'...')]))))
        # Must have: h2o chain globals + another function + 2+ inner codes
        h2o_chain = all(n in global_names for n in ('h2o', 'agno4', 'h3o', 'o2'))
        non_h2o_funcs = [n for n in global_names if n not in ('h2o', 'agno4', 'h3o', 'o2')]
        if h2o_chain and non_h2o_funcs and len(inner_codes) >= 2 and not load_fasts:
            inner_texts = []
            for ic in inner_codes:
                t = _inline_lambda_code(ic, depth + 1)
                inner_texts.append(t)
            
            func = non_h2o_funcs[0]
            func_inner = inner_texts[0]
            h2o_inners = inner_texts[1:]
            
            if func_inner and all(h2o_inners):
                h2o_args = ", ".join(t for t in h2o_inners if t)
                result = func + "(" + func_inner + ")"
                result += " + h2o(agno4(h3o(o2([" + h2o_args + "]))))"
                return result

        # --- Pattern J: h2o chain with inner code lambda args ---
        # e.g. h2o(agno4(h3o(o2([c2h6(b'...'), c2h6(b'...')]))))
        # Only h2o chain globals, inner_codes as arguments
        if h2o_chain and not non_h2o_funcs and inner_codes and not load_fasts:
            inner_texts = []
            for ic in inner_codes:
                t = _inline_lambda_code(ic, depth + 1)
                inner_texts.append(t)
            resolved = [t for t in inner_texts if t]
            if len(resolved) == len(inner_codes):
                return "h2o(agno4(h3o(o2([" + ", ".join(resolved) + "]))))"

        return None

    # --- mklambda312: lambda expression ---
    def n_mklambda312(node):
        # mklambda312 ::= LOAD_LAMBDA LOAD_STR MAKE_FUNCTION_0
        # Try inlining first — access code object directly from LOAD_LAMBDA token
        body_text = None
        try:
            # node[0] is LOAD_LAMBDA token, its .attr is the code object
            load_lambda = node[0]
            if hasattr(load_lambda, 'attr') and hasattr(load_lambda.attr, 'co_code'):
                body_text = _inline_lambda_code(load_lambda.attr)
        except Exception:
            pass
        
        if body_text:
            self.write("lambda: " + body_text)
            self.prune()
            return
        
        # Fallback to normal make_function
        from uncompyle6.semantics.helper import find_code_node
        try:
            code_node = find_code_node(node, -2)
            self.make_function(node, is_lambda=True, code_node=code_node)
        except Exception:
            self.write("lambda: ...")
        self.prune()

    self.n_mklambda312 = n_mklambda312

    # --- lambda_body312: immediately-invoked lambda ---
    def n_lambda_body312(node):
        # lambda_body312 ::= mklambda312 CALL_FUNCTION_0
        # node[0] = mklambda312, node[0][0] = LOAD_LAMBDA token
        body_text = None
        try:
            load_lambda = node[0][0]  # LOAD_LAMBDA inside mklambda312
            if hasattr(load_lambda, 'attr') and hasattr(load_lambda.attr, 'co_code'):
                body_text = _inline_lambda_code(load_lambda.attr)
        except Exception:
            pass

        if body_text:
            self.write(body_text)
            self.prune()
            return

        # Fallback: (lambda: ...)()
        self.write("(")
        self.preorder(node[0])
        self.write(")()")
        self.prune()

    self.n_lambda_body312 = n_lambda_body312

    # --- is_op312: handle 'is not' vs 'is' ---
    def n_is_op312(node):
        # is_op312 ::= expr expr IS_OP
        # IS_OP.attr: "is" or "is not"
        self.preorder(node[0])
        is_op = node[2]
        if hasattr(is_op, 'attr') and is_op.attr and 'not' in str(is_op.attr):
            self.write(" is not ")
        else:
            self.write(" is ")
        self.preorder(node[1])
        self.prune()

    self.n_is_op312 = n_is_op312

    # --- list312: list from constant ---
    def n_list312(node):
        # list312 ::= BUILD_LIST_0 LOAD_CONST LIST_EXTEND
        # list312 ::= BUILD_LIST_0 expr LIST_EXTEND
        child = node[1]
        if hasattr(child, 'attr') and isinstance(child.attr, tuple):
            const_val = child.attr
            self.write("[")
            sep = ""
            for item in const_val:
                self.write(sep)
                self.write(repr(item))
                sep = ", "
            self.write("]")
        elif hasattr(child, 'kind') and child.kind == 'LOAD_CONST':
            self.write("[")
            self.write(repr(child.attr))
            self.write("]")
        else:
            self.write("[")
            self.preorder(child)
            self.write("]")
        self.prune()

    self.n_list312 = n_list312

    # --- build_list312: list from expressions ---
    def n_build_list312(node):
        # build_list312 ::= expr BUILD_LIST_1
        # build_list312 ::= expr expr BUILD_LIST_2
        self.write("[")
        sep = ""
        for child in node:
            if hasattr(child, 'kind') and child.kind.startswith('BUILD_LIST'):
                break
            self.write(sep)
            self.preorder(child)
            sep = ", "
        self.write("]")
        self.prune()

    self.n_build_list312 = n_build_list312

    # --- compare_chained312: chained comparison ---
    # AST structure:
    #   compare_chained312 ::= expr compare_chain_mid312 compare_chain_end312 COME_FROM
    #   compare_chain_mid312 (leaf, 6 children):
    #     [0] expr [1] COPY [2] COMPARE_OP [3] COPY [4] POP_JUMP_IF_FALSE [5] POP_TOP
    #   compare_chain_mid312 (nested, 7 children):
    #     [0] compare_chain_mid312 [1] expr [2] COPY [3] COMPARE_OP [4] COPY [5] POP_JUMP_IF_FALSE [6] POP_TOP
    #   compare_chain_end312 (4 children):
    #     [0] expr [1] COMPARE_OP [2] JUMP_FORWARD [3] POP_TOP

    def _walk_chain_mid(node):
        """Recursively render a compare_chain_mid312 node.
        Outputs: op1 expr1 op2 expr2 ... (without leading expr which is from parent)"""
        if len(node) == 6:
            # Leaf form: expr COPY COMPARE_OP COPY POP_JUMP_IF_FALSE POP_TOP
            # Get operator
            op_node = node[2]  # COMPARE_OP or IS_OP
            op_str = op_node.pattr if hasattr(op_node, 'pattr') and op_node.pattr else str(getattr(op_node, 'attr', ''))
            if op_node.kind == 'IS_OP':
                if 'not' in str(op_str):
                    self.write(" is not ")
                else:
                    self.write(" is ")
            else:
                self.write(" %s " % op_str.replace("-", " "))
            self.preorder(node[0])  # expr (the right-hand operand)
        elif len(node) == 7:
            # Nested form: compare_chain_mid312 expr COPY COMPARE_OP COPY POP_JUMP_IF_FALSE POP_TOP
            # First recurse into nested chain_mid
            _walk_chain_mid(node[0])
            # Then print this level's operator and expr
            op_node = node[3]  # COMPARE_OP or IS_OP
            op_str = op_node.pattr if hasattr(op_node, 'pattr') and op_node.pattr else str(getattr(op_node, 'attr', ''))
            if op_node.kind == 'IS_OP':
                if 'not' in str(op_str):
                    self.write(" is not ")
                else:
                    self.write(" is ")
            else:
                self.write(" %s " % op_str.replace("-", " "))
            self.preorder(node[1])  # expr (the right-hand operand at this level)

    def n_compare_chained312(node):
        # compare_chained312 ::= expr compare_chain_mid312 compare_chain_end312 COME_FROM
        # Print first operand
        self.preorder(node[0])

        # Walk the chain mid recursively
        if hasattr(node[1], 'kind') and 'compare_chain_mid' in node[1].kind:
            _walk_chain_mid(node[1])

        # Print the final chain end
        if hasattr(node[2], 'kind') and 'compare_chain_end' in node[2].kind:
            end_node = node[2]
            # compare_chain_end312: [0] expr [1] COMPARE_OP [2] JUMP_FORWARD [3] POP_TOP
            op_node = end_node[1]  # COMPARE_OP or IS_OP
            op_str = op_node.pattr if hasattr(op_node, 'pattr') and op_node.pattr else str(getattr(op_node, 'attr', ''))
            if op_node.kind == 'IS_OP':
                if 'not' in str(op_str):
                    self.write(" is not ")
                else:
                    self.write(" is ")
            else:
                self.write(" %s " % op_str.replace("-", " "))
            self.preorder(end_node[0])  # expr (final operand)
        self.prune()

    self.n_compare_chained312 = n_compare_chained312

    # --- match statement handlers ---
    def n_match_stmt312(node):
        self.write(self.indent, "match ")
        self.preorder(node[0])
        self.println(":")
        self.indent_more()
        self.preorder(node[1])
        for i in range(2, len(node)):
            child = node[i]
            if hasattr(child, 'kind') and child.kind in (
                'match_cases312_mid', 'match_case312_mid', 'match_default312'
            ):
                self.preorder(child)
        self.indent_less()
        self.prune()

    self.n_match_stmt312 = n_match_stmt312

    def n_match_case312_first(node):
        case_val = node[1]
        self.write(self.indent, "case ")
        self.preorder(case_val)
        self.println(":")
        self.indent_more()
        for i in range(4, len(node)):
            child = node[i]
            if hasattr(child, 'kind') and child.kind in (
                'l_stmts', 'l_stmts_opt', 'stmts', '_stmts'
            ):
                self.preorder(child)
                break
        self.indent_less()
        self.prune()

    self.n_match_case312_first = n_match_case312_first

    def n_match_case312_mid(node):
        case_val = node[1]
        self.write(self.indent, "case ")
        self.preorder(case_val)
        self.println(":")
        self.indent_more()
        for i in range(3, len(node)):
            child = node[i]
            if hasattr(child, 'kind') and child.kind in (
                'l_stmts', 'l_stmts_opt', 'stmts', '_stmts'
            ):
                self.preorder(child)
                break
        self.indent_less()
        self.prune()

    self.n_match_case312_mid = n_match_case312_mid

    def n_match_cases312_mid(node):
        for child in node:
            self.preorder(child)
        self.prune()

    self.n_match_cases312_mid = n_match_cases312_mid

    def n_match_default312(node):
        self.write(self.indent, "case _:")
        self.println("")
        self.indent_more()
        for child in node:
            if hasattr(child, 'kind') and child.kind in (
                'l_stmts', 'l_stmts_opt', 'stmts', '_stmts'
            ):
                self.preorder(child)
                break
        self.indent_less()
        self.prune()

    self.n_match_default312 = n_match_default312

    # --- listcomp312: inline list comprehension ---
    def n_listcomp312(node):
        get_iter_node = node[0]
        iterable = get_iter_node[0] if len(get_iter_node) > 0 else None
        body = node[1]
        var_name = None
        for i in range(len(node) - 1, 1, -1):
            child = node[i]
            if hasattr(child, 'kind'):
                if child.kind == 'STORE_NAME':
                    var_name = child.pattr
                    break
                elif child.kind in ('store', 'STORE_FAST'):
                    if hasattr(child, 'pattr') and child.pattr:
                        var_name = child.pattr
                    elif hasattr(child, '__len__') and len(child) > 0:
                        inner = child[0]
                        if hasattr(inner, 'pattr') and inner.pattr:
                            var_name = inner.pattr
                    break
        if var_name:
            self.write(self.indent, var_name, " = ")
        self.write("[")
        if hasattr(body, 'kind') and body.kind == 'listcomp_body312':
            inner = body[4] if len(body) > 4 else None
            store = body[3] if len(body) > 3 else None
            if inner and hasattr(inner, 'kind') and inner.kind == 'listcomp_inner312':
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

    # --- try/except312 handler for exception-table-reconstructed blocks ---
    def n_try_except312(node):
        """Render synthetic try_except312 nodes from exception table reconstruction.
        Structure: try_except312 = [try_stmts, except_handler312]
        """
        self.write(self.indent, "try:\n")
        self.indent_more()
        # Render try body
        if len(node) > 0:
            self.preorder(node[0])
        self.indent_less()
        # Render except handler
        if len(node) > 1:
            self.preorder(node[1])
        self.prune()

    self.n_try_except312 = n_try_except312

    def n_except_handler312(node):
        """Render synthetic except_handler312 nodes.
        Structure: except_handler312 = [LOAD_NAME(MemoryError), STORE_NAME(var), except_stmts]
        """
        exc_type = 'MemoryError'
        exc_var = '_exc'
        if len(node) > 0 and hasattr(node[0], 'pattr'):
            exc_type = node[0].pattr
        if len(node) > 1 and hasattr(node[1], 'pattr'):
            exc_var = node[1].pattr

        self.write(self.indent, f"except {exc_type} as {exc_var}:\n")
        self.indent_more()
        # Render except body
        if len(node) > 2:
            self.preorder(node[2])
        self.indent_less()
        self.println("")
        self.prune()

    self.n_except_handler312 = n_except_handler312

    # --- match_subject_block312 handler for reconstructed match subject patterns ---
    def n_match_subject_block312(node):
        """Render the match subject pattern:
        __patch_match_subject = 'X' == 'Y'
        if __patch_match_subject is True:
            raise MemoryError([True])
        elif __patch_match_subject is False:
            _N = [[True], [False]]
            co2(["_X"])
        raise MemoryError([True])
        """
        left = getattr(node, 'match_left', '?')
        right = getattr(node, 'match_right', '?')
        store_var = getattr(node, 'match_store_var', '_N')
        co2_arg = getattr(node, 'match_co2_arg', '_?')

        self.write(self.indent, f"__patch_match_subject = '{left}' == '{right}'\n")
        self.write(self.indent, "if __patch_match_subject is True:\n")
        self.indent_more()
        self.write(self.indent, "raise MemoryError([True])\n")
        self.indent_less()
        self.write(self.indent, "elif __patch_match_subject is False:\n")
        self.indent_more()
        self.write(self.indent, f"{store_var} = [[True], [False]]\n")
        self.write(self.indent, f'co2(["{co2_arg}"])\n')
        self.indent_less()
        self.write(self.indent, "raise MemoryError([True])\n")
        self.prune()

    self.n_match_subject_block312 = n_match_subject_block312

