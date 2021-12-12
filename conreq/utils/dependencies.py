import subprocess

import requirements


class DependencyConflict(Exception):
    pass


def find_py_dependencies(ignore_conflicts: bool = False) -> set[str]:
    """Returns a set of all Python dependencies required by this Conreq instance."""
    with open("requirements.txt", encoding="utf-8") as req_file:
        all_python_reqs = set()
        for req in requirements.parse(req_file):
            req_string = req.name or req.uri
            if req.specs:
                req_string += ",".join(
                    [(operator + version) for operator, version in req.specs],
                )
            all_python_reqs.add(req_string)

    return all_python_reqs


def install_py_dependencies() -> None:
    """Installs all dependencies required by this Conreq instance."""
    subprocess.run(["pip", "install", *find_py_dependencies()], check=True)
