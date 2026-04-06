@echo off
:: Define o diretório inicial como a pasta onde o .bat está
cd /d "%~dp0"

:: Entra na pasta específica (substitua 'nome_da_sua_pasta' pelo nome real)
cd config

title Synapsee EEG Analyzer
echo Iniciando o Servidor EEG na pasta %cd%...

:: Executa o streamlit
python -m streamlit run app.py
pause