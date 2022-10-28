import os
from typing import List

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pandas import DataFrame

from domain.contracts.abstract_output_graphs_plot import AbstractOutputGraphsPlot
from domain.models.evaluation_job_parameters import EvaluationJobParameters
from domain.models.linkage_type import LinkageType


class ConfusionMatrixPlot(AbstractOutputGraphsPlot):
    def _draw_plot(self, linkages_data: List[int], file_path: str) -> None:
        # general format [TN, FP,FN,TP]
        confusion_matrix: np.array = np.array([[linkages_data[1], linkages_data[2]], [linkages_data[3], linkages_data[0]]])

        linkages_name: List[str] = ['True Negative', 'False Positive', 'False Negative', 'True Positive']
        linkages_count: List[int] = ["{0:0.0f}".format(value) for value in confusion_matrix.flatten()]
        linkages_percentage: List[str] = ["{0:.2%}".format(value) for value in confusion_matrix.flatten() / np.sum(confusion_matrix)]
        linkages_labels: List[str] = [f"{v1}\n{v2}\n{v3}" for v1, v2, v3 in zip(linkages_name, linkages_count, linkages_percentage)]
        linkages_labels: np.array = np.asarray(linkages_labels).reshape(2, 2)

        fig, ax = plt.subplots(num=5, figsize=(16, 9), dpi=120, facecolor='w', edgecolor='k')
        sns.heatmap(confusion_matrix, annot=linkages_labels, fmt='', square=True, cbar=False, xticklabels=True,yticklabels=True,linewidths=.5, ax=ax, cmap="Blues")

        ax.set_xlabel('Predicted Labels')
        ax.set_ylabel('True Labels')
        ax.set_title("Confusion Matrix")
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=10)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontsize=10, rotation_mode='anchor', ha='right')

        fig.savefig(file_path, bbox_inches='tight',format='png')
        plt.close()
        # plt.clf()


    def draw_general_plot(self, linkages_df: DataFrame, evaluation_job_parameters: EvaluationJobParameters,
                          output_dir: str) -> None:
        file_path: str = os.path.join(output_dir, '1-Heat_Map_Confusion_Matrix.png')
        linkage_types: List[str] = [linkage_type.value for linkage_type in LinkageType]
        linkages_data: List[int] = [(linkages_df.linkage_type.values == label).sum() for label in linkage_types]
        self._draw_plot(linkages_data=linkages_data, file_path=file_path)

    def draw_per_class_plot(self, linkages_df: DataFrame, evaluation_job_parameters: EvaluationJobParameters,
                            output_dir: str) -> None:
        pass
