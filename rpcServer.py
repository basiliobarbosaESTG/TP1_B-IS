from xmlrpc.server import SimpleXMLRPCServer
from psycopg2 import Error
import datetime,json,psycopg2
from Database import querys
from Converters.xml_related.converterXML import converterXML
from Converters.xml_related.validatorXML import validateXML

#Conecção a base de dados
#abrimos o ficheiro de configuração da base de dados
f = open('config.json')
#carregamos o ficheiro de configuracao para obter os dados da BD
data = json.load(f).get('dbconfig')
connection = psycopg2.connect(
    host=data.get('host'),
    port=data.get('port'),
    user=data.get('user'),
    password=data.get('password'),  
    database=data.get('database')) 

cursor = connection.cursor()

# print("PostgreSQL server information")
# print(connection.get_dsn_parameters(), "\n")

cursor.execute("SELECT version();") #Verifcar coneção
record = cursor.fetchone()
print("Está conectado a - ", record, "\n")

def convert(athlete_events_file,name_file): #Chama a classe que faz a conversao do ficheiro de CSV para XML
    c = converterXML(athlete_events_file,name_file)
    result = c.convert()
    print(result)

def validate(xml, xsd): #Chama a classe que faz a validação do XML com o XSD
    return validateXML(xml, xsd)

def get_date(): #Retorna a data atual
    return datetime.datetime.now()

def insert_file(name, file): #Insere o ficheiro na BD
    insert_data = (name, file, get_date())
    try:
        cursor.execute(querys.insert_sp, insert_data)
        connection.commit()
        cursor.execute(querys.get_last)
        result = cursor.fetchall()
        print("Ficheiro guardado\n")
        return str(result)
    except (Exception, Error) as error:
        connection.rollback()
        print("Erro ao inserir o novo ficheiro na BD", error)
        return(str(error))
        

#CONSULTAS
#Pedido á BD para executar o seguinte XPATH/XQUERY que obtem os dados de um atleta(nome, sexo e idade) a partir do seu nome
#/*/ todo que esta dentro do athlete do atributo name
def getAthleteByName(name, id): #recebe como parametros: o id e o nome
    try:
        cursor.execute("SELECT unnest(CAST(XPATH('/athletes/atlethe[@name=\""+name+"\"]/@name', xml)AS TEXT)::text[]) AS nome, unnest(CAST(xpath('/athletes/atlethe[@name=\""+name+"\"]/sex/text()', xml)AS TEXT)::text[]) AS sexo, unnest(CAST(xpath('/athletes/atlethe[@name=\""+name+"\"]/age/text()', xml)AS TEXT)::text[]) AS idade FROM xmldata where id="+id)
        #cursor.execute("SELECT unnest(xpath('/athletes/atlethe[@name=\""+name+"\"]/sex/text()', xml)) AS sexo FROM xmldata where id="+id)
        connection.commit()
        result = cursor.fetchall()
        print(len(result))
        #print(type(result[0]))
        print(type(result)) 
        #Type serve para ver o tipo de dado da variavel
        return result
    except (Exception, Error) as error:
        connection.rollback()
        print("Erro de execução: ", error)
        return(str(error))

#Consulta que conta quantas medalhas existem de cada tipo
def getGroupByMedals(id):
    try:
        cursor.execute("SELECT unnest(cast(xpath('/athletes/atlethe/competition/statsBySport/medal/text()', xml)as TEXT)::text[]) as medalhas, count(*) as contagem FROM xmldata where id="+id+" group by medalhas") 
        connection.commit()
        result = cursor.fetchall()
        print(len(result))
        print(type(result))
        return result
    except (Exception, Error) as error:
        connection.rollback()
        print("Erro de execução: ", error)
        return(str(error))

#Consulta que conta quantos tipos de desportos existem
def getGroupBySport(id):
    try:
        cursor.execute("SELECT unnest(cast(xpath('/athletes/atlethe/competition/statsBySport/sport/text()', xml)as TEXT)::text[]) as desporto, count(*) as contagem FROM xmldata where id="+id+" group by desporto") 
        connection.commit()
        result = cursor.fetchall()
        print(len(result))
        print(type(result))
        return result
    except (Exception, Error) as error:
        connection.rollback()
        print("Erro de execução: ", error)
        return(str(error))

#Consulta que conta quantos atletas existem com aquele tipo de sexo(NESTE CASO CONTA QUANTOS ATLETAS EXISTEM DO SEXO MASCULINO E FEMININO)
def getGroupBySex(id):
    try:
        cursor.execute("SELECT unnest(cast(xpath('/athletes/atlethe/sex/text()', xml)as TEXT)::text[]) as sex, count(*) as contagem FROM xmldata where id="+id+" group by sex order by contagem asc") 
        connection.commit()
        result = cursor.fetchall()
        print(len(result))
        print(type(result))
        return result
    except (Exception, Error) as error:
        connection.rollback()
        print("Erro de execução: ", error)
        return(str(error))

#Consulta que apresenta o tipo de desporto praticado através do nome de um determinado atleta
def getSportByName(name, id):
    try:
        cursor.execute("SELECT unnest(cast(xpath('/athletes/atlethe[@name=\""+name+"\"]/competition/statsBySport/sport/text()', xml)as TEXT)::text[]) as desporto FROM xmldata where id="+id) 
        connection.commit()
        result = cursor.fetchall()
        print(len(result))
        print(type(result))
        return result
    except (Exception, Error) as error:
        connection.rollback()
        print("Erro de execução: ", error)
        return(str(error))

#Consulta que apresenta o tipo de evento desportivo praticado através do nome de um determinado atleta
def getEventByName(name, id):
    try:
        cursor.execute("SELECT unnest(cast(xpath('/athletes/atlethe[@name=\""+name+"\"]/competition/statsBySport/event/text()', xml)as TEXT)::text[]) as evento FROM xmldata where id="+id) 
        connection.commit()
        result = cursor.fetchall()
        print(len(result))
        print(type(result))
        return result
    except (Exception, Error) as error:
        connection.rollback()
        print("Erro de execução: ", error)
        return(str(error))

#Apagar ficheiro da BD
def soft_delete_file(id): 
    try:
        cursor.execute(querys.soft_delete_sp, [id])
        connection.commit()
        cursor.execute(querys.get_row, [id])
        result = cursor.fetchall()
        print(result)
        print("Ficheiro eliminado da BD\n Outout: " + str(result))
        return str(result)
    except (Exception, Error) as error:
        connection.rollback()
        print("Erro ao eliminar o ficheiro", error)
        return(str(error))

server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
print("Á escuta na porta 8000...")

#registo das funcoes
server.register_function(convert, "convert")
server.register_function(validate, "validate")
server.register_function(insert_file, "insert_file")
server.register_function(getAthleteByName, "getAthleteByName")
server.register_function(getGroupByMedals, "getGroupByMedals")
server.register_function(getGroupBySport, "getGroupBySport")
server.register_function(getGroupBySex, "getGroupBySex")
server.register_function(getSportByName, "getSportByName")
server.register_function(getEventByName, "getEventByName")
server.register_function(soft_delete_file, "soft_delete_file")

server.serve_forever()