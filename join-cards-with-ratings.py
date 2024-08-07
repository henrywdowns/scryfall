import numpy as np
import pandas as pd

card_set = "mh3"
set_draft_ratings_filename = 'mh3-card-ratings-2024-07-25.csv'

def join_cards_and_ratings(card_data=None,ratings_data=None):
    mh3_ratings = pd.read_csv('mh3-card-ratings-2024-07-25.csv')
    mh3_cards = pd.read_csv('%s_cards_output.csv' % card_set)
    merged_df = pd.merge(mh3_ratings,mh3_cards, left_on='Name',right_on='name')
    merged_df.to_csv('merged_%s_file.csv' % card_set,index=False)
    print('Job complete. Merged Ratings and Card Data for %s' % card_set)

join_cards_and_ratings(card_set,set_draft_ratings_filename)