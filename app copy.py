from fetch_data_functions.fetch_data import fetch_functions
from blacklist import blacklist
from go import go
import subprocess
import os
import traceback
import azure.functions as func

os.makedirs("./input", exist_ok=True)
os.makedirs("./output", exist_ok=True)


def fetch_hubid_and_projects():
    hub_id = fetch_functions["fetch_hub_id"]()
    projects_df = fetch_functions["fetch_and_normalize_projects"](hub_id)
    return hub_id, projects_df


def main():
    try:
        hub_id, projects_df = fetch_hubid_and_projects()
        full_project_list_names = [row for row in projects_df["attributes.name"]]
        project_list_names = [
            name for name in full_project_list_names if name in blacklist
        ]
        print(project_list_names)
        go(hub_id, projects_df, project_list_names)
        # OBSERVAR A NECESSIDADE DE USAR SUBPROCESS OU EXTRAIR PRA FUNC
        subprocess.run(["./venv/Scripts/python.exe", "inputProcesser.py"])
        return "OK"
    except Exception as e:
        traceback.print_exc()


if __name__ == "__main__":
    main()
