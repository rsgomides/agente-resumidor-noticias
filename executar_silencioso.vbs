' Script VBScript para executar o agente em segundo plano sem piscar janela preta do cmd
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = scriptDir
WshShell.Run """" & scriptDir & "\executar_rotina.bat""", 0, False
Set WshShell = Nothing
Set fso = Nothing
