from ..loader import load_module_from_file, ModuleProxy
from pathlib import Path
from typing import cast
import pytest, ast

class Visitor(ast.NodeVisitor):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.results: dict[str, list[ast.AST]] = {}

    def clear_results(self) -> None:
        self.results = {}

    def _add_result(self, name: str, value: ast.AST) -> None:
        if name not in self.results:
            self.results[name] = []
        self.results[name].append(value)

    def visit_ClassDef(self, node: ast.AST) -> None:
        self._add_result('classes', node)
        self.generic_visit(node)

@pytest.fixture
def modfile():
    return Path(__file__).parent / '_testmod.py'

def test_loader(modfile: Path) -> None:
    module = load_module_from_file(
        modfile,
        'testmod'
    )
    assert module is not None
    assert isinstance(module, ModuleProxy)

    module = cast(ModuleProxy, module)

    assert module.safe()

    module.PublicClass
    module._PrivateClass
    module.pubattr
    module._privattr

    with pytest.raises(TypeError):
        module.safe(1) # type: ignore

    module.safe(True)

def test_find_class(modfile: Path) -> None:
    module = load_module_from_file(
        modfile,
        'testmod'
    )

    tree = module.ast_tree

    vst = Visitor()
    vst.visit(tree)

def test_loader_errors() -> None:
    with pytest.raises(FileNotFoundError):
        load_module_from_file(
            Path(__file__).parent / '_test.py',
            'test'
        )
