Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

param (
    [string]$taskName,
    [string]$description,
    [string]$filePath,
    [string[]]$arguments,
    [string]$interval,
    [string]$time
)



# Define the task action (replace "YourScript.ps1" and "C:\Path\to\YourScript.ps1" with your script details)
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument '-File C:\Path\to\YourScript.ps1'

# Define the trigger (adjust the settings as needed)
$trigger = New-ScheduledTaskTrigger -Daily -At "3:00 AM"

# Create the task
$task = Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "YourScheduledTask" -Description "Description of your task"

# Optionally, run the task immediately
Start-ScheduledTask -Task $task.TaskName
