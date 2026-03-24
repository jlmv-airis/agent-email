@echo off
title Servidor del Panel - Agente de Email AI
echo.
echo --- INICIANDO INTERFAZ DE USUARIO ---
echo.
echo El panel estara disponible en: http://localhost:8000/Panel.html
echo (n8n debe estar corriendo en http://localhost:5678)
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command "$listener = New-Object System.Net.HttpListener; $listener.Prefixes.Add('http://localhost:8000/'); try { $listener.Start(); Write-Host '>>> SERVIDOR ACTIVO EN EL PUERTO 8000' -ForegroundColor Green; Start-Process 'http://localhost:8000/Panel.html'; while ($listener.IsListening) { $context = $listener.GetContext(); $path = $context.Request.Url.LocalPath.TrimStart('/'); if ($path -eq '') { $path = 'Panel.html' }; $file = Join-Path $PWD $path; if (Test-Path $file) { $buffer = [System.IO.File]::ReadAllBytes($file); $context.Response.ContentLength64 = $buffer.Length; $context.Response.OutputStream.Write($buffer, 0, $buffer.Length) } else { $context.Response.StatusCode = 404 }; $context.Response.Close() } } catch { Write-Host 'ERROR: No se pudo iniciar el servidor en el puerto 8000. Asegurate de que no este en uso.' -ForegroundColor Red; pause }"
pause
