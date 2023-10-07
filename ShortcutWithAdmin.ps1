$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$Home\Desktop\AdminTest.lnk")
#$Shortcut.WindowStyle = 7 # 3=Maximized 4=Normal 7=Minimized
#$Shortcut.IconLocation = "$iconPath, $iconIndex"
$Shortcut.TargetPath = "C:\WINDOWS\System32\notepad.exe"
#$Shortcut.Arguments = 
#$Shortcut.WorkingDirectory = 
$Shortcut.Save()

$bytes = [System.IO.File]::ReadAllBytes("$Home\Desktop\AdminTest.lnk")
#Write-Host $bytes()
$bytes[0x15] = $bytes[0x15] -bor 0x20 #Sets byte 21 (ox15) bi 6 (ox20) ON
[System.IO.File]::WriteAllBytes("$Home\Desktop\AdminTest.lnk", $bytes)