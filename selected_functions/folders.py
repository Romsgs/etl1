
from old.fetch_data import fetch_functions
from selected_functions.explore_folders import explore_folders

from fetch_data_functions.paths import paths
csv_folder_path = paths['csv_folder_path']

def folders(hub_id, project_list_of_names, projects_df_normalized):
  print("fluxo de obtenção dos Dados:")
  print("essa pagina colhe dados das pastas e mostra. depois te pede para procurar uma pagina especifica. desse ponto, ela vai percorrer toda arvore das pastas que n'ao estejam vazias e criar um arquivo csv com o prefixo items_from. esse aqruqivo, será usado na pagina Items <-")
  
  selected_name = st.selectbox("Project Name", project_list_of_names)
  selected_project = projects_df_normalized[projects_df_normalized['attributes_name'] == selected_name].iloc[0]
  
   ###
  top_folders_df_normalized = fetch_functions['fetch_and_normalize_top_folders'](hub_id, selected_project['id'])
  print("Top Folders of this project:")
  print(top_folders_df_normalized)
  top_folders_df_normalized.to_csv(f'{csv_folder_path}/top_folders_from_project_{selected_project['attributes_name']}.csv')
  ###
  selected_folder_name = st.selectbox("Select Folder", top_folders_df_normalized['attributes_name'])
  selected_folder = top_folders_df_normalized[top_folders_df_normalized['attributes_name'] == selected_folder_name].iloc[0]
  folder_content_df_normalized  = fetch_functions['fetch_and_normalize_folder_content'](selected_project['id'], selected_folder['id'])
  if folder_content_df_normalized is not None and not folder_content_df_normalized.empty:
      
      print('folder content')
      print(folder_content_df_normalized)
      
      folder_content_df_normalized.to_csv(f'{csv_folder_path}/folder_content_{selected_folder_name}.csv')
      
      folders_with_multiple_objects = folder_content_df_normalized[folder_content_df_normalized['attributes_objectCount'] > 1]
      print('pastas com objetos dentro:')
      print(folders_with_multiple_objects)
      
      folder_content_df = explore_folders(selected_project['id'], selected_folder['id'])
      print('dataFrame concatenato com toda hieraquia encontrada:')
      print(folder_content_df)
      print(f"salvando em csv, {csv_folder_path}/hierarchy_{selected_name}_{selected_folder_name}.csv")
      folder_content_df.to_csv(f'{csv_folder_path}/hierarchy_{selected_name}_{selected_folder_name}.csv')
      folder_content_df['attributes_displayName'] = folder_content_df['attributes_displayName'].astype(str)
      only_items_df = folder_content_df[folder_content_df['attributes_displayName'].str.contains(r"\.rvt|\.nwc|\.nwd$", regex=True)]
      only_nwc = only_items_df[only_items_df['attributes_displayName'].str.contains(r"ED-MOD|PR-MOD", regex=True)]
      
      
      print(f"salvando em csv o only_items_df, {csv_folder_path}/items_from_{selected_folder_name}.csv")
      only_items_df.to_csv(f"{csv_folder_path}/items_from_{selected_folder_name}.csv")
      print(f"Salvando em csv o only_nwc -> {csv_folder_path}/nwc_items{selected_folder_name}.csv")
      only_nwc.to_csv(f"{csv_folder_path}/nwc_items{selected_folder_name}.csv")
      print("apenas os Items")
      print(only_items_df)     
      
      
      print("only_items_df")
      print(only_items_df)
      list_of_items_names_df = only_items_df['attributes_displayName'] if not only_items_df.empty else st.warning("no items")
      if not only_items_df.empty:
        selected_item_name = st.selectbox("selecione o nome do arquivo", list_of_items_names_df) 
        selected_item = only_items_df[only_items_df['attributes_displayName'] == selected_item_name].iloc[0]
        print(selected_item)
          
      else:
        st.warning("no items")
  elif folder_content_df_normalized is None:
      st.warning("No folder content data available.")
  else:
      st.warning("Folder content data is empty.")
  