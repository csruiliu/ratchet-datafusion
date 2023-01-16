# Ratchet on DuckDB 

Install the DuckDB python client from source code.

It is recommended to use python virtual environment to install it.

```
cd <DuckDB codebase>/tools/pythonpkg 
python setup.py install
```

## Modification from DuckDB 

When we want to add a new Python API for DuckDB, we usually need to modified the source code in `tools/pythonpkg/src`. Also, to make sure the new added Python API can be detected by IDEs, we need to run `scripts/regenerate_python_stubs.sh` to regenerate the corresponding `__ini__.pyi` file.

Prerequisite Python Package

+ mypy
+ pybind11