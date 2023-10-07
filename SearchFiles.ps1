#$searchPath = "$Home\Desktop"
#$foundFile = Get-ChildItem -Path $searchPath -Filter "ChangeTest.lnk" -Recurse -File | Select-Object -ExpandProperty FullName
#$foundFile

$searchPath = "D:\"
$foundFile = Get-ChildItem -Directory $searchPath -Recurse | Select-Object -ExpandProperty FullName
$foundFile


function Archive {
    param (
    [Parameter(Mandatory = $true, ValueFromPipeline = $true)]
    [string]$DirPath
    [string]$rarPath
)
$archivePath = $DirPath + '.rar'
#$archivePath
Start-Process -FilePath $rarPath -ArgumentList "a -r $archivePath $DirPath" -WindowStyle Hidden -Wait
}

