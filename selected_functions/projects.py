
from app.api.services.services import services
from old.fetch_data import fetch_functions


def projects(hub_id, project_list_of_names, projects_df_normalized):

  
    ###

    selected_name = st.selectbox("Project Name", project_list_of_names)
    selected_project = projects_df_normalized[projects_df_normalized['attributes_name'] == selected_name].iloc[0]

    
    
    ###
    
    specific_project = fetch_functions['fetch_and_normalize_specifyc_projects'](hub_id, selected_project['id'], selected_name)
    
    

   
    ###
    
    
