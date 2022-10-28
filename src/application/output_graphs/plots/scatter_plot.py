import os
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame

from domain.contracts.abstract_output_graphs_plot import AbstractOutputGraphsPlot
from domain.models.evaluation_job_parameters import EvaluationJobParameters


class ScatterPlot(AbstractOutputGraphsPlot):

    def _draw_plot(self, centroid_df: DataFrame, title: str, file_path: str)->None:

        all_gt_x, all_gt_y = [x[0] for x in centroid_df.gt_centroid.values], [y[1] for y in centroid_df.gt_centroid.values]
        all_pred_x, all_pred_y = [x[0] for x in centroid_df.prediction_centroid.values], [y[1] for y in centroid_df.prediction_centroid.values]



        max_x_axis: float = max(max(all_gt_x), max(all_pred_x)) + 0.02 * max(max(all_gt_x), max(all_pred_x))
        max_y_axis: float = max(max(all_gt_y), max(all_pred_y)) + 0.06 * max(max(all_gt_y), max(all_pred_y))

        min_x_axis: float = min(min(all_gt_x), min(all_pred_x))
        min_y_axis: float = min(min(all_gt_y), min(all_pred_y))

        min_x_axis: float = max(0, min_x_axis - min_x_axis * 0.05)
        min_y_axis: float = max(0, min_y_axis - min_y_axis * 0.05)

        fig, ax = plt.subplots(num=4, figsize=(16, 9), dpi=360, facecolor='w', edgecolor='k')
        ax.scatter(all_gt_x, all_gt_y, s=50, color="red", alpha=0.7, label="GT Centroid")
        ax.scatter(all_pred_x, all_pred_y, s=50, color="blue", alpha=0.7, label="Predicted Centroid")

        ax.set_ylim([min_y_axis, max_y_axis])
        ax.set_xlim([min_x_axis, max_x_axis])
        ax.set_ylim(ax.get_ylim()[::-1])  # invert the y axis axis
        ax.xaxis.tick_top()
        ax.xaxis.set_ticks(np.arange(min_x_axis, max_x_axis ,(max_x_axis - min_x_axis) / 4))  # set x-ticks ( the +1 is intended otherwise the last tick - the size of the image - will not show )
        ax.yaxis.set_ticks(np.arange(min_y_axis, max_y_axis , (max_y_axis - min_y_axis) / 4))
        ax.set_xlabel('X-axis [px]')
        ax.set_ylabel('Y-axis [px]')
        ax.set_title(title, y=1.05)
        ax.legend(loc='lower right')

        for x_gt, x_pred, y_gt, y_pred, eucludian_distance in zip(all_gt_x, all_pred_x, all_gt_y, all_pred_y, centroid_df.ecludien_distance.values):
            ax.plot([x_gt, x_pred], [y_gt, y_pred], color='yellow')
            ax.annotate(round(eucludian_distance, 2),
                         xy=(min(x_gt, x_pred) - abs(x_gt - x_pred) / 2 - 3, min(y_gt, y_pred) - abs(y_gt - y_pred) / 2 - 3),
                         xycoords='data')
        ax.figure.savefig(file_path, bbox_inches='tight', format='png')
        plt.close()
        # plt.clf()


    def draw_general_plot(self, linkages_df: DataFrame, evaluation_job_parameters: EvaluationJobParameters,
                          output_dir: str)->None:

        title: str = "Predicted Centroid vs GT Centroid of bad IoU"
        file_path: str = os.path.join(output_dir,'4-Scatter_All_Classes_Bad_IoU.png')
        centroid_df: DataFrame = linkages_df.loc[(linkages_df["iou"] < evaluation_job_parameters.iou_average_threshold) & (linkages_df["gt_centroid"].notnull())]

        if not centroid_df.empty:
            self._draw_plot(centroid_df=centroid_df, title=title, file_path=file_path)

    def draw_per_class_plot(self, linkages_df: DataFrame, evaluation_job_parameters: EvaluationJobParameters,output_dir: str)->None:
        linkages_classes: List[str] = linkages_df.loc[linkages_df.gt_label.notnull(), 'gt_label'].unique()

        for class_name in linkages_classes:
            file_path: str = os.path.join(output_dir, class_name ,'plots', '2_Scatter_'+str(class_name)+'_Class_Bad_IoU.png')
            title: str = "Predicted Centroid vs GT Centroid of bad IoU for class: " + str(class_name)
            centroid_df: DataFrame = linkages_df.loc[(linkages_df["gt_label"] == class_name) & (linkages_df["iou"] < evaluation_job_parameters.iou_average_threshold) & (linkages_df["gt_centroid"].notnull())]

            if not centroid_df.empty:
                self._draw_plot(centroid_df=centroid_df, title=title, file_path=file_path)
