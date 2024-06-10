from fetch_data_functions.fetch_data import fetch_functions
from selected_functions.explore_folders import explore_folders
import time
from datetime import timedelta

csv_folder_path = "./input"
tempo_inicial = time.time()


def go(hub_id, project_df, project_list_names):
    for current_project_name in project_list_names:
        selected_projects_df = project_df[
            project_df["attributes.name"] == current_project_name
        ]
        list_of_project_id = [id for id in selected_projects_df["id"]]
        #########################################################################################################################################################
        for project_id in list_of_project_id:
            top_folders_df = fetch_functions["fetch_and_normalize_top_folders"](
                hub_id, project_id
            )
            top_folders_df = top_folders_df[
                top_folders_df["attributes.hidden"] == False
            ]
            print("---------------")
            print(top_folders_df.head())
            print(top_folders_df["attributes.name"])
            regex_para_encontrar_a_pasta_do_prjeto = (
                r"(^BL\d{4}|Project\s*Files)|(^\d{4}|Project\s*Files)"
            )
            top_project_folder = top_folders_df[
                top_folders_df["attributes.name"].str.contains(
                    regex_para_encontrar_a_pasta_do_prjeto, na=False, regex=True
                )
            ]
            project_folder_id = top_project_folder["id"].iloc[0]
            if (
                top_project_folder.empty
                or top_folders_df is None
                or top_folders_df.empty
            ):
                continue
            try:

                folder_content_df = fetch_functions[
                    "fetch_and_normalize_folder_content"
                ](project_id, project_folder_id)
            except Exception as e:
                print(f"error on folder contend df: {e}")
            folder_content_regex = r".ENG$"
            folder_ENG = folder_content_df[
                folder_content_df["attributes.name"].str.contains(
                    folder_content_regex, na=False, regex=True
                )
            ]
            if folder_ENG.empty:
                continue
            eng_folder_content = fetch_functions["fetch_and_normalize_folder_content"](
                project_id, folder_ENG["id"].iloc[0]
            )
            for folder_after_eng_id in eng_folder_content["id"]:
                folder_content_files_df = explore_folders(
                    project_id, folder_after_eng_id
                )
                print(folder_content_files_df)
                folder_content_regex = r".*(?:ED|PH).*\.(?:nwc|nwd)$"
                if folder_content_files_df.empty:
                    continue
                only_the_federated_files = folder_content_files_df[
                    folder_content_files_df["attributes.displayName"].str.contains(
                        folder_content_regex, na=False, regex=True
                    )
                ]
                if not only_the_federated_files.empty:
                    list_of_files_id = []
                    for index, row in only_the_federated_files.iterrows():
                        list_of_files_id.append(row["id"])
                        items_metadata = fetch_functions[
                            "fetch_and_normalize_item_metadata"
                        ](project_id, row["id"])
                        if items_metadata is None or items_metadata.empty:
                            continue
                        item_metadata_id = items_metadata["id"].iloc[0]
                        items_metadata_version = fetch_functions[
                            "fetch_and_normalize_item_metadata_version"
                        ](project_id, item_metadata_id)
                        if (
                            items_metadata_version is None
                            or items_metadata_version.empty
                        ):
                            continue
                        items_version_derivative_id = items_metadata_version[
                            "relationships.derivatives.data.id"
                        ].iloc[0]
                        derivative_metadata_df = fetch_functions[
                            "fetch_and_normalize_derivative_metadata"
                        ](items_version_derivative_id)
                        if (
                            derivative_metadata_df is None
                            or derivative_metadata_df.empty
                        ):
                            continue
                        item_guid = derivative_metadata_df.loc[0, "guid"]
                        try:
                            derivative_properties_df = fetch_functions[
                                "fetch_and_normalize_derivative_items_properties"
                            ](items_version_derivative_id, item_guid, row["id"])
                            if (
                                derivative_properties_df is None
                                or derivative_properties_df.empty
                            ):
                                print(
                                    f"project:  {project_id} folder eng {folder_ENG} urn derivative {items_version_derivative_id} guid {item_guid}"
                                )
                                continue

                            print(
                                f"Using this item version ID: < {items_version_derivative_id} > and this item GUID: < {item_guid} >"
                            )
                            file_path = f"{csv_folder_path}/{row['attributes.displayName']}.json"
                            print(f"Escrevendo para o arquivo: {file_path}")
                            derivative_properties_df.to_json(file_path)

                        except Exception as e:
                            print(
                                "No data found for ID: " + items_version_derivative_id
                            )
                            print("An error occurred: " + str(e))
    tempo_final = time.time()
    duracao = tempo_final - tempo_inicial
    duracao_timedelta = timedelta(seconds=duracao)
    duracao_formatada = str(duracao_timedelta)
    print(f"duração: {duracao_formatada}")
