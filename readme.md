Author: Walisson Alkmim</br>
Versão: 1.0</br>
Data: 15/05/2022</br>

<h3><b>Requisitos:</b></h3>
* Ter usário com permissão de: 
    * Criar e gerenciar roles 
    * Criar e gerenciar schemas 
    * Criar e gerenciar procedures
    * Gerenciar permissões no ambiente
    * Acesso leitura nas tabelas de catálago
* Python 3.10
* Pacote para conexão com Postgres: python3 -m pip install psycopg2
* Bash instalado. Caso não utilize Mac OS ou distribuições Linux, Pode instalar Git Bash no seu Windows

<h3><b>Ferramentas utilizadas::</b></h3>
* VS Code 
* PgAdmin 4
* Git Bash
* Ambiente teste python da w3schools (https://www.w3schools.com/)
    * Utilizei para validar scripts individuais sem ter que executar todo contexto

<h3><b>Plataformas::</b></h3>
* AWS Cloud Provider 
* RDS Postgres 14.2 com configurações nínimas


<h3><b>Como Executar::</b></h3>
* Baixe o repositório para diretório local
* Para distribuições Linux e Mac OS Executar via Terminal
* Para Windows temos algumas opções:
    * Para versões a partir do Windows 10, é possível instalar o Subsystem Linux, desta forma habilitará o bash no prompt command
        * https://www.techtudo.com.br/noticias/2016/04/como-instalar-e-usar-o-shell-bash-do-linux-no-windows-10.ghtml
    * Pode ser utilizado o Git Bash - Integra com VS Code
        * https://gitforwindows.org/

* No terminal escolhido, navegue até o diretorio do repositório
* Abaixo mapa da execução do script, substitua os parâmetros entre <> pelos respectivos valores:
    host=<RDS_Write_Endpoint>
    port=<RDS_Port>
    pg_user_name=<RDS_Admin_User>
    pg_password=<RDS_Admin_Password>
    role_name=<Employee_User>
    role_password=<Employee_Password>

    python3 rds_python_permission_automation.py \
    --host ${host} \
    --port ${port} \
    --pg_user_name ${pg_user_name} \
    --pg_password ${pg_password} \
    --role_name ${role_name} \
    --role_password ${role_password}

<h3><b>Exemplo da execução::</b></h3>
    host=rdszm.c3iie8ju3iaa.us-east-1.rds.amazonaws.com
    port=5432
    pg_user_name=postgres
    pg_password=sadfvsda84f7984v8f
    role_name=carlos.henrique
    role_password=barataBela

    python3 rds_python_permission_automation.py \
    --host ${host} \
    --port ${port} \
    --pg_user_name ${pg_user_name} \
    --pg_password ${pg_password} \
    --role_name ${role_name} \
    --role_password ${role_password}

<h3><b>Obrigado!</b></h3>
