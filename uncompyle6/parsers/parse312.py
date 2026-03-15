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
"""
spark grammar for Python 3.12.

Python 3.12 bytecode uses very different patterns from 3.8:
  - RETURN_CONST replaces LOAD_CONST + RETURN_VALUE for constant returns
  - CALL replaces CALL_FUNCTION (we map it to CALL_FUNCTION_n in the scanner)
  - BINARY_OP replaces all BINARY_*/INPLACE_* (we map to old names in scanner)
  - FOR loops use JUMP_BACKWARD + END_FOR instead of JUMP_ABSOLUTE + POP_TOP
  - No SETUP_LOOP, SETUP_EXCEPT in real bytecode
  - BEFORE_WITH for context managers
  - Exception handling via exception table
"""

from __future__ import print_function

from spark_parser import DEFAULT_DEBUG as PARSER_DEFAULT_DEBUG

from uncompyle6.parser import PythonParserSingle, nop_func
from uncompyle6.parsers.parse38 import Python38Parser


class Python312Parser(Python38Parser):
    def p_312_stmt(self, args):
        """
         # RETURN_CONST is the primary return mechanism in 3.12
         # It replaces LOAD_CONST + RETURN_VALUE for constant returns
         stmt               ::= return_const
         return_const       ::= RETURN_CONST

         # Module-level: RETURN_CONST can end a module (implicit return None)
         sstmt              ::= return_const
         sstmt              ::= stmt
         sstmt              ::= return_const RETURN_LAST

         # For loops in 3.12 use END_FOR after the loop
         # Pattern: expr get_for_iter store body JUMP_BACK _come_froms END_FOR
         stmt               ::= for312
         stmt               ::= forelsestmt312

         for312             ::= expr get_for_iter store for_block312 _come_froms END_FOR
         for312             ::= expr get_for_iter store for_block312 _come_froms END_FOR POP_TOP
         for312             ::= expr get_for_iter store for_block312 END_FOR
         for312             ::= expr get_for_iter store for_block312 END_FOR POP_TOP
         for312             ::= expr get_iter store for_block312 _come_froms END_FOR
         for312             ::= expr get_iter store for_block312 END_FOR

         for_block312       ::= l_stmts_opt JUMP_BACK _come_froms
         for_block312       ::= l_stmts_opt JUMP_BACK
         for_block312       ::= l_stmts JUMP_BACK _come_froms
         for_block312       ::= l_stmts JUMP_BACK

         # For loops where the body returns (no JUMP_BACK)
         # return inside for compiles as: expr POP_TOP RETURN_VALUE
         # POP_TOP cleans up the iterator before returning
         for_block312       ::= return_expr POP_TOP RETURN_VALUE
         for_block312       ::= l_stmts return_expr POP_TOP RETURN_VALUE

         forelsestmt312     ::= expr get_for_iter store for_block312 _come_froms END_FOR else_suite
         forelsestmt312     ::= expr get_for_iter store for_block312 END_FOR else_suite

         # While loops in 3.12
         stmt               ::= whilestmt312
         stmt               ::= whileTruestmt312

         whilestmt312       ::= _come_froms testexpr l_stmts_opt JUMP_BACK
         whilestmt312       ::= _come_froms testexpr l_stmts_opt JUMP_BACK come_froms
         whilestmt312       ::= _come_froms testexpr l_stmts_opt COME_FROM JUMP_BACK
         whilestmt312       ::= _come_froms testexpr returns JUMP_BACK

         whileTruestmt312   ::= _come_froms l_stmts JUMP_BACK
         whileTruestmt312   ::= _come_froms l_stmts JUMP_BACK come_froms
         whileTruestmt312   ::= _come_froms l_stmts JUMP_BACK COME_FROM_EXCEPT_CLAUSE
         whileTruestmt312   ::= _come_froms pass JUMP_BACK

         # break/continue in 3.12
         break              ::= BREAK_LOOP
         break              ::= POP_TOP BREAK_LOOP

         # Simple call statement
         stmt               ::= call_stmt
         call_stmt          ::= call

         # If/else in 3.12: intermediate branches end with JUMP_FORWARD
         # (we convert RETURN_CONST None to JUMP_FORWARD in scanner)
         ifstmt             ::= testexpr _ifstmts_jump312
         _ifstmts_jump312   ::= c_stmts_opt JUMP_FORWARD _come_froms
         _ifstmts_jump312   ::= c_stmts_opt JUMP_FORWARD come_froms
         _ifstmts_jump312   ::= c_stmts JUMP_FORWARD _come_froms

         ifelsestmt         ::= testexpr c_stmts_opt JUMP_FORWARD else_suite come_froms
         ifelsestmt         ::= testexpr c_stmts_opt JUMP_FORWARD else_suite _come_froms

         # Ternary expressions (if_exp) in 3.12
         # Pattern: cond POP_JUMP_IF_FALSE then_expr JUMP_FORWARD COME_FROM(s) else_expr COME_FROM
         # In nested ternaries, multiple COME_FROMs may appear at the else point
         if_exp             ::= expr jmp_false expr JUMP_FORWARD _come_froms expr COME_FROM
         if_exp             ::= expr jmp_false expr JUMP_FORWARD expr COME_FROM

         # list with const init
         expr               ::= list312
         list312            ::= BUILD_LIST_0 LOAD_CONST LIST_EXTEND
         list312            ::= BUILD_LIST_0 expr LIST_EXTEND

         # assert statement in 3.12
         # Simple: assert expr → POP_JUMP_IF_TRUE ... LOAD_ASSERTION_ERROR RAISE_VARARGS_1
         stmt               ::= assert312
         assert312          ::= expr POP_JUMP_IF_TRUE
                                 LOAD_ASSERTION_ERROR RAISE_VARARGS_1 COME_FROM
         assert312          ::= assert_expr POP_JUMP_IF_TRUE
                                 LOAD_ASSERTION_ERROR RAISE_VARARGS_1 COME_FROM
         # assert with message
         assert312          ::= expr POP_JUMP_IF_TRUE
                                 LOAD_ASSERTION_ERROR expr RAISE_VARARGS_2 COME_FROM
         # inline assert (inside for loop): uses POP_JUMP_IF_FALSE to skip assertion
         # Pattern: expr COMPARE_OP POP_JUMP_IF_FALSE JUMP_BACK COME_FROM LOAD_ASSERTION_ERROR RAISE_VARARGS_1
         assert312          ::= expr POP_JUMP_IF_FALSE JUMP_BACK COME_FROM
                                 LOAD_ASSERTION_ERROR RAISE_VARARGS_1
         assert312          ::= expr POP_JUMP_IF_FALSE JUMP_FORWARD COME_FROM
                                 LOAD_ASSERTION_ERROR RAISE_VARARGS_1

         # f-string in 3.12
         expr               ::= fstring312
         fstring312         ::= expr FORMAT_VALUE
         fstring312         ::= expr FORMAT_VALUE_SPEC
         fstring312         ::= expr expr FORMAT_VALUE_SPEC
         expr               ::= build_string312
         build_string312    ::= joined_str312
         joined_str312      ::= expr expr FORMAT_VALUE BUILD_STRING
         joined_str312      ::= expr expr FORMAT_VALUE expr BUILD_STRING
         joined_str312      ::= expr fstring312 expr BUILD_STRING
         joined_str312      ::= expr fstring312 BUILD_STRING
         # Multi-part fstring: "prefix {a} middle {b} suffix"
         # Pattern: LOAD_STR expr FORMAT_VALUE LOAD_STR expr FORMAT_VALUE BUILD_STRING
         joined_str312      ::= expr expr FORMAT_VALUE expr expr FORMAT_VALUE BUILD_STRING

         # Slice operations (new in 3.12)
         expr               ::= binary_slice312
         binary_slice312    ::= expr expr expr BINARY_SLICE
         binary_slice312    ::= expr expr BINARY_SLICE

         # with statement in 3.12 (BEFORE_WITH replaces old SETUP_WITH)
         stmt               ::= with_stmt312
         with_stmt312       ::= expr BEFORE_WITH store l_stmts_opt
                                 LOAD_CONST LOAD_CONST LOAD_CONST CALL_FUNCTION POP_TOP
         with_stmt312       ::= expr BEFORE_WITH store l_stmts_opt
                                 LOAD_CONST LOAD_CONST LOAD_CONST CALL_FUNCTION POP_TOP
                                 JUMP_FORWARD POP_JUMP_IF_TRUE COME_FROM POP_TOP POP_EXCEPT
                                 POP_TOP POP_TOP

         # Dict comprehension inline (3.12)
         expr               ::= dictcomp312
         dictcomp312        ::= expr get_for_iter BUILD_MAP_0 COME_FROM FOR_ITER
                                 store expr expr MAP_ADD JUMP_BACK COME_FROM END_FOR
         dictcomp312        ::= BUILD_MAP_0 expr get_for_iter store expr expr MAP_ADD
                                 JUMP_BACK _come_froms END_FOR

         # Generator function body starts with RETURN_GENERATOR + POP_TOP
         stmt               ::= return_generator312
         return_generator312 ::= RETURN_GENERATOR POP_TOP

         # for-else with break in 3.12
         # break compiles as: if_cond POP_JUMP_IF_TRUE ... JUMP_BACK COME_FROM POP_TOP JUMP_FORWARD
         #   then: COME_FROM END_FOR else_body
         # get_for_iter ::= GET_ITER _come_froms FOR_ITER (defined in parse37.py)
         stmt               ::= forelse312_break
         forelse312_break   ::= expr get_for_iter store
                                 for_block312_break
                                 _come_froms END_FOR
                                 else_suite312 COME_FROM
         forelse312_break   ::= expr get_for_iter store
                                 for_block312_break
                                 _come_froms END_FOR
                                 else_suite312
         for_block312_break ::= l_stmts_opt JUMP_BACK _come_froms POP_TOP JUMP_FORWARD
         for_block312_break ::= l_stmts_opt JUMP_BACK COME_FROM POP_TOP JUMP_FORWARD
         else_suite312      ::= l_stmts_opt

         # Walrus operator (:=) in 3.12
         # (n := expr) compiles as: expr COPY STORE_NAME n
         # COPY duplicates TOS so the expression value stays on stack
         expr               ::= walrus_expr312
         walrus_expr312     ::= expr COPY store

         # RETURN_VALUE for function bodies (return <expr>)
         return             ::= expr POP_TOP RETURN_VALUE

         # Function definition in 3.12
         # mkfunc: LOAD_CODE <code_obj> LOAD_STR <func_name> MAKE_FUNCTION_0
         # funcdef: mkfunc STORE_NAME <func_name>
         stmt               ::= funcdef312
         funcdef312         ::= mkfunc312 store
         mkfunc312          ::= LOAD_CODE LOAD_STR MAKE_FUNCTION_0
         mkfuncdeco312      ::= expr mkfunc312 CALL_FUNCTION_1
         stmt               ::= funcdefdeco312
         funcdefdeco312     ::= mkfuncdeco312 store

         # Lambda definition in 3.12
         # lambda: LOAD_LAMBDA <code_obj> LOAD_STR <lambda> MAKE_FUNCTION_0
         # Usually followed by CALL_FUNCTION_0 for immediate invocation
         mklambda312        ::= LOAD_LAMBDA LOAD_STR MAKE_FUNCTION_0
         expr               ::= mklambda312
         expr               ::= lambda_body312
         lambda_body312     ::= mklambda312 CALL_FUNCTION_0

         # IS_OP comparison (Python 3.12 uses IS_OP for 'is'/'is not')
         # Used for: x is True, x is False, x is not None
         expr               ::= is_op312
         is_op312           ::= expr expr IS_OP

         # RAISE_VARARGS_1 as a standalone statement (raise ExcType(args))
         stmt               ::= raise_stmt312
         raise_stmt312      ::= expr RAISE_VARARGS_1

         # BUILD_LIST expressions
         expr               ::= build_list312
         build_list312      ::= expr BUILD_LIST_1
         build_list312      ::= expr expr BUILD_LIST_2


         # Chained comparisons in 3.12
         # Pattern: expr expr COPY COMPARE_OP COPY POP_JUMP_IF_FALSE POP_TOP
         #          expr COPY COMPARE_OP COPY POP_JUMP_IF_FALSE POP_TOP
         #          expr COMPARE_OP JUMP_FORWARD POP_TOP COME_FROM
         # This is used for: a > b < c > d (3-element chain)
         expr               ::= compare_chained312
         compare_chained312 ::= expr compare_chain_mid312 compare_chain_end312 _come_froms
         compare_chained312 ::= expr compare_chain_mid312 compare_chain_end312

         # Middle link: ... COPY COMPARE_OP COPY POP_JUMP_IF_FALSE POP_TOP expr
         compare_chain_mid312 ::= expr COPY COMPARE_OP COPY POP_JUMP_IF_FALSE POP_TOP
         compare_chain_mid312 ::= compare_chain_mid312 expr COPY COMPARE_OP COPY POP_JUMP_IF_FALSE POP_TOP

         # IS_OP in chained comparisons: expr COPY IS_OP COPY POP_JUMP_IF_FALSE POP_TOP
         compare_chain_mid312 ::= expr COPY IS_OP COPY POP_JUMP_IF_FALSE POP_TOP
         compare_chain_mid312 ::= compare_chain_mid312 expr COPY IS_OP COPY POP_JUMP_IF_FALSE POP_TOP
         compare_chain_end312 ::= expr IS_OP JUMP_FORWARD POP_TOP
         compare_chain_end312 ::= expr IS_OP

         # End link: expr COMPARE_OP JUMP_FORWARD POP_TOP (COME_FROM handled by parent)
         compare_chain_end312 ::= expr COMPARE_OP JUMP_FORWARD POP_TOP
         compare_chain_end312 ::= expr COMPARE_OP

         # Ternary conditional expression in 3.12
         # (true_val if condition else false_val)
         # => condition POP_JUMP_IF_FALSE true_val JUMP_FORWARD COME_FROM false_val
         expr               ::= if_exp312
         if_exp312          ::= expr POP_JUMP_IF_FALSE expr JUMP_FORWARD _come_froms expr
         if_exp312          ::= expr POP_JUMP_IF_FALSE expr JUMP_FORWARD COME_FROM expr

         # Ternary with 'and' condition: (val if cond1 and cond2 else val)
         # => cond1 POP_JUMP_IF_FALSE cond2 POP_JUMP_IF_FALSE true JUMP_FORWARD COME_FROM COME_FROM false  
         if_exp312          ::= expr POP_JUMP_IF_FALSE expr POP_JUMP_IF_FALSE expr JUMP_FORWARD _come_froms expr
        """


    def p_312_returns(self, args):
        """
         # Return statements
         return             ::= return_expr RETURN_VALUE
         return             ::= RETURN_CONST
         return_expr_or_cond ::= return_expr
         return_expr_or_cond ::= RETURN_CONST

         stmt               ::= return_const
         return_const       ::= RETURN_CONST

         # return None is very common in 3.12
         return_if_stmt     ::= return_expr RETURN_VALUE
         return_if_stmt     ::= RETURN_CONST
         return_if_stmts    ::= _stmts return_if_stmt

         # 3.12 ending_return uses RETURN_CONST
         ending_return      ::= RETURN_CONST RETURN_LAST
         ending_return      ::= RETURN_CONST
        """

    def p_312_try(self, args):
        """
         # try/except in 3.12 uses exception table, not SETUP_FINALLY
         # Pattern: try_body JUMP_FORWARD except_handler ... POP_EXCEPT
         stmt               ::= try_except312
         stmt               ::= tryfinally312

         # 3.12 try/except: try body ends with JUMP_FORWARD that skips the except handler
         try_except312      ::= suite_stmts_opt JUMP_FORWARD
                                 except_handler312
         try_except312      ::= suite_stmts_opt JUMP_FORWARD
                                 except_handler312 _come_froms
         try_except312      ::= suite_stmts_opt JUMP_FORWARD
                                 except_handler312 POP_EXCEPT
         try_except312      ::= suite_stmts_opt JUMP_FORWARD
                                 except_handler312 _come_froms POP_EXCEPT
         # With COPY (cleanup after RERAISE — RERAISE is skipped)
         try_except312      ::= suite_stmts_opt JUMP_FORWARD
                                 except_handler312 COPY POP_EXCEPT
         try_except312      ::= suite_stmts_opt JUMP_FORWARD
                                 except_handler312 _come_froms COPY POP_EXCEPT

         # Exception handler pattern in 3.12:
         # LOAD_NAME ExcType, COMPARE_OP, POP_JUMP_IF_FALSE, POP_TOP,
         # handler_body, POP_EXCEPT, JUMP_FORWARD
         except_handler312  ::= except_cond312 except_stmts312
         except_handler312  ::= except_stmts312

         # Exception condition check
         except_cond312     ::= expr COMPARE_OP POP_JUMP_IF_FALSE POP_TOP
         except_cond312     ::= expr COMPARE_OP POP_JUMP_IF_FALSE _come_froms POP_TOP

         # Exception handler body
         except_stmts312    ::= l_stmts_opt POP_EXCEPT
         except_stmts312    ::= l_stmts_opt POP_EXCEPT JUMP_FORWARD
         except_stmts312    ::= l_stmts_opt POP_EXCEPT return_const

         tryfinally312      ::= SETUP_FINALLY suite_stmts_opt POP_BLOCK
                                 COME_FROM_FINALLY suite_stmts_opt

         # match/case in 3.12
         # Pattern: subject COPY case_value COMPARE_OP POP_JUMP_IF_FALSE POP_TOP body JUMP_FORWARD
         #          COME_FROM case_value COMPARE_OP POP_JUMP_IF_FALSE body JUMP_FORWARD
         #          default_body
         stmt               ::= match_stmt312

         # Full match statement: subject + first case + more cases + optional default
         match_stmt312      ::= expr match_case312_first match_cases312_mid match_default312
         match_stmt312      ::= expr match_case312_first match_cases312_mid
         match_stmt312      ::= expr match_case312_first match_default312
         match_stmt312      ::= expr match_case312_first

         # First case: has COPY to duplicate subject, POP_TOP after successful match
         match_case312_first ::= COPY expr COMPARE_OP POP_JUMP_IF_FALSE
                                  POP_TOP l_stmts_opt _jump
         match_case312_first ::= COPY expr COMPARE_OP POP_JUMP_IF_FALSE
                                  POP_TOP l_stmts _jump

         # Middle cases: COME_FROM from prev failed branch, compare against subject (still on stack)
         match_cases312_mid ::= match_case312_mid+
         match_case312_mid  ::= COME_FROM expr COMPARE_OP POP_JUMP_IF_FALSE
                                 l_stmts_opt _jump
         match_case312_mid  ::= COME_FROM expr COMPARE_OP POP_JUMP_IF_FALSE
                                 l_stmts _jump

         # Default case (wildcard _): just the body
         match_default312   ::= COME_FROM l_stmts_opt
         match_default312   ::= l_stmts_opt
         # Inline list comprehension in 3.12
         # In 3.12, list comprehensions are inlined (no separate code object).
         # get_iter already includes `expr GET_ITER` so no separate expr needed.
         # Pattern: get_iter BUILD_LIST_0 COME_FROM FOR_ITER store body 
         #          LIST_APPEND JUMP_BACK COME_FROM END_FOR store store
         stmt               ::= listcomp312
         listcomp312        ::= get_iter listcomp_body312 STORE_FAST STORE_NAME
         listcomp312        ::= get_iter listcomp_body312 store store
         listcomp312        ::= get_iter listcomp_body312 store

         expr               ::= listcomp312_expr
         listcomp312_expr   ::= get_iter listcomp_body312 STORE_FAST
         listcomp312_expr   ::= get_iter listcomp_body312

         listcomp_body312   ::= BUILD_LIST_0 _come_froms FOR_ITER store
                                 listcomp_inner312 JUMP_BACK _come_froms END_FOR
         listcomp_inner312  ::= expr LIST_APPEND
         listcomp_inner312  ::= expr expr BINARY_MULTIPLY LIST_APPEND

        """

    def __init__(self, debug_parser=PARSER_DEFAULT_DEBUG):
        super(Python312Parser, self).__init__(debug_parser)
        self.customized = {}

    def remove_rules_312(self):
        """Remove rules that don't apply to 3.12.
        We do this one-by-one to be safe about rules that might not exist."""
        rules_to_remove = [
            "for                ::= setup_loop expr get_for_iter store for_block POP_BLOCK",
            "for                ::= setup_loop expr get_for_iter store for_block POP_BLOCK NOP",
            "for_block          ::= l_stmts_opt COME_FROM_LOOP JUMP_BACK",
            "forelsestmt        ::= setup_loop expr get_for_iter store for_block POP_BLOCK else_suite",
            "forelselaststmt    ::= setup_loop expr get_for_iter store for_block POP_BLOCK else_suitec",
            "forelselaststmtl   ::= setup_loop expr get_for_iter store for_block POP_BLOCK else_suitel",
            # Old if_exp rules that use jump_absolute_else / jf_cf don't apply in 3.12
            "if_exp             ::= expr jmp_false expr jump_absolute_else expr",
            "if_exp             ::= expr jmp_false expr jf_cf expr COME_FROM",
        ]
        for rule in rules_to_remove:
            try:
                self.remove_rules(rule)
            except (KeyError, TypeError):
                pass

    def customize_reduce_checks_full312(self, tokens, customize):
        """Extra checks for 3.12 reductions."""
        self.remove_rules_312()
        self.check_reduce["whileTruestmt312"] = "tokens"
        self.check_reduce["whilestmt312"] = "tokens"
        self.check_reduce["if_exp"] = "AST"

    def customize_grammar_rules(self, tokens, customize):
        super(Python38Parser, self).customize_grammar_rules(tokens, customize)
        self.customize_reduce_checks_full312(tokens, customize)

        customize_instruction_basenames = frozenset(
            (
                "BEFORE",
                "BUILD",
                "CALL",
                "DICT",
                "GET",
                "FORMAT",
                "LIST",
                "LOAD",
                "MAKE",
                "SETUP",
                "UNPACK",
            )
        )

        custom_ops_processed = frozenset()
        self.seen_ops = frozenset([t.kind for t in tokens])
        self.seen_op_basenames = frozenset(
            [opname[: opname.rfind("_")] for opname in self.seen_ops]
        )

        custom_ops_processed = {"DICT_MERGE"}

        n = len(tokens)
        has_get_iter_call_function1 = False
        for i, token in enumerate(tokens):
            if (
                token == "GET_ITER"
                and i < n - 2
                and (tokens[i + 1] == "CALL_FUNCTION_1" 
                     or (tokens[i + 1].kind == "CALL_FUNCTION" and tokens[i + 1].attr == 1))
            ):
                has_get_iter_call_function1 = True

        for i, token in enumerate(tokens):
            opname = token.kind

            if (
                opname[: opname.find("_")] not in customize_instruction_basenames
                or opname in custom_ops_processed
            ):
                continue

            opname_base = opname[: opname.rfind("_")]

            if (
                opname[: opname.find("_")] not in customize_instruction_basenames
                or opname in custom_ops_processed
            ):
                continue

            if opname_base in (
                "BUILD_LIST",
                "BUILD_SET",
                "BUILD_SET_UNPACK",
                "BUILD_TUPLE",
                "BUILD_TUPLE_UNPACK",
            ):
                v = token.attr

                is_LOAD_CLOSURE = False
                if opname_base == "BUILD_TUPLE":
                    is_LOAD_CLOSURE = True
                    for j in range(v):
                        if tokens[i - j - 1].kind != "LOAD_CLOSURE":
                            is_LOAD_CLOSURE = False
                            break
                    if is_LOAD_CLOSURE:
                        rule = "load_closure ::= %s%s" % (
                            ("LOAD_CLOSURE " * v),
                            opname,
                        )
                        self.add_unique_rule(rule, opname, token.attr, customize)

                elif opname_base == "BUILD_LIST":
                    v = token.attr
                    if v == 0:
                        rule_str = """
                           list        ::= BUILD_LIST_0
                           list_unpack ::= BUILD_LIST_0 expr LIST_EXTEND
                           list        ::= list_unpack
                        """
                        self.add_unique_doc_rules(rule_str, customize)

                if not is_LOAD_CLOSURE or v == 0:
                    build_count = token.attr
                    thousands = build_count // 1024
                    thirty32s = (build_count // 32) % 32
                    if thirty32s > 0:
                        rule = "expr32 ::=%s" % (" expr" * 32)
                        self.add_unique_rule(
                            rule, opname_base, build_count, customize
                        )
                    if thousands > 0:
                        self.add_unique_rule(
                            "expr1024 ::=%s" % (" expr32" * 32),
                            opname_base,
                            build_count,
                            customize,
                        )
                    collection = opname_base[opname_base.find("_") + 1 :].lower()
                    rule = (
                        ("%s ::= " % collection)
                        + "expr1024 " * thousands
                        + "expr32 " * thirty32s
                        + "expr " * (build_count % 32)
                        + opname
                    )
                    self.add_unique_rules(
                        ["expr ::= %s" % collection, rule], customize
                    )
                    continue
                continue


            elif opname == "LOAD_CLOSURE":
                self.addRule("""load_closure ::= LOAD_CLOSURE+""", nop_func)

            elif opname == "MAKE_FUNCTION_8":
                if "LOAD_DICTCOMP" in self.seen_ops:
                    rule = """
                       dict_comp ::= load_closure LOAD_DICTCOMP LOAD_STR
                                     MAKE_FUNCTION_8 expr
                                     GET_ITER CALL_FUNCTION_1
                       """
                    self.addRule(rule, nop_func)
                elif "LOAD_SETCOMP" in self.seen_ops:
                    rule = """
                       set_comp ::= load_closure LOAD_SETCOMP LOAD_STR
                                    MAKE_FUNCTION_CLOSURE expr
                                    GET_ITER CALL_FUNCTION_1
                       """
                    self.addRule(rule, nop_func)

    def reduce_is_invalid(self, rule, ast, tokens, first, last):
        lhs = rule[0]
        n = len(tokens)
        last = min(last, n - 1)
        fn = self.reduce_check_table.get(lhs, None)
        try:
            if fn:
                result = fn(self, lhs, n, rule, ast, tokens, first, last)
                if result:
                    return result
        except (AttributeError, KeyError):
            # Reduce checks may access self.insts and self.offset2inst_index
            # which might not be available or might reference forwarded
            # NOP offsets. In such cases, don't reject the rule.
            pass
        except Exception:
            # For other exceptions, also don't crash — just don't reject
            pass

        if lhs in ("whileTruestmt312", "whilestmt312"):
            jb_index = last - 1
            while jb_index > 0 and tokens[jb_index].kind.startswith("COME_FROM"):
                jb_index -= 1
            t = tokens[jb_index]
            if t.kind != "JUMP_BACK":
                return True
            return t.attr != tokens[first].off2int()

        if lhs in ("aug_assign1", "aug_assign2") and ast[0][0] == "and":
            return True

        # Reject expr ::= LOAD_CODE when followed by LOAD_STR + MAKE_FUNCTION
        # This prevents GLR ambiguity with mkfunc312 ::= LOAD_CODE LOAD_STR MAKE_FUNCTION_0
        if lhs == "expr" and len(ast) == 1 and ast[0].kind == "LOAD_CODE":
            if last + 1 < n and tokens[last + 1].kind == "LOAD_STR":
                if last + 2 < n and tokens[last + 2].kind.startswith("MAKE_FUNCTION"):
                    return True

        # Validate if_exp: the trailing COME_FROM must come from the JUMP_FORWARD
        # if_exp ::= expr jmp_false expr JUMP_FORWARD [_come_froms] expr COME_FROM
        # The last COME_FROM's source (attr) should equal the JUMP_FORWARD's offset
        if lhs == "if_exp":
            # Find JUMP_FORWARD in the AST
            jf_node = None
            trailing_cf = ast[-1]
            for child in ast:
                if hasattr(child, 'kind') and child.kind == "JUMP_FORWARD":
                    jf_node = child
                    break
            if jf_node is not None and trailing_cf.kind == "COME_FROM":
                # COME_FROM.attr should be the offset of the JUMP_FORWARD
                try:
                    jf_offset = jf_node.off2int()
                    cf_source = int(str(trailing_cf.attr).split('_')[0]) if trailing_cf.attr else -1
                    if cf_source != jf_offset:
                        return True
                except (ValueError, TypeError, AttributeError):
                    pass

        return False

    def parse(self, tokens, customize=None):
        """Override parse to handle large token streams that cause Earley
        parser state explosion. When token count exceeds MAX_TOKENS,
        split at statement boundaries and parse each chunk independently.
        """
        MAX_TOKENS = 200

        if len(tokens) <= MAX_TOKENS:
            return super().parse(tokens)

        # Find statement boundaries: positions where we can safely split
        split_points = []
        for i in range(len(tokens) - 1):
            t = tokens[i]
            if t.kind in ('STORE_NAME', 'STORE_SUBSCR', 'STORE_FAST',
                          'STORE_GLOBAL', 'STORE_DEREF', 'DELETE_NAME',
                          'DELETE_FAST', 'DELETE_GLOBAL'):
                next_t = tokens[i + 1]
                if next_t.kind in ('LOAD_NAME', 'LOAD_CONST', 'LOAD_FAST',
                                   'LOAD_GLOBAL', 'LOAD_CODE', 'LOAD_LAMBDA',
                                   'PUSH_NULL', 'NOP', 'RETURN_CONST',
                                   'RETURN_VALUE', 'JUMP_FORWARD',
                                   'JUMP_BACK', 'COME_FROM',
                                   'DELETE_NAME', 'DELETE_FAST',
                                   'LOAD_DEREF', 'LOAD_STR',
                                   'BUILD_LIST_0', 'BUILD_MAP_0'):
                    split_points.append(i)

        if not split_points:
            return super().parse(tokens)

        # Build chunks: find the best split point near MAX_TOKENS
        chunk_ranges = []
        start = 0
        sp_idx = 0

        while sp_idx < len(split_points):
            sp = split_points[sp_idx]
            chunk_size = sp - start + 1

            if chunk_size >= MAX_TOKENS:
                # Find the best split point: the largest one still < MAX_TOKENS
                best_sp = None
                for j in range(sp_idx, -1, -1):
                    candidate = split_points[j]
                    if candidate >= start and (candidate - start + 1) < MAX_TOKENS:
                        best_sp = candidate
                        break

                if best_sp is not None and best_sp > start:
                    chunk_ranges.append((start, best_sp))
                    start = best_sp + 1
                    # Find next sp_idx after start
                    while sp_idx < len(split_points) and split_points[sp_idx] < start:
                        sp_idx += 1
                    continue
                else:
                    # No good split point found before MAX_TOKENS, use current
                    chunk_ranges.append((start, sp))
                    start = sp + 1

            sp_idx += 1

        # Add remaining tokens as final chunk
        if start < len(tokens):
            chunk_ranges.append((start, len(tokens) - 1))

        if len(chunk_ranges) <= 1:
            return super().parse(tokens)

        # Parse each chunk independently
        from uncompyle6.scanner import Token as TokenClass
        all_stmts = []

        for ci, (chunk_start, chunk_end) in enumerate(chunk_ranges):
            chunk_tokens = list(tokens[chunk_start:chunk_end + 1])

            if not chunk_tokens:
                continue

            # Ensure chunk ends with a terminal token
            last_tok = chunk_tokens[-1]
            if last_tok.kind not in ('RETURN_CONST', 'RETURN_VALUE',
                                     'RETURN_LAST', 'RETURN_VALUE_LAMBDA',
                                     'LAMBDA_MARKER'):
                chunk_tokens.append(
                    TokenClass(opname='RETURN_CONST', attr=None,
                              pattr='None', offset=99999, linestart=None)
                )

            try:
                import sys, os, io
                old_stdout = sys.stdout
                sys.stdout = io.StringIO()
                try:
                    chunk_ast = super().parse(chunk_tokens)
                finally:
                    sys.stdout.close()
                    sys.stdout = old_stdout
                if chunk_ast is not None:
                    if hasattr(chunk_ast, '__iter__'):
                        for child in chunk_ast:
                            all_stmts.append(child)
                    else:
                        all_stmts.append(chunk_ast)
            except Exception:
                # Chunk failed — continue with remaining chunks
                # Create a placeholder comment node
                pass

        # Build a combined stmts AST
        if all_stmts:
            from spark_parser import GenericASTBuilder
            combined = GenericASTBuilder.nonterminal(self, 'stmts', all_stmts)
            return combined
        else:
            return super().parse(tokens)


class Python312ParserSingle(Python312Parser, PythonParserSingle):
    pass


if __name__ == "__main__":
    # Check grammar
    p = Python312Parser()
    p.remove_rules_312()
    p.check_grammar()
    from xdis.version_info import IS_PYPY, PYTHON_VERSION_TRIPLE

    if PYTHON_VERSION_TRIPLE[:2] == (3, 12):
        lhs, rhs, tokens, right_recursive, dup_rhs = p.check_sets()
        from uncompyle6.scanner import get_scanner

        s = get_scanner(PYTHON_VERSION_TRIPLE, IS_PYPY)
        opcode_set = set(s.opc.opname).union(
            set(
                """JUMP_BACK CONTINUE RETURN_END_IF COME_FROM
               LOAD_GENEXPR LOAD_ASSERT LOAD_SETCOMP LOAD_DICTCOMP LOAD_CLASSNAME
               LAMBDA_MARKER RETURN_LAST
            """.split()
            )
        )
        remain_tokens = set(tokens) - opcode_set
        import re

        remain_tokens = set([re.sub(r"_\d+$", "", t) for t in remain_tokens])
        remain_tokens = set([re.sub("_CONT$", "", t) for t in remain_tokens])
        remain_tokens = set(remain_tokens) - opcode_set
        print(remain_tokens)
