from typing import Optional, List

from pydantic import BaseModel, validator


class WebGraphsParameters(BaseModel):
    uid: str
    job_type: str
    graph_name: str
    label_name: Optional[str]
    iou_good_threshold: Optional[float]
    iou_average_threshold: Optional[float]

    @validator('job_type', pre=True)
    def check_job_type(cls , job_type):
        accepted_job_type =[
            'object_detection',
            'image_classification'
        ]
        if job_type not in accepted_job_type:
            raise ValueError("Job type not supported")
        else:
            return job_type

    @validator('graph_name', pre=True)
    def check_graph_name(cls, graph_name: str, values):
        accepted_object_detection_graphs: List[str] = [
            'heat_map',
            'histogram',
            'pie_chart'
        ]
        accepted_image_classification_graphs: List[str] = [
            'heat_map',
            'pie_chart'
        ]
        if graph_name not in accepted_object_detection_graphs and graph_name not in accepted_image_classification_graphs:
            raise ValueError("Unknown Web Graph Name: Web Graph Not Supported")
        elif "job_type" in values and values["job_type"] =="image_classification" and graph_name not in accepted_image_classification_graphs:
            raise ValueError("graph type not supported for image_classification")
        else:
            return graph_name

    @validator('label_name')
    def check_label_name(cls, label_name: str, values):
        accepted_per_label_graphs: List[str] = [
            'pie_chart',
            'histogram'
        ]
        if "graph_name" not in values:
            raise ValueError("graph_name not supported")
        elif (values["graph_name"] in accepted_per_label_graphs and label_name is not None) or (label_name is None):
            return label_name
        else:
            raise ValueError("label_name  is not supported for: " + str(values["graph_name"]))
