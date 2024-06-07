
from app.api.services.services import services
from old.fetch_data import fetch_functions
import os
import pandas as pd
import json
from urllib.parse import urlparse
from fetch_data_functions.paths import paths
csv_folder_path = paths['csv_folder_path']

def get_files():
  
  list_of_files = []
  list_of_dfs = []
  
  for file in os.listdir(path=csv_folder_path):
    if file.startswith('item_metadata_version_'):
      list_of_files.append(file)
      df = pd.read_csv(f'{csv_folder_path}/{file}')
      list_of_dfs.append(df)
  if len(list_of_dfs) < 1 or list_of_dfs == []:
      return pd.DataFrame()
  if len(list_of_dfs) == 1:      
      return pd.DataFrame(list_of_dfs[0], index=False)
  else:
    return pd.concat(list_of_dfs)


def safe_parse_json(x):
    try:
        json_data = json.loads(x.replace("'", "\""))
        return json_data['data']['id'] if 'data' in json_data else None
    except json.JSONDecodeError as e:
        
        return pd.DataFrame()
    except KeyError as e:
        
        return pd.DataFrame()



def versions(project_list_of_names, projects_df_normalized):
  selected_name = st.selectbox("Project Name", project_list_of_names)
  selected_project = projects_df_normalized[projects_df_normalized['attributes_name'] == selected_name].iloc[0]
  print("selected Project: ", selected_project['attributes_name'])
  items_df = get_files()
  print("items_df")
  print(items_df)
  
  if not items_df.empty:
    
    selected_item_name = st.selectbox("Choose the item", items_df['attributes_name'])
    print("Selected Item", selected_item_name)
    
    derivatives_data = items_df[items_df['attributes_name'] == selected_item_name]
    print('Derivatives Data')
    print(derivatives_data)

    if 'relationships_derivatives' in derivatives_data.columns:
      
      derivatives_data['guid'] = derivatives_data['relationships_derivatives'].apply(safe_parse_json)
      items_version_derivative_id = derivatives_data['guid'].dropna().unique().tolist()[0]
      

      if items_version_derivative_id:
        print('current file derivative id')
        print(items_version_derivative_id)        
        
        derivative_metadata_df = fetch_functions['fetch_and_normalize_derivative_metadata'](items_version_derivative_id)
        
        
        item_guid = derivative_metadata_df.loc[0,'metadata_guid']
        print("derivative_metadata_df")
        print(derivative_metadata_df)
        print("item_guid")
        print(item_guid)
        
        derivative_hierarchy_df = fetch_functions['fetch_and_normalize_derivative_obj_hierarchy'](items_version_derivative_id, item_guid)
        print("derivative hierarchy")
        
        new_derivative_hierarchy=pd.DataFrame(derivative_hierarchy_df)
        print(new_derivative_hierarchy)
        derivativeproperties_df = fetch_functions['fetch_and_normalize_derivative_items_properties'](items_version_derivative_id, item_guid)
        print("derivative properties")
        derivativeproperties_df = pd.DataFrame(derivativeproperties_df)
        derivativeproperties_df.to_json(f"{csv_folder_path}/json_properties_{selected_item_name}.json")
        print(derivativeproperties_df)

      else:
            print("No derivative data available for the selected items.")
    else:
      items_version_derivative_id = derivatives_data['guid']

      if items_version_derivative_id:
        
        print(items_version_derivative_id)
        
        
        
        
        

        
        
        print(items_version_derivative_id)
        
        derivative_metadata_df = fetch_functions['fetch_and_normalize_derivative_metadata'](items_version_derivative_id)
        
        item_guid = items_version_derivative_id[0]
        print(derivative_metadata_df)
        print(item_guid)
        derivative_hierarchy_df = fetch_functions['fetch_and_normalize_derivative_obj_hierarchy'](items_version_derivative_id, item_guid)
        print("derivative hierarchy")
        print(derivative_hierarchy_df)
        derivativeproperties_df = fetch_functions['fetch_and_normalize_derivative_items_properties'](items_version_derivative_id, item_guid)
        print("derivative properties")
        print(derivativeproperties_df)

        print("No 'relationships_derivatives' found in the data.")
  else:
      print('Try another file.')
