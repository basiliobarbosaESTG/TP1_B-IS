import xmlschema

#faz a validaçáo do xml retornando verdadeiro ou falso
def validateXML(xml_path, xsd_path): 
    try:
        my_schema = xmlschema.XMLSchema(xsd_path)
        if my_schema.is_valid(xml_path):
            return "O ficheiro é válido!"
        else:
            return "O ficheiro náo é válido com este xsd"
    except(Exception) as error:
        return "Erro ao validar o ficheiro XML: " + str(error)