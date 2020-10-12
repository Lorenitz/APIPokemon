import requests
import json 
import urllib.request
import os.path
import os

def get_pokemons(url='http://pokeapi.co/api/v2/pokemon/', offset=0):
    args = {'offset': offset} if offset else {}
    
    response = requests.get(url, params=args)

    if response.status_code == 200:
        payload = response.json()
        results = payload['results']
       
        if offset == 0:
            init_csv_headers()
         
        if results:
            for pokemon in results:                  
                pokemon_info = get_pokemon_info(pokemon['url'])    
                pokemon_species = get_pokemon_species(pokemon_info)
                    
                pokemon_row = {
                    "name": pokemon['name'],
                    "type_text": get_pokemon_type(pokemon_info),
                    "stats": get_pokemon_stats(pokemon_info),
                    "location": get_pokemon_location(pokemon_info),
                    "egg": get_pokemon_egg(pokemon_species),
                    "gen": get_pokemon_gen(pokemon_species),
                    "url": get_pokemon_sprites(pokemon_info), 
                    "urlFront": get_pokemon_sprites_Front(pokemon_info)  
                }

                write_csv_row(pokemon_row)
                
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


def get_pokemon_sprites(pokemon_info):
    
    
    save_path = 'C:/Users/loren/Documents/GitHub Projects/APIPokemon/PokemonBack'
    
    poke_img_url = pokemon_info['sprites']['back_default']
    filename ="back - " +  poke_img_url.split("/")[-1]
    
    path_fileName = os.path.join(save_path, filename+".png")
    
    
    r = requests.get(poke_img_url, timeout=0.5)
    
    with open(path_fileName, 'wb') as back:
        back.write(r.content)
    
    return poke_img_url

def get_pokemon_sprites_Front(pokemon_info):
    
    
    save_path = 'C:/Users/loren/Documents/GitHub Projects/APIPokemon/PokemonFront'
    
    poke_img_url_front = pokemon_info['sprites']['front_default']
    filename ="front - " +  poke_img_url_front.split("/")[-1]
    
    path_fileName = os.path.join(save_path, filename+".png")
    
    
    r = requests.get(poke_img_url_front, timeout=0.5)
    
    with open(path_fileName, 'wb') as front:
        front.write(r.content)
    
    return poke_img_url_front

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

def init_csv_headers():
    file = open('pokelist.csv','w')
    file.write(
        'Pokemon'  + ',' +
        'Type' + ',' +
        'Attack' + ',' +
        'Defense' + ',' +
        'Speed'  + ',' +
        'Location' + ',' +
        'PokemonEgg' +  ',' +
        'PokemonGen' + ',' + 
        'PokemonUrl'  + ',' + 
        'PokemonUrlFront' + '\n'
    )
    file.close()     
    
def write_csv_row(row):
    file = open('pokelist.csv','a')
    file.write(
        row['name'] + ',' +
        row['type_text'] + ',' +
        str(row['stats']['attack']) + ',' + 
        str(row['stats']['defense']) + ',' + 
        str(row['stats']['speed']) +  ',' + 
        row['location'] +  ',' +  
        row['egg']  +   ',' +
        row['gen'] + ',' +   
        row['url']  + ',' + 
        row['urlFront'] + '\n'
    )
    file.close()          

if __name__=='__main__':
    
    start = input("Pokemon Data from csv or xlsx [CSV/XLSX]").lower()
    if start == 'csv':
       get_pokemons()
    else:
        pass



        
