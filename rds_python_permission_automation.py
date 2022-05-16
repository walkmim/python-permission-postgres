
#Reference 
#https://www.devmedia.com.br/como-criar-uma-conexao-em-postgresql-com-python/34079

#python3 -m pip install psycopg2

import argparse
import psycopg2


def Connect_to_Postgres(host,database,port,pg_user_name,pg_password):
    connection = psycopg2.connect(host=host, database=database, port=port, user=pg_user_name, password=pg_password)
    cursor = connection.cursor()
    cursor.execute("SELECT '>>>>>>>>>> Connected successfully on database '".format(database))
    row = cursor.fetchone()
    returnn = str(row[0])
    
    print("\n{} '{}' <<<<<<<<<<<".format(returnn,database))
    return connection

    
def CreatePostgresRole (connection,role_name,role_password):
    cursor = connection.cursor()
    
    scriptRoleValidation = "SELECT usename FROM pg_catalog.pg_user WHERE usename = '{}'".format(role_name)
    cursor.execute(scriptRoleValidation)
    row = str(cursor.fetchone()[0])
    
    if (len(row)>2):
        print("\nRole '{}' already exists!".format(role_name))  
    else:
        scriptRoleCreate = "".join(( 'CREATE ROLE "{}" \n'.format(role_name),
                        'NOSUPERUSER \n',
                        'NOCREATEDB \n',
                        'NOCREATEROLE \n',
                        'NOINHERIT \n',
                        'LOGIN \n',
                        'NOREPLICATION \n',
                        'NOBYPASSRLS \n',
                        "PASSWORD '{}';".format(role_name,role_password)))
        cursor.execute(scriptRoleCreate)
        connection.commit()
        print("\nRole '{}' created successfully!".format(role_name))    
    cursor.close()

def GrantPermissionTrustedDB (connection,role_name):
    cursor = connection.cursor()
    script = "".join(( 'GRANT CONNECT ON DATABASE "Trusted"             TO "{}";\n'.format(role_name),
                       'GRANT USAGE ON SCHEMA "Base"                    TO "{}";\n'.format(role_name),
                       'GRANT USAGE ON SCHEMA "Communal"                TO "{}";\n'.format(role_name),
                       'GRANT SELECT ON ALL TABLES IN SCHEMA "Base"     TO "{}";\n'.format(role_name),
                       'GRANT SELECT ON ALL TABLES IN SCHEMA "Communal" TO "{}";'.format(role_name)))
    #print('\n{}'.format(script))
    cursor.execute(script)
    connection.commit()
    cursor.close()
    print("\nGrant permissions on 'Trusted' database to '{}' executed successfully!".format(role_name))

def GrantPermissionConsumerDB (connection,role_name):
    cursor = connection.cursor()
    script = "".join(( 'GRANT CONNECT ON DATABASE "Consumer"            TO "{}";\n'.format(role_name),
                       'GRANT USAGE ON SCHEMA "Communal"                TO "{}";\n'.format(role_name),
                       'GRANT SELECT ON ALL TABLES IN SCHEMA "Communal" TO "{}";'.format(role_name)))
    #print('\n{}'.format(script))
    cursor.execute(script)
    connection.commit()
    cursor.close()
    print("\nGrant permissions on 'Consumer database' to '{}' executed successfully!".format(role_name))
    
def GrantPermissionSandBoxDB (connection,role_name):
    cursor = connection.cursor()
    role_name_split = role_name.split(".")
    nominal_schema_name = "".join((role_name_split[0].capitalize(),role_name_split[1].capitalize()))
        
    scriptCreateNominalSchema = """
        CREATE OR REPLACE FUNCTION TMP_PROC_CREATE_NOMINAL_SCHEMA (sch_name text, create_stmt text)
        RETURNS text AS
        $_$
        BEGIN
        IF EXISTS (
        SELECT schema_name FROM information_schema.schemata where schema_name = sch_name
        ) THEN
        RETURN 'SCHEMA ' || '''' || sch_name || '''' || ' ALREADY EXISTS';
        ELSE
        EXECUTE create_stmt;
        RETURN 'SCHEMA ' || '''' || sch_name || '''' || ' CREATED';
        END IF;

        END;
        $_$ LANGUAGE plpgsql;
        SELECT TMP_PROC_CREATE_NOMINAL_SCHEMA('Riscos.{0}', 'CREATE SCHEMA "Riscos.{0}"');
        DROP FUNCTION IF EXISTS TMP_PROC_CREATE_NOMINAL_SCHEMA(sch_name text, create_stmt text);""".format(nominal_schema_name)
    #print('\n{}'.format(scriptCreateNominalSchema))
    cursor.execute(scriptCreateNominalSchema)
    connection.commit()
    print("\nSchema '{}' on 'Sandbox' created successfully!".format(nominal_schema_name))

    script = "".join(( 'GRANT CONNECT ON DATABASE "SandBox"                                 TO "{}";\n'.format(role_name),
                       'GRANT USAGE ON SCHEMA "Riscos"                                      TO "{}";\n'.format(role_name),
                       'GRANT USAGE ON SCHEMA "Riscos.{}"                                   TO "{}";\n'.format(nominal_schema_name,role_name),
                       'GRANT ALL PRIVILEGES ON SCHEMA "Riscos"                             TO "{}";\n'.format(role_name),
                       'GRANT ALL PRIVILEGES ON SCHEMA "Riscos.{}"                          TO "{}";\n'.format(nominal_schema_name,role_name),
                       'ALTER DEFAULT PRIVILEGES IN SCHEMA "Riscos" GRANT ALL ON TABLES     TO "{}";\n'.format(role_name),
                       'ALTER DEFAULT PRIVILEGES IN SCHEMA "Riscos.{}" GRANT ALL ON TABLES  TO "{}";'.format(nominal_schema_name,role_name)))
    #print('\n{}'.format(script))
    cursor.execute(script)
    connection.commit()
    cursor.close() 
    print("\nGrant permissions on 'Sandbox' database to '{}' executed successfully!".format(role_name))
    
def PostgresDBAutomationAccess(args):
    print('\n','*_* '*30)
    print("\n'The automation access process started for '{}' role!".format(args.role_name))
    connection = Connect_to_Postgres(args.host,'postgres',args.port,args.pg_user_name,args.pg_password)
    CreatePostgresRole(connection,args.role_name, args.role_password)
    connection.close()
    
    print("\nGrant premissions on 'Trusted' database to '{}' Started!".format(args.role_name))
    connection = Connect_to_Postgres(args.host,'Trusted',args.port,args.pg_user_name,args.pg_password)
    GrantPermissionTrustedDB(connection,args.role_name)
    connection.close()
    
    print("\nGrant premissions on 'Consumer' database to '{}' Started!".format(args.role_name))
    connection = Connect_to_Postgres(args.host,'Consumer',args.port,args.pg_user_name,args.pg_password)
    GrantPermissionConsumerDB(connection,args.role_name)
    connection.close()
    
    print("\nGrant premissions on 'SandBox' database to '{}' Started!".format(args.role_name))
    connection = Connect_to_Postgres(args.host,'SandBox',args.port,args.pg_user_name,args.pg_password)
    GrantPermissionSandBoxDB(connection,args.role_name)
    connection.close()
    print("\n'The automation access process finished up for '{}' role!\n".format(args.role_name))
    print('*_* '*30)
def main():
    parser = argparse.ArgumentParser(
        description='New role and default permissons for new employee')
    parser.add_argument(
        '--host', 
        required=True,
        help='Your Postgres endpoint connection')
    parser.add_argument(
        '--port', 
        required=True,
        help='Your Postgres Port')
    parser.add_argument(
        '--pg_user_name', 
        required=True,
        help='Your Postgres user name')
    parser.add_argument(
        '--pg_password', 
        required=True,
        help='Your Postgres user password')
    parser.add_argument(
        '--role_name', 
        required=True,
        help='The employee user name')
    parser.add_argument(
        '--role_password', 
        required=True,
        help='The employee user password')
    args = parser.parse_args()
    
    PostgresDBAutomationAccess (args)

if __name__ == '__main__':
    main()