$port = 8000
$url = "http://localhost:$port/Panel.html"
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$port/")
try {
    $listener.Start()
    Write-Host "--- SERVIDOR DEL PANEL ACTIVADO ---" -ForegroundColor Cyan
    Write-Host "Accediendo a: $url" -ForegroundColor Green
    Write-Host "NO CIERRES ESTA VENTANA MIENTRAS USES EL PANEL" -ForegroundColor Yellow
    Start-Process $url
    while ($listener.IsListening) {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response
        $path = $request.Url.LocalPath.TrimStart('/')
        if ($path -eq "") { $path = "Panel.html" }
        $filePath = Join-Path (Get-Location) $path
        if (Test-Path $filePath) {
            $bytes = [System.IO.File]::ReadAllBytes($filePath)
            $response.OutputStream.Write($bytes, 0, $bytes.Length)
        } else {
            $response.StatusCode = 404
        }
        $response.Close()
    }
} finally {
    $listener.Stop()
}