# Open the Allure report. Results are linked at .\allure-results.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$javaHome = "C:\Program Files\Eclipse Adoptium\jre-21.0.12.101-hotspot"
$allureBin = "C:\Users\pione\AppData\Local\allure\allure-2.46.1\bin"
if (Test-Path $javaHome) { $env:JAVA_HOME = $javaHome }
if (Test-Path $allureBin) { $env:Path = "$allureBin;$env:JAVA_HOME\bin;" + $env:Path }

allure serve allure-results
