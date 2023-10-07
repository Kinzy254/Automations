$filePath = "C:\Users\Angel\Desktop\notepad.lnk"
$startupFolder = [Environment]::GetFolderPath("Startup")
#$startupFolder
$startupPath = Join-Path -Path $startupFolder -ChildPath (Split-Path $shortcutPath -Leaf)
#$startupPath
Copy-Item -Path $shortcutPath -Destination $startupPath
