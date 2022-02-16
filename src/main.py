import lexer as my_lexer
from my_parser import parser
from pathlib import Path

if __name__ == "__main__":
    path = Path("../exemplary_data/test2.m")
    with open(path, "r") as f:
        ast = parser.parse(f.read(), lexer=my_lexer.lexer)
    result = ast.convert(0)
    print(result)

    dir = path.parents[0]
    name = path.name.split(".")[0]
    print(str(name))
    new_path = dir / f"{str(name)}_out.py"
    with open(new_path, "w") as f:
        f.write(result)
