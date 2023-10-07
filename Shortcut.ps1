$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WShShell.CreateShortcut("$Home\Desktop\notepad.lnk")
#$Shortcut.WindowStyle = 7 # 3=Maximized 4=Normal 7=Minimized
#$Shortcut.IconLocation = "$iconPath, $iconIndex"
$Shortcut.TargetPath = "%ProgramFiles%\CodeBlocks\codeblocks.exe"
#$Shortcut.Arguments = 
#$Shortcut.WorkingDirectory = 
$Shortcut.Save()