#!/bin/bash

VEN_DIR="venv"

if [ ! -f requirements.txt ]; then
    echo "requirements.txt não encontrado."
    exit 1
fi

if [ ! -d $VEN_DIR ]; then
    python3 -m venv $VEN_DIR
    echo "Virtual enviroment criado"
else
    echo "Virtual enviroment encontrado"
fi

# Ativa o virtual enviroment
echo "Acessando venv..."
source $VEN_DIR/bin/activate

# Atualiza o pip
echo "Deseja atualizar o pip? (s/n)"
read ANSWER
if [ "$ANSWER" = "s" ]; then
    pip install --upgrade pip
    if [ $? -ne 0 ]; then
        echo "Erro ao atualizar o pip"
        exit 1
    fi
fi

# Instala as dependências
if [ -f  ]; then
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Erro ao instalar as dependências"
        exit 1
    fi
fi

# Desativa o virtual enviroment
echo "Deseja desativar o venv? (s/n)"
read ANSWER
if [ "$ANSWER" = "s" ]; then
    deactivate
fi

echo "Configuração concluída"