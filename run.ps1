# Run the local checkout: install uv if it is missing, install dependencies, and start CareerPilot.
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
    $env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
}
uv run --project $PSScriptRoot careerpilot @args
exit $LASTEXITCODE
