import requests
import json 


def get_pokemons(url='http://pokeapi.co/api/v2/pokemon/', offset=0):
    args = {'offset': offset} if offset else {}
    
    response = requests.get(url, params=args)

    if response.status_code == 200:
        payload = response.json()
        results = payload['results']
       
       
        if offset == 0:
            file = open('pokelist.csv','w')
            file.write('Pokemon'  + ',' + 'Type' + ',' + 'Attack' + ',' + 'Defense' + '\n')
            file.close()
       
       
        if results:
            for pokemon in results:
                name = pokemon['name']
                PokemonUrl = pokemon['url']
                
                PokeResponse = requests.get(PokemonUrl, params=args)
               
                ReturnNode = PokeResponse.json()
               
               #Empty string to save my returned values from loop.
                typelist = [] 
                for PokemonType in ReturnNode['types']:
                    typelist.append(PokemonType['type']['name'])
                    
                PokemonTypeText = ' and '.join(typelist)
                
                
                attack=0
                defense=0
                for node in ReturnNode['stats']:
                    
                    if node['stat']['name'] == 'attack':
                        attack = node['base_stat']
                    if node['stat']['name'] == 'defense':
                        defense = node['base_stat']
                    
                    
                    
                file = open('pokelist.csv','a')
                file.write(name + ',' + PokemonTypeText + ',' + str(attack) + ',' + str(defense) +  '\n')
                file.close()
                
    next = input("Keep loading? [Y/N]").lower()
    if next == 'y':
        get_pokemons(offset=offset+20)
       

if __name__=='__main__':
    #url='http://pokeapi.co/api/v2/pokemon-form/'
    get_pokemons()



        