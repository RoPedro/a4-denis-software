## Em ambientes Windows, rodar configure.bat, em ambientes GNU/Linux, rodar configure.sh para instalar as dependências e configurar o venv

# Imagem da database
https://hub.docker.com/r/pedrolrmoreira/bibliotecadb

# Em configurações adicionais do docker, usar a porta 5432:5432

# Informações a respeito do DB, se necessário
user=postgres  
password=admin123  
database=biblioteca  
port=5432  

## TO RUN:
`flask run --host 0.0.0.0 --port 5000`
`flask --debug run --host 0.0.0.0 --port 5000`