from selected_functions.fetch_data import fetch_functions

import pandas as pd
def explore_folders(project_id, folder_id):
    """Recursive function to explore folders, collect items, and return all items as a DataFrame.
    Args:
        project_id (str): The project identifier.
        folder_id (str): The starting folder identifier.

    Returns:
        pd.DataFrame: A DataFrame containing all items found recursively within the folders.
    """
    
    items_collected = []
    try:
        content_df = fetch_functions['fetch_and_normalize_folder_content'](project_id, folder_id)
        

        
        if 'type' in content_df.columns:
            folders = content_df[content_df['type'] == 'folders']
            items = content_df[content_df['type'] == 'items']
            
            for sub_folder_id in folders['id'].tolist():
                sub_folder_items = explore_folders(project_id, sub_folder_id)
                items_collected.extend([sub_folder_items])
            
            if not items.empty:
                items_collected.append(items)
        else:
            
            pass

    except Exception as e:
        print(e)
    
    if items_collected:
        return pd.concat(items_collected, ignore_index=True)
    else:
        return pd.DataFrame()










































