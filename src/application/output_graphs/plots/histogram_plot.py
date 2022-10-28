import os
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame

from domain.contracts.abstract_output_graphs_plot import AbstractOutputGraphsPlot
from domain.models.evaluation_job_parameters import EvaluationJobParameters


class HistogramPlot(AbstractOutputGraphsPlot):
    def _draw_plot(self, iou_values: np.array, evaluation_job_parameters: EvaluationJobParameters, title: str, file_path: str) -> None:
        all_bins: List[List[float]] = \
            [[round(i, 2) for i in np.arange(0, evaluation_job_parameters.iou_average_threshold + 0.01, 0.05).tolist()],
             [round(i, 2) for i in np.arange(evaluation_job_parameters.iou_average_threshold,evaluation_job_parameters.iou_good_threshold + 0.01, 0.05).tolist()],
             [round(i, 2) for i in np.arange(evaluation_job_parameters.iou_good_threshold, 1.01, 0.05).tolist()]]

        fig, ax = plt.subplots(num=3, figsize=(16, 9), dpi=360, facecolor='w', edgecolor='k')

        ax.hist(x=iou_values, bins=all_bins[0], facecolor="#FF0000", alpha=0.5, label="Bad IoU", linewidth=1,
                 edgecolor='black')
        ax.hist(x=iou_values, bins=all_bins[1], facecolor="#1778F2", alpha=0.5, label="Average IoU", linewidth=1,
                 edgecolor='black')
        ax.hist(x=iou_values, bins=all_bins[2], facecolor="#25D366", alpha=0.5, label="Good IoU", linewidth=1,
                 edgecolor='black')

        ax.legend(loc='upper left')
        ax.set_xlabel('IoU')
        ax.set_ylabel('Number of detections')
        ax.set_title(title, fontweight="bold")
        ax.set_xticks(np.arange(0, 1.1, step=0.1))
        ax.set_xlim(0, 1)

        ax.figure.savefig(file_path, bbox_inches='tight', format='png')
        # plt.clf()

        plt.close()

    def draw_general_plot(self, linkages_df: DataFrame, evaluation_job_parameters: EvaluationJobParameters,
                          output_dir: str) -> None:
        title: str = "IoU Vs Number of detections"
        file_path : str = os.path.join(output_dir,'3-Histogram_All_Classes_IoU_Partition.png' )
        all_iou_values: np.array = linkages_df.iou.values[pd.notnull(linkages_df.iou.values)]
        self._draw_plot(iou_values=all_iou_values, evaluation_job_parameters=evaluation_job_parameters, title=title,
                        file_path=file_path)

    def draw_per_class_plot(self, linkages_df: DataFrame, evaluation_job_parameters: EvaluationJobParameters,
                            output_dir: str) -> None:
        linkages_classes: List[str] = linkages_df.loc[linkages_df.gt_label.notnull(), 'gt_label'].unique()

        for class_name in linkages_classes:
            file_path: str = os.path.join(output_dir, class_name ,'plots', '1-Histogram_'+str(class_name)+'_Class_IoU_Partition.png')
            title: str = "IoU Vs Number of detections for class: " + str(class_name)
            per_class_iou_values: np.array = linkages_df.loc[(linkages_df["gt_label"] == class_name) & (linkages_df["iou"].notnull()), "iou"].values

            if per_class_iou_values.size > 0:
                self._draw_plot(iou_values=per_class_iou_values, evaluation_job_parameters=evaluation_job_parameters,
                                title=title, file_path=file_path)
