import xmlrpc.client

def conect_rpc():
    conn = xmlrpc.client.ServerProxy("http://localhost:8000/")
    return conn

def convertCSVtoXML():
    athlete_events_file = input("Inserir athlete_events_file: ")
    name_file = input("Inserir nome: ")
    try:
        conn = conect_rpc()
        conn.convert(athlete_events_file, name_file)
        return name_file + ".xml"
    except(Exception) as error:
        print("Erro: ", error)

def validateXML_CSV():
    xml = input("Inserir ficheiro XML: ")
    xsd = input("Inserir ficheiro XSD: ")
    try:
        conn = conect_rpc()
        print(conn.validate(xml, xsd))
    except(Exception) as error:
        print("Erro: ", error)

def insertDoc_in_DB():
    try:
        name = input("Inserir nome do ficheiro: ")
        file = input("Inserir ficheiro XML para BD: ")
        conn = conect_rpc()
        ficheiro = open(file, encoding="UTF8").read()
        result = conn.insert_file(name, ficheiro)
        print("Output: " + str(result))
    except(Exception) as error:
        print("Erro: ", error)

def getAthleteByName():
    try:
        #sex = input("Insert the athelete sex: \n EX: M\n")
        name = input("Inserir nome do atleta: \n EX: A Lamusi\n")
        id = input("Inserir o id da linha da BD: ")
        conn = conect_rpc()
        result = conn.getAthleteByName(name, id) #, id - name, sex
        #print("Athele Info:\n\tName: "+ result[0][1]+ "\n\tSex: " + result[0][2])
        #for r in result:
        print(result[0]) # print("Athele Info:\n\tName: "+ r[0]) ->   [1][0] + "\n\tSex: " + result[2][0] + "\n\tAge: "+ result[3][0]
    except(Exception) as error:
        print("Erro: ", error)

def getGroupByMedals():
    try:
        id = input("Inserir o id da linha da BD: ")
        conn = conect_rpc()
        result = conn.getGroupByMedals(id)
        for r in result:
            print(r)
    except(Exception) as error:
        print("Erro: ", error)

def getGroupBySport():
    try:
        id = input("Inserir o id da linha da BD: ")
        conn = conect_rpc()
        result = conn.getGroupBySport(id)
        for r in result:
            print(r)
    except(Exception) as error:
        print("Erro: ", error)

def getGroupBySex():
    try:
        id = input("Inserir o id da linha da BD: ")
        conn = conect_rpc()
        result = conn.getGroupBySex(id)
        for r in result:
            print(r)
    except(Exception) as error:
        print("Erro: ", error)

def getSportByName():
    try:
        name = input("Inserir nome do atleta: \n EX: A Lamusi\n")
        id = input("Inserir o id da linha da BD: ")
        conn = conect_rpc()
        result = conn.getSportByName(name, id)
        for r in result:
            print(r)
    except(Exception) as error:
        print("Erro: ", error)

def getEventByName():
    try:
        name = input("Inserir nome do atleta: \n EX: A Lamusi\n")
        id = input("Inserir o id da linha da BD: ")
        conn = conect_rpc()
        result = conn.getEventByName(name, id)
        for r in result:
            print(r)
    except(Exception) as error:
        print("Erro: ", error)

def softDelete():
    id = input("Inserir o id da linha da BD: ")
    try:
        conn = conect_rpc()
        result = conn.soft_delete_file(id)
        print("Output: " + str(result))
    except(Exception) as error:
        print("Erro: ", error)

def menu():
    while True:
        print("1 - Converter ficheiro CSV para XML")
        print("2 - Validar XML com Schemma")
        print("3 - Inserir novo ficheiro XML na base de dados")
        print("4 - Obter dados do atleta através do nome")
        print("5 - Obter contagem do tipo de medalhas e agrupar")
        print("6 - Obter contagem dos tipos de desportos e agrupar")
        print("7 - Obter contagem dos tipos de sexo e agrupar")
        print("8 - Obter desporto praticado através do nome do atleta")
        print("9 - Obter evento desportivo praticado através do nome")
        print("10 - Soft-Delete do ficheiro")
        print("0 - Sair")
        escolha = input("Escolha uma opção: ")
        if escolha == "1":
            convertCSVtoXML()
        if escolha == "2":
            validateXML_CSV()
        if escolha == "3":
            insertDoc_in_DB()
        if escolha == "4":
            getAthleteByName()
        if escolha == "5":
            getGroupByMedals()
        if escolha == "6":
            getGroupBySport()
        if escolha == "7":
            getGroupBySex()
        if escolha == "8":
            getSportByName()
        if escolha == "9":
            getEventByName()
        if escolha == "10":
            softDelete()
        if escolha == "0":
            print("Bye")
            quit()

def main():
    menu()

if __name__ == "__main__":
    main()