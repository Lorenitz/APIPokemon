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
                pokemon_url = pokemon['url']
                
                pokemon_info = get_pokemon_info(pokemon_url)    
                pokemon_type_text = get_pokemon_type(pokemon_info)
                pokemon_species = get_pokemon_species(pokemon_info)
                pokemon_egg = get_pokemon_egg(pokemon_species)
                pokemon_gen = get_pokemon_gen(pokemon_species)
                pokemon_location = get_pokemon_location(pokemon_info)
                pokemon_stats = get_pokemon_stats(pokemon_info)
                     
                #Writing my data on csv    
                file = open('pokelist.csv','a')
                file.write(name + ',' + pokemon_type_text + ',' + str(pokemon_stats['attack']) + ',' + str(pokemon_stats['defense']) + ',' + str(pokemon_stats['speed']) +  ',' + pokemon_location +  ',' +  pokemon_egg +   ',' +  pokemon_gen + '\n')
                file.close()
                
    next = input("Keep loading? [Y/N]").lower()
    if next == 'y':
        get_pokemons(offset=offset+20)

def get_pokemon_info(url):
    response = requests.get(url)          
    return response.json()   

def get_pokemon_type(pokemon_info):   
    typelist = [] 
    for type_node in pokemon_info['types']:
        typelist.append(type_node['type']['name'])
        
    result = ' and '.join(typelist)
    return result

def get_pokemon_species(pokemon_info):
    poke_species_url = pokemon_info['species']['url']
    response = requests.get(poke_species_url)
    species_info = response.json()
    return species_info

def get_pokemon_egg(species_info):
    egg_groups=[]
    for egg in species_info['egg_groups']:
        egg_groups.append(egg['name'])
    
    result = ' and '.join(egg_groups)    
    return result

def get_pokemon_gen(species_info):
    result = species_info['generation']['name']
    return result

def get_pokemon_location(pokemon_info):
    location_url = pokemon_info['location_area_encounters']
    response = requests.get(location_url)
    
    location_info = response.json()
    
    local_list=[]
    for PokeLocation in location_info:
        local_list.append(PokeLocation['location_area']['name'])
    
    result = ' and '.join(local_list)    
    return result

def get_pokemon_stats(pokemon_info):    
    result = {
        "attack": 0,    
        "defense": 0,
        "speed": 0
    }
    
    for node in pokemon_info['stats']:
       
        if node['stat']['name'] == 'attack':
            result['attack'] = node['base_stat']
        if node['stat']['name'] == 'defense':
            result['defense'] = node['base_stat']
        if node['stat']['name'] == 'speed':
            result['speed'] = node['base_stat']
                    
    return result                

if __name__=='__main__':
    #url='http://pokeapi.co/api/v2/pokemon-form/'
    get_pokemons()



        