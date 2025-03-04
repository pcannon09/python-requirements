if ($args[0] -eq "--ungen") {
    Write-Host "[ WARN ] Are you sure that you want to remove every generated file and dir? (CTRL + C to cancel, press Enter to continue)"
    Read-Host
    Write-Host "[ DELETE ] Deleting dir '.private' " -NoNewline
    Remove-Item -Path ".\.private" -Recurse -Force
    Write-Host "[ DONE ]"

    exit
}

Write-Host "[ CREATE ] Creating '.private/logs' dir " -NoNewline
New-Item -ItemType Directory -Path ".\.private\logs" -Force | Out-Null
Write-Host "[ DONE ]"
