import os
import azure.functions as func

os.makedirs("./input", exist_ok=True)
os.makedirs("./output", exist_ok=True)


def main(req: func.HttpRequest) -> func.HttpResponse:
    print("Function triggered")
    return func.HttpResponse("Process completed successfully", status_code=200)


if __name__ == "__main__":
    main()
