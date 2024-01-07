Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

function Find-MediaFiles {
    param (
        [string]$drive
    )

    $mediaFiles = @()
    $audioExtensions = @('.mp3', '.wav', '.flac')
    $videoExtensions = @('.mp4', '.mkv', '.avi')
    $drive

    Get-ChildItem -Recurse -Path $drive | ForEach-Object {
        $fileExtension = $_.Extension.ToLower()

        if ($audioExtensions -contains $fileExtension -or $videoExtensions -contains $fileExtension) {
            $mediaFiles += "$($_.Name) "# - $($_.FullName)
        }
    }

    return $mediaFiles
}

function Write-ToFile {
    param (
        [string]$drive,
        [string[]]$files
    )

    $cwd = Get-Location
    $cwd
    $outFile = "$cwd\" + $drive.Replace(":\", "") + "_media_files.txt"
    $outFile
    $files | Out-File -FilePath $outFile -Encoding utf8
}



$drives = Get-WmiObject Win32_LogicalDisk | Where-Object { $_.DriveType -eq 3 } | ForEach-Object { $_.DeviceID + "\" }
# $drives

foreach ($drive in $drives) {

    $mediaFiles = Find-MediaFiles -drive $drive

    if ($mediaFiles.Count -gt 0) {
        Write-ToFile -drive $drive -files $mediaFiles
    }
}
