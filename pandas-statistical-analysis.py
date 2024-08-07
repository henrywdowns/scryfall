import pandas as pd
import numpy as np

filename = 'merged_mh3_file_updated.csv'
df = pd.read_csv(filename)

class StatisticalAnalysis:
    def __init__(self,data_frame=None,processed_df=None,filename=None):
        self.df = data_frame
        self.processed_df = processed_df
        self.filename = filename

    def list_rows(self):
        return pd.pivot_table(self.df,values='power',columns='Name',aggfunc='mean')
    
    def list_row_names(self):
        return df.columns.tolist()

    def convert_col_data_types(self):
        safeguard = 0
        col_list = self.df.columns.tolist()
        col_choice = []
        print(f'Present columns: {col_list}.')
        while safeguard < 10:
            safeguard += 1
            user_selection = input('Select a column or \'all\' to confirm each.\n')
            if user_selection == 'quit':
                return
            elif user_selection == 'all':
                col_choice = col_list
                break
            elif user_selection in col_list:
                col_choice.append(user_selection)
                break
            else:
                print(f'Incorrect choice. Try again. Tries remaining: {9-safeguard}')
        safeguard = 0
        print('Valid data choices: "int64", "float64","object"')
        for col in col_choice:
            while safeguard < 3:
                data_type = input(f'Choose a data type for {col}\n')
                if data_type == 'quit':
                    return
                elif data_type == 'int64' or data_type == 'i':
                    if self.df[col].astype(str).str.contains('%').any():
                        self.df[col] = self.df[col].str.replace('%', '').str.strip()
                        self.df[col] = pd.to_numeric(self.df[col], errors='coerce') / 100
                    else:
                        pass
                    self.df[col] = pd.to_numeric(self.df[col],errors='coerce')
                    if pd.api.types.is_numeric_dtype(self.df[col]):
                        self.df[col] = self.df[col].astype('Int64')
                        break
                elif data_type == 'float64' or data_type == 'f':
                    self.df[col] = pd.to_numeric(self.df[col],errors='coerce')
                    self.df[col] = self.df[col].astype('float64')
                    break
                elif data_type == 'object' or data_type == 'o':
                    self.df[col] = self.df[col].astype('object')                
                    break
                else:
                    print(f'Invalid answer. {2-safeguard} attempts left.')
                    safeguard+=1
        print(self.df.dtypes)
        while safeguard < 3:
            confirm_save_changes = input('Save changes to file? (y/n)\n')
            if confirm_save_changes.lower() == 'y':
                self.df.to_csv(f'{filename[:-4]}_updated.csv', index = False)
                break
            elif confirm_save_changes.lower() == 'n':
                break
            else:
                print(f'Bad input. Try y or n. {2-safeguard} attempts left.')
    
    def check_data_types(self):
        return self.df.dtypes
    
    def descriptive_statistics(self):
        # filter numeric columns:
        result_dict = {}
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        result_dict["count"] = self.df[numeric_cols].count()
        result_dict["min"] = self.df[numeric_cols].min()
        result_dict["max"] = self.df[numeric_cols].max()
        result_dict["mean"] = self.df[numeric_cols].mean()
        result_dict["median"] = self.df[numeric_cols].median()
        # result_dict["mode"] = self.df[numeric_cols].mode()
        # result_dict["min"] = self.df[numeric_cols].min()
        # result_dict["min"] = self.df[numeric_cols].min()
        # result_dict["min"] = self.df[numeric_cols].min()
        # result_dict["min"] = self.df[numeric_cols].min()
        return result_dict

    def agg_by_mv_p_t(self):
        # WHERE statement
        filtered_df = df[(df['rarity'] == 'common') | (df['rarity'] == 'uncommon')].copy()
        # hardcode null values
        filtered_df.loc[:,'colors'] = filtered_df['colors'].fillna('Unknown')
        #GROUP BY statement, with aggregation over GIH WR and ALSA
        result = filtered_df.groupby(['colors','cmc','power','toughness']).agg(
            gih_wr_avg=('GIH WR','mean'),
            ALSA_avg=('ALSA','mean')
        ).reset_index()
        return result
    
    def ALSA_analysis(self):
        filtered_df = df[(['rarity'] == 'common') | (df['rarity'] == 'uncommon')].copy()
        filtered_df.loc[:,'colors'] = filtered_df['colors'].fillna('Unknown')
        filtered_df.loc[:,'ALSA'] = filtered_df['ALSA'].round(0)
        result = filtered_df.groupby(['ALSA','power','toughness','cmc','colors','Name']).agg(
            gih_wr_avg=('GIH WR','mean')
        ).reset_index()
        return result

    def convert_df_to_csv(self):
        self.processed_df.to_csv(self.filename,index=False)
        print(f'{self.filename} has been created.')


########## FUNCTION CALLS BELOW ##########

if __name__ == "__main__":
    mh3_class = StatisticalAnalysis(df)
    # mh3_class.convert_col_data_types()
    # print(mh3_class.check_data_types())
    # print(mh3_class.data_frame)
    # print(mh3_class.descriptive_statistics())
    # print(mh3_class.list_row_names())
    aggregated_df = mh3_class.ALSA_analysis()
    print(aggregated_df)
    mh3_agg_class = StatisticalAnalysis(df,aggregated_df,"mh3_agg_output.csv")
    mh3_agg_class.convert_df_to_csv()