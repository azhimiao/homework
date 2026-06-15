"""Skill-Core tooling library."""

from .compiler import compile_skill, compile_skill_dir
from .diff import check_drift
from .export import export_ir_json, ir_to_dict
from .install import install_skill
from .ir_parser import IRDocument, parse_ir
from .migrate import migrate_file, migrate_scan
from .registry import build_registry, find_skill, list_skills, load_registry
from .scaffold import scaffold
from .test_runner import run_tests
from .validate import validate_skill_dir

__all__ = [
    "IRDocument",
    "parse_ir",
    "compile_skill",
    "compile_skill_dir",
    "check_drift",
    "export_ir_json",
    "ir_to_dict",
    "install_skill",
    "migrate_file",
    "migrate_scan",
    "build_registry",
    "find_skill",
    "list_skills",
    "load_registry",
    "scaffold",
    "run_tests",
    "validate_skill_dir",
]
