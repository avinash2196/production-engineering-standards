$ErrorActionPreference = "Stop"

python "$PSScriptRoot/validate_repository.py"

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
