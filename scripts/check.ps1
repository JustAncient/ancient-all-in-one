param(
    [string]$Python = "C:\Users\Ancie\AppData\Local\Programs\Python\Python313\python.exe"
)

$ErrorActionPreference = "Stop"

& $Python -m unittest discover -s tests
& $Python -m compileall ancient_all_in_one tests
& $Python -m ruff check ancient_all_in_one tests
