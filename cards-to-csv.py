import requests
import csv
import json

class mtg_set_exporter:
    def __init__(self,set) -> None:
        self.set = set

    base_url = 'https://api.scryfall.com/cards/search?q=set%3A'

    def get(self,url=base_url):
        url = f'{url}{self.set}'
        response = requests.get(url)
        if response.status_code != 200:
            print(f'Error -- status code {response.status_code}')
            return {}
        else:
            print('Success -- Staging data...')
        return response.json()
    
    def navigate(self,function="abridged card output",new_json = None):
        ### TOP SECTION MAKES AN API CALL WITH SELF.GET() AUTOMATICALLY... NOT NECESSARILY EFFICIENT
        
        print(f'\n\n====== {function} ======\n\n')

        scryfall_json = None
        function = function.lower()

        if new_json: # default None for fresh call - when next page URL available, this gets added to call
            scryfall_json = new_json
        else:
            scryfall_json = self.get() # call the API, declare JSON as a variable
            self.scryfall_json_log(scryfall_json) # save raw JSON as .txt
        if not isinstance(scryfall_json, dict) and not new_json:
            print(f"Warning: navigate received non-dictionary scryfall_json. Received value: {scryfall_json} ")
            try:
                print(f'New JSON: {new_json}')
            except:
                print("No new JSON")
            if function == "has more":
                return False
            if function == "next page":
                return None
        print(f'Scryfall JSON type: {type(scryfall_json)}') # debugging stuff. this sometimes comes back as just "true" for some reason
        json_keys = list(scryfall_json.keys()) # make an array of the dict keys in the JSON
        print(f'JSON Keys: {json_keys}')
        card_attributes = list(scryfall_json[json_keys[json_keys.index('data')]][1].keys())
        # get column names for card data

        ### POST-API CALL, THIS IS WHERE YOU DECIDE WHAT TO DO WITH THE DATA IN THE JSON

        if function == "full card output": # return all columns
            return scryfall_json["data"]

        elif function == "abridged card output": # return just important columns
            output_obj = [] # holds all cards created with below loop
            desired_attributes = [
                'name','mana_cost','cmc','type_line','oracle_text','power','toughness','colors','color_identity','keywords','set','rarity'
            ]
            for item in scryfall_json["data"]: # iterate through cards in data
                temp_card = {} # temp dictionary to hold card data
                for att in desired_attributes: # run through desired attributes, creating KVs for each
                    try:
                        temp_card[att] = item[att]
                    except:
                        temp_card[att] = "n/a"
                output_obj.append(temp_card)
            return output_obj

        elif function == "card attributes":
            return card_attributes
        
        elif function == "has more":

            return scryfall_json["has_more"]
        
        elif function == "next page":
            return scryfall_json["next_page"]
        
        elif function == "options":
            return json_keys

        elif function == "card count":
            return scryfall_json["total_cards"]
        
        elif function == "debug":
            return f"========={len(json_keys)}========="

        else:
            return 
    
    def export_multiple_pages(self):
        running_card_list = []
        upcoming_page = ""
        safeguard = 0

        while True:
            safeguard += 1 # increment to avoid infinite loop
            if safeguard > 15:
                print(f"Safeguard triggered. Count: {safeguard}")

            # extract data
            if upcoming_page: # if we already have "upcoming page" data: use additional page protocol
                try:
                    new_cards = self.get(upcoming_page)
                    running_card_list += self.navigate('abridged card output',new_cards)
                except:
                    print("Error -- something went wrong with upcoming_page in export_multiple_pages")
            else: # if no "upcoming page" data, probably the first page so barebones protocol
                try:
                    running_card_list += self.navigate("abridged card output")
                except:
                    print("Error -- something went wrong with barebones protcol")

            # extraction done -- check for more data
            print("checking for more...")
            are_there_more = self.navigate("has more",upcoming_page)
            print(f'More pages: {are_there_more}')
            if are_there_more: # if more data, update upcoming_page with URL.
                 upcoming_page = self.navigate("next page",upcoming_page)
                 print(f"Upcoming page: {upcoming_page}")
            else: # if not, end the loop and move on.
                 break
            
        print(f"Complete -- Pages run: {safeguard}")
        return running_card_list

    def gen_csv(self):

        data = self.export_multiple_pages()
        fieldnames = list(data[0].keys())

        with open(f'{self.set}_cards_output.csv',mode='w',newline='',encoding='utf-8-sig') as file:
            writer = csv.DictWriter(file,fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    
    def scryfall_json_log(self,sc_json):
        with open('scryfall_json_log_file.txt', 'w') as convert_file: 
            convert_file.write(json.dumps(sc_json))
        print('scryfall_json_log_file.txt created successfully.')

        
if __name__ == "__main__":
    set_code = "fdn"
    target_set = mtg_set_exporter(set_code)
    #print(set_BLB.navigate("abridged card output"))
    # print(set_BLB.navigate("options"))
    #output = set_BLB.export_multiple_pages()
    #print(output)
    set_csv = target_set.gen_csv()