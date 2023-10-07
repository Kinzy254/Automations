function Get-ShortcutIcon {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $true, ValueFromPipeline = $true)]
        [Alias('FullName')]
        [string]$Path #Needs to be absolute path
    )
    switch ([System.IO.Path]::GetExtension($Path)) {
        '.lnk' {
            $WshShell = New-Object -ComObject WScript.Shell
            $shortcut = $WshShell.CreateShortcut($Path)
            $iconPath = $shortcut.IconLocation
            $iconInfo = if ($iconPath -match '^,(\d+)') 
            {
                [PSCustomObject]@{
                    IconPath = $shortcut.TargetPath; IconIndex = [int]$Matches[1]
                }
            }
            else {
                [PSCustomObject]@{
                    IconPath = $iconPath; IconIndex = 0
                }
            }

            #Clean up :)
            $null = [System.Runtime.InteropServices.Marshal]::ReleaseComObject($shortcut)
            $null = [System.Runtime.InteropServices.Marshal]::ReleaseComObject($WshShell)
            [System.GC]::Collect()
            [System.GC]::WaitForPendingFinalizers()

            #Return icon info
            $iconInfo
        }
        '.url' {
            $content = Get-Content -Path $Path -Raw
            $iconPath = [regex]::Match($content, '(?im)^\s*IconFile\s*=\s*(.*)').Groups[1].Value
            $iconPath = [regex]::Match($content, '(?im)^\s*IconIndex\s*=\s*(\d+)').Groups[1].Value
            [PSCustomObject]@{
                IconPath = $iconPath; IconIndex = [int]$iconIndex
            }
        }
        Default {Write-Warning "'$Path' does not point to a .lnk file"}
    }
}

#Usage :)
$shortcutPath = 'C:\Users\Angel\Desktop\ChangeTest.lnk'
$iconInfo = Get-ShortcutIcon -Path $shortcutPath

#Display the icon info
$iconInfo.IconPath
$iconInfo.IconIndex

