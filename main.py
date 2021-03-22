import requests as rq
import json as js

id_produto = 1
id_cat_produto = 2


def json_bairros():
    json_bairros = ""

    try: 
        arquivo = open("./lat_long.json", "r", encoding="UTF-8")
        txt_arquivo = arquivo.read()
        json_bairros = js.loads(txt_arquivo)
    except:
        arquivo.close()
        print("erro")
    else:
        arquivo.close()
        print("finalizou")

    return json_bairros["bairros"]


def json_alimentos():
    json_alimentos = ""

    try: 
        arquivo = open("./alimentos.json", "r", encoding="UTF-8")
        txt_arquivo = arquivo.read()
        json_alimentos = js.loads(txt_arquivo)
    except:
        arquivo.close()
        print("erro")
    else:
        arquivo.close()
        print("finalizou")

    return json_alimentos


def get_lat_lng(bairro):
    lat = bairro["info"]["lat"]
    lng = bairro["info"]["lng"]
    return lat, lng


def retornar_produtos_json(bairro, prod, limit):
    limit = str(limit)
    cat = str(prod)
    lat, lng = get_lat_lng(bairro)

    headers = {'Authorization': 'YXBpX3Bpbm5nb19zZWNyZXRfa2V5X2dyZ2k5LmNvbQ=='}
    url = "http://api.note.ehorus.com.br/v2/user/246956/markets/products?limit=" + limit + "&order_by=relevancia_desc&offset=0&lat=" + str(lat) + "&lng=" + str(lng) + "&cat=" + cat + "&distance=10"
    
    resp = rq.get(url, headers = headers)
    resp_txt = resp.text
    json = js.loads(resp_txt)

    return json


def criar_produtos(produtos, bairro, idcorrente):
    id_bairro = bairro["id"]

    for produto in produtos["result"]["products"]:
        name = produto['name']
        tipo = produto['tipo']
        price = produto['price']
        image_url = produto['image_url']
        qtd = produto['measure']['quantity']
        unt = produto['measure']['unit']
        cat = tipo + " " + str(qtd) + " " + unt
        json = '{ "id" : ' + str(idcorrente) + ', "id_bairro" : ' + str(id_bairro) + ', "nome" : "' + name + '", "tipo" : "' + tipo + '", "preco" : ' + str(price) + ', "url_img" : "' + image_url + '", "categoria" : "' + cat + '"}, \n'
        idcorrente += 1
        adicionar_prod_arquivo(json)

    return idcorrente


def adicionar_prod_arquivo(produto):
    try: 
        arquivo = open('./alimento_bairros.json', 'a', encoding="UTF-8")
        arquivo.write(produto)
    except:
        arquivo.close()
    else:
        arquivo.close()

def criador(bairros, alimentos):
    id_corrente_produto = 1
    cont = 1

    for alimento in alimentos:
        id_alimento = alimento["nielsen_id"]
        nome_alimento = alimento["descricao"]

        for bairro in bairros:
            print("Criando alimento " + nome_alimento + " para o bairro " + bairro["name"])
            produtos = retornar_produtos_json(bairro, id_alimento, 50)
            id_corrente_produto = criar_produtos(produtos, bairro, id_corrente_produto)
            print("Foram cadastrados " + str(id_corrente_produto-1) + " " + nome_alimento)
            cont += 1

        print(nome_alimento + " criado com sucesso !!")

    print("Finalizado a criacao")


bairros = json_bairros()
alimentos = json_alimentos()
print("Total de bairros : " + str(len(bairros)))
print("Total de alimentos : " + str(len(alimentos)))
criador(bairros, alimentos)
