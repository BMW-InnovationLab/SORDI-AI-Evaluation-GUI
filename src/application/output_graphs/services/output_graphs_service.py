import os
from typing import List
from pandas import DataFrame

from application.output_graphs.plots.confusion_matrix_plot import ConfusionMatrixPlot
from application.output_graphs.plots.heat_map_plot import HeatMapPlot
from application.output_graphs.plots.histogram_plot import HistogramPlot
from application.output_graphs.plots.scatter_plot import ScatterPlot
from application.results.services.labels_retrieval_service import LabelsRetrievalService
from domain.contracts.abstract_output_graphs_service import AbstractOutputGraphsService

from domain.models.evaluation_job_parameters import EvaluationJobParameters


class OutputGraphsService(AbstractOutputGraphsService):

    def __init__(self):
        self.confusion_matrix_plot = ConfusionMatrixPlot()
        self.heat_map_plot = HeatMapPlot()
        self.histogram_plot = HistogramPlot()
        self.scatter_plot = ScatterPlot()

    def _get_object_detection_per_class_plot(self, linkages_df: DataFrame,
                                             evaluation_job_parameters: EvaluationJobParameters,
                                             output_dir: str):

        output_dir: str = os.path.join(output_dir, '02-Specific Per Label Evaluation')
        self.histogram_plot.draw_per_class_plot(linkages_df=linkages_df,
                                                evaluation_job_parameters=evaluation_job_parameters,
                                                output_dir=output_dir)
        self.scatter_plot.draw_per_class_plot(linkages_df=linkages_df,
                                              evaluation_job_parameters=evaluation_job_parameters,
                                              output_dir=output_dir)

    def _get_object_detection_general_plot(self, linkages_df: DataFrame,
                                           evaluation_job_parameters: EvaluationJobParameters,
                                           output_dir: str):

        output_dir: str = os.path.join(output_dir, '01-General Evaluation')

        self.confusion_matrix_plot.draw_general_plot(linkages_df=linkages_df,
                                                     evaluation_job_parameters=evaluation_job_parameters,
                                                     output_dir=output_dir)
        self.heat_map_plot.draw_general_plot(linkages_df=linkages_df,
                                             evaluation_job_parameters=evaluation_job_parameters,
                                             output_dir=output_dir)
        self.histogram_plot.draw_general_plot(linkages_df=linkages_df,
                                              evaluation_job_parameters=evaluation_job_parameters,
                                              output_dir=output_dir)
        self.scatter_plot.draw_general_plot(linkages_df=linkages_df,
                                            evaluation_job_parameters=evaluation_job_parameters,
                                            output_dir=output_dir)

    def _get_image_classification_general_plot(self, linkages_df: DataFrame,
                                               evaluation_job_parameters: EvaluationJobParameters, output_dir: str):
        output_dir: str = os.path.join(output_dir, '01-General Evaluation')

        self.heat_map_plot.draw_general_plot(linkages_df=linkages_df,
                                             evaluation_job_parameters=evaluation_job_parameters, output_dir=output_dir)
        self.confusion_matrix_plot.draw_general_plot(linkages_df=linkages_df,
                                                evaluation_job_parameters=evaluation_job_parameters,
                                                output_dir=output_dir)

    def plot(self, linkages_df: DataFrame, output_dir: str,
             evaluation_job_parameters: EvaluationJobParameters):
        if evaluation_job_parameters.job_type == "object_detection":
            self._get_object_detection_general_plot(linkages_df=linkages_df,
                                                    evaluation_job_parameters=evaluation_job_parameters,
                                                    output_dir=output_dir)
            self._get_object_detection_per_class_plot(linkages_df=linkages_df,
                                                      evaluation_job_parameters=evaluation_job_parameters,
                                                      output_dir=output_dir)
        elif evaluation_job_parameters.job_type == "image_classification":
            self._get_image_classification_general_plot(linkages_df=linkages_df,
                                                        evaluation_job_parameters=evaluation_job_parameters,
                                                        output_dir=output_dir)
