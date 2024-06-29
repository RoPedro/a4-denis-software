@echo off

SET VEN_DIR=venv

IF NOT EXIST requirements.txt (
    echo requirements.txt não encontrado.
    EXIT /B 1
)

IF NOT EXIST %VEN_DIR% (
    python -m venv %VEN_DIR%
    echo Virtual environment criado.
) ELSE (
    echo Virtual environment encontrado.
)

:: Ativa o virtual environment
echo Acessando venv...
CALL %VEN_DIR%\Scripts\activate

:: Atualiza o pip (opcional)
echo Deseja atualizar o pip? (s/n)
SET /P ANSWER=
IF /I "%ANSWER%"=="s" (
    python -m pip install --upgrade pip
    IF %ERRORLEVEL% NEQ 0 (
        echo Erro ao atualizar o pip.
        EXIT /B 1
    )
)

:: Instala as dependências
IF EXIST requirements.txt (
    python -m pip install -r requirements.txt
    IF %ERRORLEVEL% NEQ 0 (
        echo Erro ao instalar as dependências.
        EXIT /B 1
    )
)

:: Desativa o virtual environment (opcional)
echo MANTENHA O VENV ATIVADO CASO DESEJE TESTAR O CÓDIGO
echo Deseja manter o venv ativado? (s/n)
SET /P ANSWER=
IF /I "%ANSWER%"=="n" (
    CALL deactivate
)
