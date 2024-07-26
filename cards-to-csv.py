import requests
import csv

class mtg_set_exporter:
    def __init__(self,set) -> None:
        self.set = set

    base_url = 'https://api.scryfall.com/cards/search?q=set%3A'

    def get(self,url=base_url):
        url = f'{url}{self.set}'
        response = requests.get(url)
        if response.status_code != 200:
            print(f'Error -- status code {response.status_code}')
        else:
            print('Success -- Staging data...')
        return response.json()
    
    def navigate(self,function="abridged card output",new_json = None):
        scryfall_json = None
        if new_json:
            scryfall_json = new_json
        else:
            scryfall_json = self.get()

        json_keys = list(scryfall_json.keys())
        card_attributes = list(scryfall_json[json_keys[json_keys.index('data')]][1].keys())

        if function == "full card output":
            return scryfall_json["data"]

        elif function == "abridged card output":
            output_obj = []
            desired_attributes = [
                'name','mana_cost','cmc','type_line','oracle_text','power','toughness','colors','color_identity','keywords','set','rarity'
            ]
            for item in scryfall_json["data"]:
                temp_card = {}
                for att in desired_attributes:
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
        more_pages = False
        upcoming_page = ""
        safeguard = 0
        running_card_list += self.navigate("abridged card output")
        if self.navigate("has more"):
            more_pages = True
            upcoming_page = self.navigate("next page")
        while more_pages:
            print(f'Upcoming page: {upcoming_page}')
            if not upcoming_page:
                break
            safeguard += 1
            if safeguard > 15:
                print(safeguard) #########
                more_pages = False
            new_cards = self.get(upcoming_page)
            print(f'Has more: {self.navigate("has more",new_cards)}')
            print(list(new_cards.keys())) ########
            #print(len(new_cards)) #########
            #print(self.navigate("options"),new_cards) ########
            if new_cards:
                try:
                    running_card_list += self.navigate("abridged card output",new_cards)
                except:
                    print("Houston, we have an oopsie")
            upcoming_page = self.navigate("has more",new_cards)
            print(upcoming_page)
            if self.navigate("has more",upcoming_page) != True:
                more_pages = False
        print(f"Complete -- Pages run: {safeguard+1}")
        return running_card_list

    def gen_csv(self):

        data = self.export_multiple_pages()
        fieldnames = list(data[0].keys())

        with open(f'{self.set}_cards_output.csv',mode='w',newline='') as file:
            writer = csv.DictWriter(file,fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        
if __name__ == "__main__":
    set_code = "mh3"
    target_set = mtg_set_exporter(set_code)
    #print(set_BLB.navigate("abridged card output"))
    # print(set_BLB.navigate("options"))
    #output = set_BLB.export_multiple_pages()
    #print(output)
    set_csv = target_set.gen_csv()