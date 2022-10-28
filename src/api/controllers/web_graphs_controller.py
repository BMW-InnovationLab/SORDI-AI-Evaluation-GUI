import pandas
from fastapi import APIRouter, HTTPException
from pandas import DataFrame

from application.web_graphs.services.web_graph_service import WebGraphService
from containers import Services, Repositories
from domain.excpetions.application_error import ApplicationError
from domain.excpetions.web_graphs_exceptions import InvalidLabelName, WebGraphsGenralException
from domain.models.web_graph_output_object import WebGraphsOutputObject
from domain.models.web_graphs_parameters import WebGraphsParameters

router = APIRouter()

web_graph_service = Services.web_graph_service()
result_retrival_service = Services.results_retrieval_service()


@router.post("/", response_model=WebGraphsOutputObject)
async def get_web_graphs_data(web_graph_parameter: WebGraphsParameters) -> WebGraphsOutputObject:
    linkages_df: DataFrame = result_retrival_service.get_results(web_graph_parameter.uid).linkages_by_iou
    if linkages_df.empty:
        raise HTTPException(status_code=400, detail="Evaluation Job Not Finished Yet")
    else:
        try:
            return web_graph_service.get_web_graphs_data(linkages_df=linkages_df,
                                                         web_graphs_parameters=web_graph_parameter)
        except ApplicationError as e:
            raise HTTPException(status_code=e.status_code, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail=e.__str__())
