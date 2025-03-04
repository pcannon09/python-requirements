# NOTE: Make sure to have 'pyinstaller' installed

param (
    [string]$action,
    [string]$arg2
)

if ([string]::IsNullOrEmpty($action)) {
    $compileFiles = @("main.py", "File.py", "Debug.py", "ReqInfo.py")
    $compileFilesStr = $compileFiles -join " "

    Write-Host "Files to compile: $compileFilesStr"

    if (Test-Path "./python/build") {
        Remove-Item "./python/build" -Recurse -Force
    }
    if (Test-Path "./python/dist") {
        Remove-Item "./python/dist" -Recurse -Force
    }

    New-Item -ItemType Directory -Path "python" -Force | Out-Null

    Set-Location "python"

    pyinstaller --onefile $compileFilesStr

    Move-Item -Path "./dist/main" -Destination "./dist/py-req"

    Set-Location ".."

    New-Item -ItemType Directory -Path "bin" -Force | Out-Null
    Move-Item -Path "./python/dist/py-req" -Destination "./bin/"
    Remove-Item -Path "./python/dist", "./python/build", "./python/main.spec" -Recurse -Force
}
elseif ($action -eq "run") {
    & "./python/dist/main/py-req" $arg2
}

