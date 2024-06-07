import pandas as pd
import os
import re
from datetime import datetime
import traceback
from app.env_config import BLOB_CONTAINER_NAME, URL_SAS_BLOB
from app.blobstorageService import Blob_Storage_Service

blob_service = Blob_Storage_Service(account_url=URL_SAS_BLOB, container_name=BLOB_CONTAINER_NAME)

get_sigla_regex = r'-([A-Z]{2})-'
get_codigo_projeto = r'(^[A-Z]{2}\d{4})-'
versaoProjetoRegex = r'(\d{4}\.(nwd|nwc))'
checklist_regex = r".*DR\d*.*"
paths = {"input_folder": "./input","output_folder": "./output"}
try:  
    input_folder_path = paths['input_folder']
    output_folder_path = paths['output_folder']
    markup_df = pd.DataFrame()
    checklist_df = pd.DataFrame()
    os.makedirs(output_folder_path, exist_ok=True)
    for file in os.listdir(input_folder_path):
      try:
        normalized_df = pd.read_json(os.path.join(input_folder_path, file))
        
        # Descomente ou comente a linha abaixo se necessário pois alguns aruivos JSON nao possuem collection
        normalized_df = pd.json_normalize(normalized_df['collection'].iloc[0]) 
        checklist_columns = normalized_df.filter(regex=checklist_regex).columns.to_list()
        markup_entries_list = []
        checklist_entries_list = []
        nome_do_arquivo = file
        
        codigo_do_projeto_match = re.search(get_codigo_projeto, nome_do_arquivo)
        codigo_do_projeto = codigo_do_projeto_match.group(1) if codigo_do_projeto_match else None

        for index, row in normalized_df.iterrows():
          new_markup_entry = {
            'IdObjeto': row.get('objectid', None),
            'CodigoProjeto': codigo_do_projeto,
            'NomeAtivo': row.get("name", None),
            "MarkupCodigoAplicação": row.get('properties.Element.BLSCodigoAplicacao', None),
            "DescricaoAplicacao": row.get("properties.Element.BLSDescricaoAplicacao", None), 
            "IdMarkup": row.get("properties.Element.BLSIdMarkup", None),
            "CodigoMarkup": row.get("properties.Element.BLSMarkupCodigoPrincipal", None),
            "DescricaoMarkup": row.get("BLSMarkupDescricao", None),
            "NomeItem": row.get("properties.Item.Name", None),
            "TagEquipamento": row.get("properties.Element.BLSTagEquipamento", None),
            'Categoria': row.get('properties.Element.Category', None),
            "SubcategoriaElemento": row.get("properties.Revit Type.BLSSubcategoria", None),
            'arquivoFonte': row.get('properties.Item.Source File', None),
            'caminho': row.get('properties.Document.PathName', None)
          }
          markup_entries_list.append(new_markup_entry)

        for index, row in normalized_df.iterrows():
          for checklist_item in checklist_columns:
            new_checklist_entry = {
              'IdObjeto': row.get('objectid', None),
              'ItemChecklist': checklist_item,
              'Concluído': row.get(checklist_item, None),
              'arquivoFonte': row.get('properties.Item.Source File', None)
            }
            checklist_entries_list.append(new_checklist_entry)

        if markup_entries_list:
          markup_df = pd.DataFrame(markup_entries_list)
          markup_filename = os.path.join(output_folder_path, f'{nome_do_arquivo[:-5]}_markups.xlsx')
          markup_df.to_excel(markup_filename, index=False)
          blob_service.upload_to_blob(markup_filename)  # Upload the markup file

        if checklist_entries_list:
          checklist_df = pd.DataFrame(checklist_entries_list)
          checklist_filename = os.path.join(output_folder_path, f'{nome_do_arquivo[:-5]}_checklist.xlsx')
          checklist_df.to_excel(checklist_filename, index=False)
          blob_service.upload_to_blob(checklist_filename)  # Upload the checklist file

      except Exception as e:
          print(f'Erro ao processar o arquivo {file}: {e}')
          continue

except Exception as error:
    print(error)
    os.makedirs('./errorLogs', exist_ok=True)
    with open('./errorLogs/inputProcessorErrorLog.txt', 'a') as file:
        error_message = f"{datetime.now()}: {traceback.format_exc()}"
        file.write(error_message + "\n")

