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
            file.write('Pokemon'  + ',' + 'Type' + ',' + 'Attack' + ',' + 'Defense' + ',' + 'Speed'  + ',' + 'Location' + ',' + 'PokemonEgg' +  ',' + 'PokemonGen' + '\n')
            file.close()
       
       
        if results:
            for pokemon in results:
                name = pokemon['name']
                PokemonUrl = pokemon['url']
                
                PokeResponse = requests.get(PokemonUrl, params=args)
               
                ReturnNode = PokeResponse.json()
               
                
               
               #Pokemon Types
                typelist = [] 
                for PokemonType in ReturnNode['types']:
                    typelist.append(PokemonType['type']['name'])
                    
                PokemonTypeText = ' and '.join(typelist)
                
                #Pokemon Eggs
                PokeSpeciesUrl = ReturnNode['species']['url']
                PokeSpecies = requests.get(PokeSpeciesUrl, params=args)
                ReturnPokeSpecies = PokeSpecies.json()
                
                Arr_eggGroups=[]
                for Egggroup in ReturnPokeSpecies['egg_groups']:
                    Arr_eggGroups.append(Egggroup['name'])
                
                PokemonEgg = ' and '.join(Arr_eggGroups)    
                
                
                
                #PokemonGeneration
                
                PokeGen = ReturnPokeSpecies['generation']['name']
                            
                
                
                #Pokemon Stats
                attack=0
                defense=0
                speed=0
                for node in ReturnNode['stats']:
                    
                    if node['stat']['name'] == 'attack':
                        attack = node['base_stat']
                    if node['stat']['name'] == 'defense':
                        defense = node['base_stat']
                    if node['stat']['name'] == 'speed':
                        speed = node['base_stat']
                    
                #Pokemon Location    
                LocationUrl = ReturnNode['location_area_encounters']
                LocationResponse = requests.get(LocationUrl, params = args)
                
                LocationNode = LocationResponse.json()
                
                LocalList=[]
                for PokeLocation in LocationNode:
                    LocalList.append(PokeLocation['location_area']['name'])
                
                PokemonLocation = ' and '.join(LocalList)    
                
                
                
                #Writing my data on csv    
                file = open('pokelist.csv','a')
                file.write(name + ',' + PokemonTypeText + ',' + str(attack) + ',' + str(defense) + ',' + str(speed) +  ',' + str(PokemonLocation) +  ',' +  PokemonEgg +   ',' +  PokeGen + '\n')
                file.close()
                
    next = input("Keep loading? [Y/N]").lower()
    if next == 'y':
        get_pokemons(offset=offset+20)
       

if __name__=='__main__':
    #url='http://pokeapi.co/api/v2/pokemon-form/'
    get_pokemons()



        