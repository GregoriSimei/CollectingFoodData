import json
import requests
from geopy.geocoders import Nominatim

def ajustar_bairro_p_json(cod, bairro, latitude, longitude):
    json_bairro = '{"id" : ' + str(cod) + ' , "name" : "' + bairro + '", "info" : { "lat" : ' + str(latitude) + ', "lng" : ' + str(longitude) + ' } }'
    print(json_bairro)
    return json_bairro

def ajustar_bairros_p_json(bairros):
    json_final = '{ "bairros" : ['
    total = len(bairros)-1
    i = 0
    
    for bairro in bairros:

        if i != total:
            json_final += bairro + ", "
        else: 
            json_final += bairro
        i = i+1
    json_final += "]}"

    return json_final

def criar_arquivo(bairros):
    try: 
        arquivo = open('./lat_long.json', 'w', encoding="UTF-8")
        arquivo.write(bairros)
    except:
        arquivo.close()
    else:
        arquivo.close()
    


geolocator = Nominatim(user_agent="geopy.geocoders.options.default_user_agent")

try: 
    arquivo = open("./bairro.json", "r", encoding='utf8')
    arquivo_texto = arquivo.read()
    bairros = json.loads(arquivo_texto)
    cidade_estado = " , Curitiba - PR"

    json_bairros = []

    total_bairros = len(bairros["bairros"])
    num_atual = 1

    for bairro in bairros["bairros"]:
        porcent = num_atual / total_bairros * 100
        #print(str(int(porcent)) + "%" )
        pesquisa = bairro + cidade_estado
        location = geolocator.geocode(pesquisa)
        lat = location.latitude
        lng = location.longitude
        json_bairro = ajustar_bairro_p_json(num_atual, pesquisa,lat,lng)
        json_bairros.append(json_bairro)
        num_atual += 1

    json_final = ajustar_bairros_p_json(json_bairros)
    criar_arquivo(json_final)

    print("leu")
except:
    arquivo.close()
    print("nao leu")
else:
    arquivo.close()
    print("fim")

