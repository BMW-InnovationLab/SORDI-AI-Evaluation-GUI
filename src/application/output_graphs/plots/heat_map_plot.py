import os
from typing import List

from pandas import DataFrame
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import confusion_matrix

from domain.contracts.abstract_output_graphs_plot import AbstractOutputGraphsPlot
from domain.models.evaluation_job_parameters import EvaluationJobParameters


class HeatMapPlot(AbstractOutputGraphsPlot):

    def _draw_plot(self, confusion_df: DataFrame, title: str, file_path: str) -> None:

        sns.set_theme()
        fig, ax = plt.subplots(num=6, figsize=(16, 9), dpi=280, facecolor='w', edgecolor='k')
        sns.heatmap(confusion_df, annot=True, fmt='g', square=True, cbar=False, xticklabels=True, yticklabels=True,linewidths=.5, ax=ax, cmap="Blues")
        ax.set_xlabel('Predicted Labels')
        ax.set_ylabel('True Labels')
        ax.set_title(title)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=10)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontsize=10, rotation_mode='anchor', ha='right')

        fig.savefig(file_path, bbox_inches='tight',format='png')
        # plt.clf()

        plt.close()

    def draw_general_plot(self, linkages_df: DataFrame, evaluation_job_parameters: EvaluationJobParameters,
                          output_dir: str) -> None:
        title: str = "Multi-Class Confusion Matrix"
        file_path: str = os.path.join(output_dir,'2-Heat_Map_Multi-Class_Confusion_Matrix.png')
        prediction_labels: List[str] = linkages_df.prediction_label.astype(str).tolist()
        gt_labels: List[str] = linkages_df.gt_label.astype(str).tolist()
        all_label: List[str] = list(set(prediction_labels + gt_labels))

        # add nan to the end of all_label
        all_label.append(all_label.pop(all_label.index("nan"))) if 'nan' in all_label else all_label.append("nan")

        confusion_matrix_array: np.array = confusion_matrix(gt_labels, prediction_labels, labels=all_label)
        confusion_df: DataFrame = pd.DataFrame(confusion_matrix_array, all_label, all_label)

        self._draw_plot(confusion_df=confusion_df, title=title, file_path=file_path)

    def draw_per_class_plot(self, linkages_df: DataFrame, evaluation_job_parameters: EvaluationJobParameters,
                            output_dir: str) -> None:
        pass
