import pandas as pd
import asyncio

from app.api.services.retrieve_metadata_derivative_service import RetrieveMetadataDerivativeService
async def get_metadata(urnOfSouce, derivativeService: RetrieveMetadataDerivativeService):
  try:
    viewables_df = await derivativeService.get_list_of_viewables(urnOfSouce)
    return viewables_df
  except Exception as e:
    print(f'erro no dataframeDerivative.py get_metadata\nurnOfSource: {urnOfSouce}\nerror >>>> {e}')

async def get_hierarchy(urnOfSouce, guid, derivativeService: RetrieveMetadataDerivativeService):
  print("urnofsource",urnOfSouce,"guid", guid)
  try:
    hierarchy_df = pd.DataFrame(await derivativeService.get_object_hierarchy(urnOfSouce, guid))
    return hierarchy_df
  except Exception as e:
    print(f'erro no dataframeDerivative.py hierarchy: \nurnOfSource: {urnOfSouce} \nguid: {guid}\nerro: >>>>\n{e}')

async def get_properties(urnOfSouce, guid, derivativeService: RetrieveMetadataDerivativeService, objectid):
  print(f"Usando urn: {urnOfSouce}, guid: {guid}")
  try:
    properties_df = await derivativeService.get_properties(urnOfSouce, guid, objectid)

    return properties_df
  except Exception as e:
    print(f'erro 1 no dataframeDerivative.py properties: \nurnOfSource: {urnOfSouce} \nguid: {guid}\nerro: >>>>\n{e}')
    st.warning("tentando novamente...")
    try:
      properties_df = await derivativeService.get_properties(urnOfSouce, guid, objectid)

      return properties_df
    except Exception as e:
      print(f'erro 2 no dataframeDerivative.py properties: \nurnOfSource: {urnOfSouce} \nguid: {guid}\nerro: >>>>\n{e}')
    return properties_df