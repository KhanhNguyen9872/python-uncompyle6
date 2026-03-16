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
Python 3.12 bytecode decompiler scanner.

Python 3.12 has major bytecode changes from 3.8:
  - BINARY_OP replaces all individual binary/inplace ops
  - CALL replaces CALL_FUNCTION/CALL_METHOD
  - PUSH_NULL for non-method call convention
  - RESUME at every function/generator entry
  - RETURN_CONST for returning constants
  - END_FOR replaces POP_TOP on exhausted iterators
  - JUMP_BACKWARD replaces backward JUMP_ABSOLUTE
  - No JUMP_ABSOLUTE (all jumps are relative)
  - BEFORE_WITH replaces SETUP_WITH for context managers
  - No SETUP_LOOP, SETUP_EXCEPT
  - KW_NAMES for keyword argument calls
  - LOAD_FAST_AND_CLEAR for inline comprehensions
  - COPY/SWAP stack manipulation
  - POP_JUMP_IF_NONE/POP_JUMP_IF_NOT_NONE
  - BINARY_SLICE/STORE_SLICE
  - CALL_INTRINSIC_1/2 for internal operations
  - Exception handling via exception table (not SETUP_FINALLY blocks)
  - PUSH_EXC_INFO/CHECK_EXC_MATCH/POP_EXCEPT for try/except
  - LOAD_SUPER_ATTR for super().attr
"""

import sys
from typing import Dict, List, Tuple

import xdis
from xdis import Bytecode, Instruction, instruction_size, iscode
from xdis.bytecode import _get_const_info
from xdis.opcodes import opcode_312 as opc

from uncompyle6.scanner import CONST_COLLECTIONS, Scanner, Token
from uncompyle6.scanners.tok import off2int

# bytecode verification, verify(), uses JUMP_OPs from here
JUMP_OPs = opc.JUMP_OPS

# BINARY_OP argument to operator name mapping
BINARY_OP_MAP = {
    0: "+",
    1: "&",
    2: "//",
    3: "<<",
    4: "@",
    5: "*",
    6: "%",
    7: "|",
    8: "**",
    9: ">>",
    10: "-",
    11: "/",
    12: "^",
    13: "+=",
    14: "&=",
    15: "//=",
    16: "<<=",
    17: "@=",
    18: "*=",
    19: "%=",
    20: "|=",
    21: "**=",
    22: ">>=",
    23: "-=",
    24: "/=",
    25: "^=",
}

# Map BINARY_OP arg to old-style opcode name tokens
BINARY_OP_OPNAME_MAP = {
    0: "BINARY_ADD",
    1: "BINARY_AND",
    2: "BINARY_FLOOR_DIVIDE",
    3: "BINARY_LSHIFT",
    4: "BINARY_MATRIX_MULTIPLY",
    5: "BINARY_MULTIPLY",
    6: "BINARY_MODULO",
    7: "BINARY_OR",
    8: "BINARY_POWER",
    9: "BINARY_RSHIFT",
    10: "BINARY_SUBTRACT",
    11: "BINARY_TRUE_DIVIDE",
    12: "BINARY_XOR",
    13: "INPLACE_ADD",
    14: "INPLACE_AND",
    15: "INPLACE_FLOOR_DIVIDE",
    16: "INPLACE_LSHIFT",
    17: "INPLACE_MATRIX_MULTIPLY",
    18: "INPLACE_MULTIPLY",
    19: "INPLACE_MODULO",
    20: "INPLACE_OR",
    21: "INPLACE_POWER",
    22: "INPLACE_RSHIFT",
    23: "INPLACE_SUBTRACT",
    24: "INPLACE_TRUE_DIVIDE",
    25: "INPLACE_XOR",
}


class Scanner312(Scanner):
    def __init__(self, show_asm=None, debug="", is_pypy=False):
        self.opc = opc
        self.opname = opc.opname
        self.version = (3, 12)
        self.show_asm = show_asm
        self.is_pypy = is_pypy
        self.debug = debug

        self.Token = Token
        self.offset2tok_index = None

        # Bytecode converted into instructions
        self.insts = []

        # Setup opcode classification sets for 3.12
        # No SETUP_LOOP, SETUP_EXCEPT in 3.12
        self.setup_ops = frozenset([self.opc.SETUP_FINALLY, self.opc.SETUP_WITH])
        self.setup_ops_no_loop = frozenset([self.opc.SETUP_FINALLY])

        # Add back break/continue opcodes for parsing
        self.opc.BREAK_LOOP = 80
        self.opc.CONTINUE_LOOP = 119

        self.pop_jump_tf = frozenset(
            [self.opc.POP_JUMP_IF_FALSE, self.opc.POP_JUMP_IF_TRUE]
        )
        self.not_continue_follow = ("END_FINALLY", "POP_BLOCK", "RETURN_VALUE", "RETURN_CONST")

        # Opcodes that can start a statement
        statement_opcodes = [
            self.opc.STORE_FAST,
            self.opc.DELETE_FAST,
            self.opc.STORE_DEREF,
            self.opc.STORE_GLOBAL,
            self.opc.DELETE_GLOBAL,
            self.opc.STORE_NAME,
            self.opc.DELETE_NAME,
            self.opc.STORE_ATTR,
            self.opc.DELETE_ATTR,
            self.opc.STORE_SUBSCR,
            self.opc.POP_TOP,
            self.opc.DELETE_SUBSCR,
            self.opc.RETURN_VALUE,
            self.opc.RETURN_CONST,
            self.opc.RAISE_VARARGS,
            self.opc.BREAK_LOOP,
            self.opc.CONTINUE_LOOP,
        ]

        if hasattr(self.opc, 'POP_BLOCK'):
            statement_opcodes.append(self.opc.POP_BLOCK)

        self.statement_opcodes = frozenset(statement_opcodes) | self.setup_ops_no_loop

        # Designator ops
        self.designator_ops = frozenset(
            [
                self.opc.STORE_FAST,
                self.opc.STORE_NAME,
                self.opc.STORE_GLOBAL,
                self.opc.STORE_DEREF,
                self.opc.STORE_ATTR,
                self.opc.STORE_SUBSCR,
                self.opc.UNPACK_SEQUENCE,
                self.opc.UNPACK_EX,
            ]
        )

        # No JUMP_IF_*_OR_POP in 3.12
        self.jump_if_pop = frozenset()
        self.pop_jump_if_pop = frozenset(
            [
                self.opc.POP_JUMP_IF_TRUE,
                self.opc.POP_JUMP_IF_FALSE,
            ]
        )

        self.statement_opcode_sequences = [
            (self.opc.POP_JUMP_IF_FALSE, self.opc.JUMP_FORWARD),
            (self.opc.POP_JUMP_IF_TRUE, self.opc.JUMP_FORWARD),
        ]

        # Variable argument ops
        varargs_ops = set(
            [
                self.opc.BUILD_LIST,
                self.opc.BUILD_TUPLE,
                self.opc.BUILD_SET,
                self.opc.BUILD_SLICE,
                self.opc.BUILD_MAP,
                self.opc.UNPACK_SEQUENCE,
                self.opc.RAISE_VARARGS,
                self.opc.BUILD_CONST_KEY_MAP,
            ]
        )
        self.varargs_ops = frozenset(varargs_ops)

        # MAKE_FUNCTION flags
        self.MAKE_FUNCTION_FLAGS = tuple(
            """
            default keyword-only annotation closure""".split()
        )

        return

    def resetTokenClass(self):
        return self.setTokenClass(Token)

    def setTokenClass(self, tokenClass):
        self.Token = tokenClass
        return self.Token

    def build_instructions(self, co):
        """Create instruction list from code object."""
        from array import array

        self.code = array("B", co.co_code)
        bytecode = Bytecode(co, self.opc)
        self.build_prev_op()
        self.insts = self.remove_extended_args(list(bytecode))
        self.lines = self.build_lines_data(co)
        self.offset2inst_index = {}
        for i, inst in enumerate(self.insts):
            self.offset2inst_index[inst.offset] = i
        return bytecode

    def build_lines_data(self, code_obj):
        """Generate line-related helper data."""
        from collections import namedtuple

        linestarts = list(self.opc.findlinestarts(code_obj))
        self.linestarts = dict(linestarts)
        if not self.linestarts:
            return []

        lines = []
        LineTuple = namedtuple("LineTuple", ["l_no", "next"])
        _, prev_line_no = linestarts[0]
        offset = 0
        for start_offset, line_no in linestarts[1:]:
            while offset < start_offset:
                lines.append(LineTuple(prev_line_no, start_offset))
                offset += 1
            prev_line_no = line_no

        codelen = len(self.code)
        while offset < codelen:
            lines.append(LineTuple(prev_line_no, codelen))
            offset += 1
        return lines

    def build_prev_op(self):
        """Build prev_op map for navigating backward through bytecode."""
        code = self.code
        codelen = len(code)
        self.prev = self.prev_op = [0]
        for offset in self.op_range(0, codelen):
            op = code[offset]
            for _ in range(instruction_size(op, self.opc)):
                self.prev_op.append(offset)

    def op_range(self, start, end):
        while start < end:
            yield start
            start += instruction_size(self.code[start], self.opc)

    def remove_extended_args(self, instructions):
        """Remove EXTENDED_ARG instructions."""
        new_instructions = []
        last_was_extarg = False
        n = len(instructions)
        for i, inst in enumerate(instructions):
            if (
                inst.opname == "EXTENDED_ARG"
                and i + 1 < n
                and instructions[i + 1].opname != "MAKE_FUNCTION"
            ):
                last_was_extarg = True
                starts_line = inst.starts_line
                is_jump_target = inst.is_jump_target
                offset = inst.offset
                continue
            if last_was_extarg:
                new_inst = inst._replace(
                    starts_line=starts_line,
                    is_jump_target=is_jump_target,
                    offset=offset,
                )
                inst = new_inst
                if i < n:
                    new_prev = self.prev_op[instructions[i].offset]
                    j = instructions[i + 1].offset if i + 1 < n else n
                    if j < len(self.prev_op):
                        old_prev = self.prev_op[j]
                        while j < len(self.prev_op) and self.prev_op[j] == old_prev:
                            self.prev_op[j] = new_prev
                            j += 1
            last_was_extarg = False
            new_instructions.append(inst)
        return new_instructions

    def ingest(
        self, co, classname=None, code_objects={}, show_asm=None
    ) -> Tuple[list, dict]:
        """
        Create tokens from the bytecode of a Python 3.12 code object.

        Handles 3.12-specific opcodes:
        - RESUME: skipped (function entry marker)
        - PUSH_NULL: skipped (call convention detail)
        - BINARY_OP: mapped to old-style BINARY_ADD, INPLACE_ADD etc.
        - CALL: mapped to CALL_FUNCTION_n
        - RETURN_CONST: emitted as RETURN_CONST token
        - JUMP_BACKWARD: mapped to JUMP_BACK
        - END_FOR: emitted as-is
        - CACHE: skipped
        - COPY_FREE_VARS: skipped
        - MAKE_CELL: skipped
        """

        def tokens_append(j, token):
            tokens.append(token)
            self.offset2tok_index[token.offset] = j
            j += 1
            assert j == len(tokens)
            return j

        if not show_asm:
            show_asm = self.show_asm

        bytecode = self.build_instructions(co)

        if show_asm in ("both", "before"):
            print("\n# ---- disassembly:")
            for inst in self.insts:
                print(inst)

        customize = {}

        if self.is_pypy:
            customize["PyPy"] = 0

        # Scan for assertions
        self.load_asserts = set()

        tokens = []
        self.offset2tok_index = {}

        n = len(self.insts)
        for i, inst in enumerate(self.insts):
            assert_can_follow = inst.opname == "POP_JUMP_IF_TRUE" and i + 1 < n
            if assert_can_follow:
                next_inst = self.insts[i + 1]
                if (
                    next_inst.opname == "LOAD_GLOBAL"
                    and next_inst.argval == "AssertionError"
                    and inst.argval is not None
                ):
                    self.load_asserts.add(next_inst.offset)

        # Get jump targets
        self.except_targets = {}
        self.structs = [{"type": "root", "start": 0, "end": len(self.code) - 1}]
        self.loops: List[int] = []
        self.fixed_jumps: Dict[int, int] = {}
        self.ignore_if = set()
        self.not_continue = set()
        self.return_end_ifs = set()
        self.setup_loop_targets = {}
        self.setup_loops = {}

        # Build statement indices
        self.build_statement_indices_312()

        jump_targets = self.find_jump_targets_312(show_asm)

        j = 0
        for i, inst in enumerate(self.insts):
            argval = inst.argval
            op = inst.opcode
            opname = inst.opname

            # Skip certain 3.12-specific opcodes that are not relevant for decompilation
            if opname in ("RESUME", "CACHE", "COPY_FREE_VARS", "MAKE_CELL",
                          "PUSH_EXC_INFO", "INTERPRETER_EXIT", "NOP",
                          "SWAP", "RERAISE", "WITH_EXCEPT_START",
                          "LOAD_FAST_AND_CLEAR"):
                continue

            # PUSH_NULL is a calling convention detail - skip it
            if opname == "PUSH_NULL":
                continue

            # BEFORE_WITH stays as-is for grammar handling
            # (No need to convert here - we handle it in grammar)

            # Insert COME_FROM tokens at jump targets
            if inst.offset in jump_targets:
                jump_idx = 0
                for jump_offset in sorted(jump_targets[inst.offset], reverse=True):
                    come_from_name = "COME_FROM"
                    source_opname = self.insts[
                        self.offset2inst_index[jump_offset]
                    ].opname if jump_offset in self.offset2inst_index else ""

                    if source_opname.startswith("SETUP_"):
                        come_from_type = source_opname[len("SETUP_"):]
                        come_from_name = "COME_FROM_%s" % come_from_type
                    elif inst.offset in self.except_targets:
                        come_from_name = "COME_FROM_EXCEPT_CLAUSE"

                    j = tokens_append(
                        j,
                        Token(
                            opname=come_from_name,
                            attr=jump_offset,
                            pattr=repr(jump_offset),
                            offset="%s_%s" % (inst.offset, jump_idx),
                            has_arg=True,
                            opc=self.opc,
                            has_extended_arg=False,
                            optype=inst.optype,
                        ),
                    )
                    jump_idx += 1

            pattr = inst.argrepr
            opname = inst.opname

            # Strip "NULL + " prefix from LOAD_GLOBAL in Python 3.12
            # dis module adds this to show PUSH_NULL but we handle it separately
            if opname == "LOAD_GLOBAL" and isinstance(pattr, str) and pattr.startswith("NULL + "):
                pattr = pattr[7:]  # Remove "NULL + " prefix

            # Strip "NULL|self + " prefix from LOAD_ATTR in Python 3.12
            # dis module adds this for method-resolution LOAD_ATTR (odd oparg)
            if opname == "LOAD_ATTR" and isinstance(pattr, str) and pattr.startswith("NULL|self + "):
                pattr = pattr[12:]  # Remove "NULL|self + " prefix

            # Handle 3.12-specific opcode translations

            if opname == "BINARY_OP":
                # Map BINARY_OP arg to old-style token name
                op_arg = inst.arg
                if op_arg in BINARY_OP_OPNAME_MAP:
                    opname = BINARY_OP_OPNAME_MAP[op_arg]
                    pattr = BINARY_OP_MAP.get(op_arg, str(op_arg))
                else:
                    opname = "BINARY_OP_%d" % op_arg
                    pattr = str(op_arg)
                j = tokens_append(
                    j,
                    Token(
                        opname=opname,
                        attr=argval,
                        pattr=pattr,
                        offset=inst.offset,
                        linestart=inst.starts_line,
                        op=op,
                        has_arg=inst.has_arg,
                        opc=self.opc,
                        has_extended_arg=inst.has_extended_arg,
                        optype=inst.optype,
                    ),
                )
                continue

            elif opname == "CALL":
                # Map CALL to CALL_FUNCTION with attr=argc
                # The parser's call_fn_name() will transform this to CALL_FUNCTION_N
                # and custom_classfunc_rule() will add the proper grammar rule
                argc = inst.arg
                opname = "CALL_FUNCTION"
                customize[opname] = argc
                j = tokens_append(
                    j,
                    Token(
                        opname=opname,
                        attr=argc,
                        pattr=str(argc),
                        offset=inst.offset,
                        linestart=inst.starts_line,
                        op=op,
                        has_arg=inst.has_arg,
                        opc=self.opc,
                        has_extended_arg=inst.has_extended_arg,
                        optype=inst.optype,
                    ),
                )
                continue

            elif opname == "KW_NAMES":
                # KW_NAMES is emitted before CALL for keyword arguments
                # We'll emit it as-is, the parser will need to handle it
                j = tokens_append(
                    j,
                    Token(
                        opname="KW_NAMES",
                        attr=argval,
                        pattr=pattr,
                        offset=inst.offset,
                        linestart=inst.starts_line,
                        op=op,
                        has_arg=inst.has_arg,
                        opc=self.opc,
                        has_extended_arg=inst.has_extended_arg,
                        optype=inst.optype,
                    ),
                )
                continue

            elif opname == "RETURN_CONST":
                # Emit RETURN_CONST with the constant value
                const = argval
                j = tokens_append(
                    j,
                    Token(
                        opname="RETURN_CONST",
                        attr=argval,
                        pattr=pattr,
                        offset=inst.offset,
                        linestart=inst.starts_line,
                        op=op,
                        has_arg=inst.has_arg,
                        opc=self.opc,
                        has_extended_arg=inst.has_extended_arg,
                        optype=inst.optype,
                    ),
                )
                continue

            elif opname == "JUMP_BACKWARD":
                # Backward jump = loop back
                opname = "JUMP_BACK"
                pattr = argval
                j = tokens_append(
                    j,
                    Token(
                        opname=opname,
                        attr=argval,
                        pattr=pattr,
                        offset=inst.offset,
                        linestart=inst.starts_line,
                        op=op,
                        has_arg=inst.has_arg,
                        opc=self.opc,
                        has_extended_arg=inst.has_extended_arg,
                        optype=inst.optype,
                    ),
                )
                continue

            elif opname == "JUMP_BACKWARD_NO_INTERRUPT":
                opname = "JUMP_BACK"
                pattr = argval
                j = tokens_append(
                    j,
                    Token(
                        opname=opname,
                        attr=argval,
                        pattr=pattr,
                        offset=inst.offset,
                        linestart=inst.starts_line,
                        op=op,
                        has_arg=inst.has_arg,
                        opc=self.opc,
                        has_extended_arg=inst.has_extended_arg,
                        optype=inst.optype,
                    ),
                )
                continue

            elif op in self.opc.CONST_OPS:
                const = argval
                if iscode(const):
                    if const.co_name == "<lambda>":
                        opname = "LOAD_LAMBDA"
                    elif const.co_name == "<genexpr>":
                        opname = "LOAD_GENEXPR"
                    elif const.co_name == "<dictcomp>":
                        opname = "LOAD_DICTCOMP"
                    elif const.co_name == "<setcomp>":
                        opname = "LOAD_SETCOMP"
                    elif const.co_name == "<listcomp>":
                        opname = "LOAD_LISTCOMP"
                    else:
                        opname = "LOAD_CODE"
                    pattr = "<code_object " + const.co_name + ">"
                elif isinstance(const, str):
                    opname = "LOAD_STR"
                else:
                    if isinstance(inst.arg, int) and inst.arg < len(co.co_consts):
                        argval, _ = _get_const_info(inst.arg, co.co_consts)
                    pattr = const

            elif opname == "IMPORT_NAME":
                if "." in str(inst.argval):
                    opname = "IMPORT_NAME_ATTR"

            elif opname == "LOAD_FAST_CHECK":
                # LOAD_FAST_CHECK is a 3.12 variant that raises UnboundLocalError
                # if the variable hasn't been assigned. For decompilation, treat
                # it exactly like LOAD_FAST.
                opname = "LOAD_FAST"

            elif opname == "LOAD_FAST" and argval == ".0":
                opname = "LOAD_ARG"

            elif opname in ("MAKE_FUNCTION", "MAKE_CLOSURE"):
                flags = argval
                opname_new = "MAKE_FUNCTION_%d" % flags
                attr = []
                for flag in self.MAKE_FUNCTION_FLAGS:
                    bit = flags & 1
                    attr.append(bit)
                    flags >>= 1
                attr = attr[:4]
                
                # In Python 3.12, MAKE_FUNCTION doesn't require LOAD_STR
                # but the grammar expects LOAD_CODE LOAD_STR MAKE_FUNCTION_0
                # Insert synthetic LOAD_STR with function name from the preceding code object
                func_name = ""
                if j > 0 and tokens[j-1].kind in ("LOAD_CODE", "LOAD_LAMBDA", "LOAD_GENEXPR",
                                                    "LOAD_DICTCOMP", "LOAD_SETCOMP", "LOAD_LISTCOMP"):
                    prev_code = tokens[j-1].attr
                    if hasattr(prev_code, 'co_qualname'):
                        func_name = prev_code.co_qualname
                    elif hasattr(prev_code, 'co_name'):
                        func_name = prev_code.co_name
                    else:
                        func_name = str(prev_code)
                
                j = tokens_append(
                    j,
                    Token(
                        opname="LOAD_STR",
                        attr=func_name,
                        pattr=repr(func_name),
                        offset="%s_0" % inst.offset,
                        linestart=None,
                        op=self.opc.LOAD_CONST,
                        has_arg=True,
                        opc=self.opc,
                        has_extended_arg=False,
                        optype="const",
                    ),
                )
                j = tokens_append(
                    j,
                    Token(
                        opname=opname_new,
                        attr=attr,
                        pattr=pattr,
                        offset=inst.offset,
                        linestart=inst.starts_line,
                        op=op,
                        has_arg=inst.has_arg,
                        opc=self.opc,
                        has_extended_arg=inst.has_extended_arg,
                        optype=inst.optype,
                    ),
                )
                continue

            elif op in self.varargs_ops:
                pos_args = argval
                opname = "%s_%d" % (opname, pos_args)

            elif opname == "UNPACK_EX":
                before_args = argval & 0xFF
                after_args = (argval >> 8) & 0xFF
                pattr = "%d before vararg, %d after" % (before_args, after_args)
                argval = (before_args, after_args)
                opname = "%s_%d+%d" % (opname, before_args, after_args)

            elif inst.offset in self.load_asserts:
                opname = "LOAD_ASSERT"

            elif opname == "CHECK_EXC_MATCH":
                # In 3.12, CHECK_EXC_MATCH replaces COMPARE_OP for exception checking
                opname = "COMPARE_OP"
                pattr = "exception-match"
                argval = "exception-match"
            
            elif opname == "LOAD_GLOBAL":
                # In 3.12, low bit of arg controls NULL pushing
                # xdis should already handle this, but let's make sure
                # the argval is the name
                pass

            elif opname == "LOAD_ATTR":
                # In 3.12, low bit of arg controls method mode
                # xdis should handle the decoding
                pass

            elif opname == "COMPARE_OP":
                # In 3.12, effective index = arg >> 4
                # xdis handles the decoding, but make sure pattr is set
                if isinstance(argval, str):
                    pattr = argval
                else:
                    pattr = str(argval)

            # Emit the token
            # Emit the token
            j = tokens_append(
                j,
                Token(
                    opname=opname,
                    attr=argval,
                    pattr=pattr,
                    offset=inst.offset,
                    linestart=inst.starts_line,
                    op=op,
                    has_arg=inst.has_arg,
                    opc=self.opc,
                    has_extended_arg=inst.has_extended_arg,
                    optype=inst.optype,
                ),
            )

        # Post-processing: Convert intermediate RETURN_CONST None to JUMP_FORWARD
        # In Python 3.12, if/elif/else branches end with RETURN_CONST None instead
        # of JUMP_FORWARD. We convert non-final RETURN_CONST None to JUMP_FORWARD
        # so the existing grammar for if/else works properly.
        if len(tokens) >= 2:
            last_return_idx = None
            for idx in range(len(tokens) - 1, -1, -1):
                if tokens[idx].kind == "RETURN_CONST":
                    last_return_idx = idx
                    break
            
            if last_return_idx is not None:
                for idx in range(len(tokens)):
                    if (tokens[idx].kind == "RETURN_CONST" 
                        and idx != last_return_idx
                        and tokens[idx].attr is None):
                        # Find the target: the next COME_FROM or the end
                        # This RETURN_CONST None acts as a branch exit 
                        # Convert to JUMP_FORWARD pointing to the end of the if/else chain
                        target = tokens[-1].offset if isinstance(tokens[-1].offset, int) else off2int(tokens[-1].offset)
                        tokens[idx] = Token(
                            opname="JUMP_FORWARD",
                            attr=target,
                            pattr=repr(target),
                            offset=tokens[idx].offset,
                            linestart=tokens[idx].linestart,
                            op=tokens[idx].op,
                            has_arg=True,
                            opc=self.opc,
                            has_extended_arg=False,
                            optype="jrel",
                        )

        # Post-processing: Strip tokens after the last RETURN_CONST None
        # Python 3.12's inline comprehensions leave exception cleanup tokens
        # (POP_TOP, STORE_FAST, etc.) after the module's final RETURN_CONST None.
        # These can't be parsed, so we remove them.
        # Only strip when RETURN_CONST returns None (module level cleanup).
        # Don't strip after RETURN_CONST with a value (e.g. return 1).
        if len(tokens) >= 2:
            last_rc_idx = None
            for idx in range(len(tokens) - 1, -1, -1):
                if tokens[idx].kind == "RETURN_CONST" and tokens[idx].pattr in (None, 'None'):
                    last_rc_idx = idx
                    break
            if last_rc_idx is not None and last_rc_idx < len(tokens) - 1:
                # Remove all tokens after the last RETURN_CONST None
                tokens = tokens[:last_rc_idx + 1]
        # Post-processing: detect BREAK_LOOP
        jump_back_targets: Dict[int, int] = {}
        for token in tokens:
            if token.kind == "JUMP_BACK":
                jump_back_targets[token.attr] = token.offset

        if jump_back_targets:
            loop_ends = []
            next_end = tokens[len(tokens) - 1].off2int() + 10 if tokens else 10

            new_tokens = []
            for i, token in enumerate(tokens):
                opname = token.kind
                offset = token.offset
                if offset == next_end:
                    if loop_ends:
                        loop_ends.pop()
                    next_end = (
                        loop_ends[-1]
                        if len(loop_ends)
                        else tokens[len(tokens) - 1].off2int() + 10
                    )

                if offset in jump_back_targets:
                    next_end = off2int(jump_back_targets[offset], prefer_last=False)
                    loop_ends.append(next_end)

                # Turn JUMP_FORWARD into BREAK_LOOP when inside a loop
                if opname == "JUMP_FORWARD" and len(loop_ends):
                    jump_target = token.attr
                    jj = i
                    while jj > 0 and tokens[jj - 1].kind in ("POP_TOP", "POP_BLOCK", "POP_EXCEPT"):
                        jj -= 1
                        if tokens[jj].linestart:
                            break
                    token_with_linestart = tokens[jj]
                    if token_with_linestart.linestart:
                        token.kind = "BREAK_LOOP"

                new_tokens.append(token)
            tokens = new_tokens

        if show_asm in ("both", "after"):
            print("\n# ---- tokenization:")
            for t in tokens.copy():
                print(t.format(line_prefix=""))
            print()

        return tokens, customize

    def build_statement_indices_312(self):
        """Build statement indices for 3.12 bytecode."""
        code = self.code
        start = 0
        end = codelen = len(code)

        prelim = self.inst_matches(start, end, self.statement_opcodes)
        stmts = self.stmts = set(prelim)

        pass_stmts = set()
        for sequence in self.statement_opcode_sequences:
            for i in self.op_range(start, end - (len(sequence) + 1)):
                match = True
                for elem in sequence:
                    if elem != code[i]:
                        match = False
                        break
                    i += instruction_size(code[i], self.opc)
                if match is True:
                    i = self.prev_op[i]
                    stmts.add(i)
                    pass_stmts.add(i)

        if pass_stmts:
            stmt_offset_list = list(stmts)
            stmt_offset_list.sort()
        else:
            stmt_offset_list = prelim

        self.next_stmt = slist = []
        last_stmt_offset = -1
        i = 0
        for stmt_offset in stmt_offset_list:
            # In 3.12 there's no JUMP_ABSOLUTE, skip that check
            # Exclude FOR_ITER + designators
            if code[stmt_offset] in self.designator_ops:
                j2 = self.prev_op[stmt_offset]
                while code[j2] in self.designator_ops:
                    j2 = self.prev_op[j2]
                if code[j2] == self.opc.FOR_ITER:
                    stmts.remove(stmt_offset)
                    continue
            slist += [stmt_offset] * (stmt_offset - i)
            last_stmt_offset = stmt_offset
            i = stmt_offset
        slist += [codelen] * (codelen - len(slist))

    def find_jump_targets_312(self, debug) -> dict:
        """Find jump targets for 3.12 bytecode.

        When a forward jump target lands on a NOP or other skipped opcode,
        we redirect it to the next real (non-skipped) instruction so
        that COME_FROM tokens are generated at the correct offset.
        Only forward jumps are redirected; backward jumps (loops) are
        left as-is to preserve loop structure.
        """
        skipped_opcodes = frozenset((
            "NOP", "CACHE", "PUSH_NULL",
        ))

        # Forward-only jump opcodes (not JUMP_BACKWARD, FOR_ITER)
        forward_jump_names = frozenset((
            "JUMP_FORWARD", "POP_JUMP_IF_FALSE", "POP_JUMP_IF_TRUE",
            "POP_JUMP_IF_NONE", "POP_JUMP_IF_NOT_NONE",
        ))

        targets = {}
        for i, inst in enumerate(self.insts):
            if inst.opcode in self.opc.JREL_OPS:
                target = inst.argval
                if target is not None:
                    # Only forward NOP targets for forward jumps
                    if (inst.opname in forward_jump_names
                            and target in self.offset2inst_index):
                        target_idx = self.offset2inst_index[target]
                        target_inst = self.insts[target_idx]
                        if target_inst.opname in skipped_opcodes:
                            # Walk forward to find next non-skipped instruction
                            for k in range(target_idx + 1, len(self.insts)):
                                if self.insts[k].opname not in skipped_opcodes:
                                    target = self.insts[k].offset
                                    break
                    targets[target] = targets.get(target, []) + [inst.offset]
        return targets

    # Delegate these to prevent errors from parent class
    def get_inst(self, offset):
        if offset not in self.offset2inst_index:
            # Try adjusting for EXTENDED_ARG
            adj_offset = offset - instruction_size(self.opc.EXTENDED_ARG, self.opc)
            if adj_offset in self.offset2inst_index:
                return self.insts[self.offset2inst_index[adj_offset]]
            # Fall back to closest
            for off in sorted(self.offset2inst_index.keys()):
                if off >= offset:
                    return self.insts[self.offset2inst_index[off]]
            return self.insts[-1]
        return self.insts[self.offset2inst_index[offset]]

    def get_target(self, offset, extended_arg=0):
        inst = self.get_inst(offset)
        if inst.opcode in self.opc.JREL_OPS:
            target = inst.argval
        else:
            target = xdis.next_offset(inst.opcode, self.opc, inst.offset)
        return target

    def inst_matches(self, start, end, instr, target=None, include_beyond_target=False):
        try:
            None in instr
        except Exception:
            instr = [instr]

        if start not in self.offset2inst_index:
            # Find closest offset
            for off in sorted(self.offset2inst_index.keys()):
                if off >= start:
                    start = off
                    break
            else:
                return []

        first = self.offset2inst_index.get(start, 0)
        result = []
        for inst in self.insts[first:]:
            if inst.opcode in instr:
                if target is None:
                    result.append(inst.offset)
                else:
                    t = self.get_target(inst.offset)
                    if include_beyond_target and t >= target:
                        result.append(inst.offset)
                    elif t == target:
                        result.append(inst.offset)
            if inst.offset >= end:
                break
        return result

    def next_offset(self, op, offset):
        return xdis.next_offset(op, self.opc, offset)

    def prev_offset(self, offset):
        return self.insts[self.offset2inst_index[offset] - 1].offset


if __name__ == "__main__":
    from xdis.version_info import PYTHON_VERSION_TRIPLE, version_tuple_to_str

    if PYTHON_VERSION_TRIPLE[:2] == (3, 12):
        import inspect

        co = inspect.currentframe().f_code
        tokens, customize = Scanner312().ingest(co)
        for t in tokens:
            print(t.format())
    else:
        print(
            f"Need to be Python 3.12 to demo; I am version {version_tuple_to_str()}."
        )
