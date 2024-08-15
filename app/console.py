import importlib
import os
import asyncio
from typing import Any
from ptpython.repl import embed, PythonRepl
from app.database import session_factory
from ptpython.layout import CompletionVisualisation


def import_all(file_or_dir_path: str, locals_dict: dict[str, Any]) -> None:
    if file_or_dir_path in ["app/console.py", "app/main.py"]:
        return

    if not os.path.isdir(file_or_dir_path) and file_or_dir_path.endswith(".py"):
        package_name = file_or_dir_path[:-3].replace("/", ".")
        module = importlib.import_module(package_name)
        keys_to_import = [
            k for k in module.__dict__.keys() if not k.startswith("__")
        ]
        print(f"From {package_name} importing {", ".join(keys_to_import)}")
        for key in module.__dict__:
            if key in keys_to_import:
                locals_dict[key] = module.__dict__[key]
        return

    if os.path.isdir(file_or_dir_path):
        for child_name in os.listdir(file_or_dir_path):
            child_path = f"{file_or_dir_path}/{child_name}"
            import_all(child_path, locals_dict)


def configure(repl: PythonRepl) -> None:
    repl.use_code_colorscheme("monokai")
    repl.show_signature = True
    repl.show_docstring = True
    repl.show_meta_enter_message = True
    repl.completion_visualisation = CompletionVisualisation.POP_UP
    repl.enable_auto_suggest = True
    repl.enable_fuzzy_completion = True
    repl.complete_while_typing = True
    repl.highlight_matching_parenthesis = True


print(
    r"""
############################################
#                                          #
#   _____         _        _    ____ ___   #
#  |  ___|_ _ ___| |_     / \  |  _ \_ _|  #
#  | |_ / _` / __| __|   / _ \ | |_) | |   #
#  |  _| (_| \__ \ |_   / ___ \|  __/| |   #
#  |_|  \__,_|___/\__| /_/   \_\_|  |___|  #
#                                          #
############################################
Welcome to the FastAPI interactive shell!
Brought to you by https://hackingmentality.com
"""
)
import_all("app", locals())
print("\n")
locals()["session"] = session_factory()
asyncio.run(
    embed(globals(), locals(), patch_stdout=True, return_asyncio_coroutine=True, configure=configure)  # type: ignore[func-returns-value]
)
