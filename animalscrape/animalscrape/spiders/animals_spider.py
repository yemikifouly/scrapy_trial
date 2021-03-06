import scrapy
import json

class AnimalsSpider(scrapy.Spider):

    name = 'animals'
    
    start_urls = [
        'https://lib2.colostate.edu/wildlife/atoz.php?sortby=Common_Names&letter=ALL'
    ]
    
    def parse(self, response):
    
        animals = dict()
        animals['name'] = 'sorted animal & species'
        animals['letters'] = {}
        
        # Iterate over all the rows of the table of animals
        for animal in response.css('div.tab table.names tr'):
        
            # Get the names and the species (the first link is the name, the second the species)
            common_name, genus_species = animal.css('a::text')[0].get(), animal.css('a::text')[1].get()
            
            # ------- The scraping happens above. Everything below is getting the data into a dict ------
            
            letter = common_name[0]
            # Initialize the list of animals and the total if we are dealing with a new letter
            if letter not in animals['letters']:
                animals['letters'][letter] = {'total': 0, 'animals':[]}
            
            # Add animal name and species to the list of animals whose name starts with the same letter
            animals['letters'][letter]['total'] += 1
            animals['letters'][letter]['animals'].append({'name(s)': common_name, 'species': genus_species})
            
        with open('result.json', 'w') as f:
            json.dump(animals, f)
