# Script PowerShell para agendar a execução diária do Agente de Notícias às 13:00 (Horário de Brasília)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$vbsPath = Join-Path $scriptDir "executar_silencioso.vbs"

$taskName = "AgenteNoticiasDIO"
$action = New-ScheduledTaskAction -Execute "wscript.exe" -Argument "`"$vbsPath`""
$trigger = New-ScheduledTaskTrigger -Daily -At 13:00
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description "Curadoria diária automática de notícias de IA e tecnologia às 13h" -Force | Out-Null

Write-Host "======================================================================" -ForegroundColor Green
Write-Host " [SUCESSO] Rotina diária agendada para todos os dias às 13:00!" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "Tarefa: $taskName"
Write-Host "Horário: 13:00 (Horário de Brasília)"
Write-Host "Ação: Executar em segundo plano e abrir a página HTML no navegador."
Write-Host ""
