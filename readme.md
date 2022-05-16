Author: Walisson Alkmim</br>
Versão: 1.0</br>
Data: 15/05/2022</br>

<h3><b>Requisitos:</b></h3>
 * Ter usário com permissão de: </br>
    * Criar e gerenciar roles </br>
    * Criar e gerenciar schemas </br>
    * Criar e gerenciar procedures</br>
    * Gerenciar permissões no ambiente</br>
    * Acesso leitura nas tabelas de catálago</br>
 * Python 3.10</br>
 * Pacote para conexão com Postgres: python3 -m pip install psycopg2</br>
 * Bash instalado. Caso não utilize Mac OS ou distribuições Linux, Pode instalar Git Bash no seu Windows</br>

<h3><b>Ferramentas utilizadas::</b></h3>
 * VS Code </br>
 * PgAdmin 4</br>
 * Git Bash</br>
 * Ambiente teste python da w3schools (https://www.w3schools.com/)</br>
    * Utilizei para validar scripts individuais sem ter que executar todo contexto</br>

<h3><b>Plataformas::</b></h3>
 * AWS Cloud Provider </br>
 * RDS Postgres 14.2 com configurações nínimas</br>


<h3><b>Como Executar:</b></h3>
 * Baixe o repositório para diretório local</br>
 * Para distribuições Linux e Mac OS Executar via Terminal</br>
 * Para Windows temos algumas opções:</br>
    * Para versões a partir do Windows 10, é possível instalar o Subsystem Linux, desta forma habilitará o bash no prompt command</br>
        * https://www.techtudo.com.br/noticias/2016/04/como-instalar-e-usar-o-shell-bash-do-linux-no-windows-10.ghtml</br>
    * Pode ser utilizado o Git Bash - Integra com VS Code</br>
        * https://gitforwindows.org/</br>

 * No terminal escolhido, navegue até o diretorio do repositório</br>
 * Abaixo mapa da execução do script, substitua os parâmetros entre <> pelos respectivos valores:</br></br>
```eclipse
host=<RDS_Write_Endpoint></br>
port=<RDS_Port></br>
pg_user_name=<RDS_Admin_User></br>
pg_password=<RDS_Admin_Password></br>
role_name=<Employee_User></br>
role_password=<Employee_Password></br>

python3 rds_python_permission_automation.py \
--host ${host} \
--port ${port} \
--pg_user_name ${pg_user_name} \
--pg_password ${pg_password} \
--role_name ${role_name} \
--role_password ${role_password}
```

<h3><b>Exemplo da execução:</b></h3></br>

```eclipse
host=rdszm.c3iie8ju3iaa.us-east-1.rds.amazonaws.com</br>
port=5432</br>
pg_user_name=postgres</br>
pg_password=sadfvsda84f7984v8f</br>
role_name=carlos.henrique</br>
role_password=barataBela</br>

python3 rds_python_permission_automation.py \
--host ${host} \
--port ${port} \
--pg_user_name ${pg_user_name} \
--pg_password ${pg_password} \
--role_name ${role_name} \
--role_password ${role_password}
```

<h3><b>Código para validar permissão concedida no Postgres:</b></h3></br>

```sql
select  
  r.usename as grantor, e.usename as grantee, nspname, privilege_type, is_grantable
from pg_namespace
join lateral (
  SELECT
    *
  from
    aclexplode(nspacl) as x
) a on true
join pg_user e on a.grantee = e.usesysid
join pg_user r on a.grantor = r.usesysid 
where e.usename = 'carlos.henrique';
```

</b><h3><b>Obrigado!</b></h3>
