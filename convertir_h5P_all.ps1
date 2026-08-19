# Mostrar mensaje inicial
Write-Host "Buscando archivos .h5p en la carpeta actual..." -ForegroundColor Cyan

# Obtener todos los archivos con extensión .h5p
$archivos = Get-ChildItem -Filter *.h5p

# Verificar si hay archivos para procesar
if ($archivos.Count -eq 0) {
    Write-Host "No se encontraron archivos .h5p en esta carpeta." -ForegroundColor Yellow
    exit
}

Write-Host "Se encontraron $($archivos.Count) archivo(s). Iniciando conversión..." -ForegroundColor Cyan

# Recorrer cada archivo y ejecutar el script de Python
foreach ($archivo in $archivos) {
    Write-Host "---------------------------------------------------"
    Write-Host "Procesando: $($archivo.Name)" -ForegroundColor Green
    
    # Ejecutar Python pasando el nombre del archivo con comillas (por si tiene espacios)
    python h5p_a_pdf.py "$($archivo.Name)"
}

Write-Host "---------------------------------------------------"
Write-Host "¡Proceso por lotes finalizado con éxito!" -ForegroundColor Cyan