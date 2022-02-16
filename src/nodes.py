from __future__ import annotations
from abc import ABC, abstractmethod
from ast import Expression, stmt
from dataclasses import dataclass, field
from multiprocessing.sharedctypes import Value
from turtle import right
from typing import Any, Union, Optional, ClassVar

TAB = "    "

OP_MAPPING = {
    "^": "**",
    "|": "or",
    "~": "not",
    "!": "not",
    "&": "and"
}

class Node(ABC):
    # @abstractmethod
    # def convert(self, indent=0):
    #     pass

    @abstractmethod
    def convert(self, indent_level=0):
        pass


@dataclass
class IndentAwareNode:
    pass


@dataclass
class WhileNode(Node, IndentAwareNode):
    expr: ExprNode
    stmt_list: StatementListNode

    def convert(self, indent=0):
        print(type(self).__name__, indent)
        return f"{indent * TAB}while {self.expr.convert()}:\n{self.stmt_list.convert(indent + 1)}"


@dataclass
class StatementListNode(Node, IndentAwareNode):
    statements: list[StatementNode] = field(default_factory=list)

    def convert(self, indent=0) -> str:
        converted = [stmt.convert(indent) for stmt in self.statements]
        return "\n".join(converted)


@dataclass
class StatementNode(Node, IndentAwareNode):
    statement: Union[ExprNode, IfStmtNode, WhileNode, str, FuncStmtNode]

    def convert(self, indent=0):
        print(type(self).__name__, indent)
        return (
            f"{indent * TAB}{self.statement}"
            if isinstance(self.statement, str)
            else self.statement.convert(indent)
        )


@dataclass
class IfStmtNode(Node, IndentAwareNode):
    expr: ExprNode
    stmt_list: StatementListNode
    elseif_stmt: ElseIfStmtNode

    def convert(self, indent=0):
        print(type(self).__name__, indent)
        return f"{indent * TAB}if {self.expr.convert(indent)}:\n{self.stmt_list.convert(indent + 1)}\n{self.elseif_stmt.convert(indent)}"


@dataclass
class ElseIfStmtNode(Node, IndentAwareNode):
    stmt_list: Optional[StatementListNode] = None
    elseif_stmt: Optional[ElseIfStmtNode] = None
    expr: Optional[ExprNode] = None

    def convert(self, indent=0) -> str:
        if self.expr:
            return f"{TAB * indent}elif {self.expr.convert(indent)}:\n{self.stmt_list.convert(indent + 1)}\n{self.elseif_stmt.convert(indent)}"
        elif self.stmt_list:
            return f"{TAB * indent}else:\n{self.stmt_list.convert(indent + 1)}"
        return ""


@dataclass
class ExprNode(Node, IndentAwareNode):
    data: Union[str, int, UniExprNode, BinOpExprNode]

    def convert(self, indent=0):
        print(type(self).__name__, indent)
        return (
            str(self.data)
            if isinstance(self.data, (str, int))
            else self.data.convert(indent)
        )

@dataclass
class ExprStmtNode(Node, IndentAwareNode):
    data: ExprNode

    def convert(self, indent=0):
        print(type(self).__name__, indent)
        return f"{indent * TAB}{self.data.convert(indent)}"


@dataclass
class UniExprNode(Node, IndentAwareNode):
    data: ExprNode
    sign: str

    def convert(self, indent=0):
        print(type(self).__name__, indent)
        return f"{self.sign}{self.data.convert(indent)}"


@dataclass
class BinOpExprNode(Node, IndentAwareNode):
    left: ExprNode
    op: str
    right: ExprNode

    def convert(self, indent=0):
        print(type(self).__name__, indent)
        op = OP_MAPPING.get(str(self.op), str(self.op))
        return f"{self.left.convert(indent)} {op} {self.right.convert(indent)}"


@dataclass
class ParenExprNode(Node, IndentAwareNode):
    expr: ExprNode

    def convert(self, indent=0):
        print(type(self).__name__, indent)
        return f"({self.expr.convert(indent)})"


@dataclass
class FuncStmtNode(Node, IndentAwareNode):
    id: str
    function_call: FuncCallNode
    stmt_list: StatementListNode

    def convert(self, indent=0):
        print(type(self).__name__, indent)
        return f"{TAB * indent}def {self.function_call.convert(indent)}:\n{self.stmt_list.convert(indent + 1)}\n{TAB * (indent + 1)}return {self.id}\n"


@dataclass
class FuncCallNode(Node, IndentAwareNode):
    id: str
    args: ArgsNode

    def convert(self, indent=0):
        print(type(self).__name__, indent)
        return f"{self.id}({self.args.convert(indent)})"


@dataclass
class ArgsNode(Node, IndentAwareNode):
    args: list[str, ExprNode] = field(default_factory=list)

    def convert(self, indent=0):
        print(type(self).__name__, indent)
        to_str = lambda n: n if isinstance(n, str) else n.convert(indent)
        converted = list(map(to_str, self.args))
        return ",".join(converted)
