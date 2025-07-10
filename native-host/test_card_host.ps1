param (
    [string]$Json = '{"action":"get_atr"}'
)

$venvPython = Join-Path $PSScriptRoot 'venv311\Scripts\python.exe'
$scriptPath = Join-Path $PSScriptRoot 'card_host.py'

$enc = [System.Text.Encoding]::UTF8
$data = $enc.GetBytes($Json)
$len = [System.BitConverter]::GetBytes($data.Length)

$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $venvPython
$psi.Arguments = $scriptPath
$psi.RedirectStandardInput = $true
$psi.RedirectStandardOutput = $true
$psi.UseShellExecute = $false
$psi.CreateNoWindow = $true

$proc = New-Object System.Diagnostics.Process
$proc.StartInfo = $psi
$proc.Start() | Out-Null

$stdin = $proc.StandardInput.BaseStream
$stdin.Write($len, 0, 4)
$stdin.Write($data, 0, $data.Length)
$stdin.Flush()
$stdin.Close()

$stdout = $proc.StandardOutput.BaseStream
$lenBuffer = New-Object byte[] 4
$stdout.Read($lenBuffer, 0, 4) | Out-Null
$responseLength = [BitConverter]::ToInt32($lenBuffer, 0)

$responseBuffer = New-Object byte[] $responseLength
$stdout.Read($responseBuffer, 0, $responseLength) | Out-Null
$response = [System.Text.Encoding]::UTF8.GetString($responseBuffer)

$proc.WaitForExit()

Write-Host "`Native host response:`n$response"
