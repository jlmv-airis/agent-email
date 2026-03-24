@echo off
title Servidor del Panel - Asesorias IA
echo Iniciando servidor local en el puerto 8000...
powershell -ExecutionPolicy Bypass -Command "$s = New-Object System.Net.HttpListener; $s.Prefixes.Add('http://localhost:8000/'); $s.Start(); Write-Host '--- SERVIDOR DEL PANEL ACTIVO ---' -Fore Green; Write-Host 'Accediendo a http://localhost:8000/Panel.html' -Fore Cyan; Start-Process 'http://localhost:8000/Panel.html'; while($s.IsListening){$c=$s.GetContext(); $p=$c.Request.Url.LocalPath.TrimStart('/'); if($p -eq ''){$p='Panel.html'}; $f=Join-Path (Get-Location) $p; if(Test-Path $f){$b=[System.IO.File]::ReadAllBytes($f); $c.Response.OutputStream.Write($b,0,$b.Length)}else{$c.Response.StatusCode=404}; $c.Response.Close()}"
pause