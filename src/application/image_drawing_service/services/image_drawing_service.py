from typing import List
import cv2
from PIL import Image, ImageDraw, ImageFont

from pandas import DataFrame

from domain.contracts.abstract_image_drawing_service import AbstractImageDrawingService


class ImageDrawingService(AbstractImageDrawingService):
    def __init__(self):
        self.font = ImageFont.truetype('../data/DejaVuSans.ttf', 15)

    def draw_text_on_image(self, image_path: str, output_path: str, gt_label: str, predicted_label: str) -> None:
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        width, height = image.size

        font_size: float = min(width, height) * 0.1

        font = ImageFont.truetype('../data/DejaVuSans.ttf', int(font_size))
        # draw legends
        draw.text((0, 0), gt_label, '#008FFB', font=font, align="center")
        draw.text((0, 0 + height * 0.1), predicted_label, '#FF4560', font=font, align="center")
        image.save(output_path, 'PNG')

    # def draw_bounding_box_on_image(self, image_path: str, image_output_path: str, gt_bbox_coordinates: List[DataFrame], pred_bbox_coordinates: List[DataFrame],
    #                                include_legend: bool = True) -> None:
    #     image = Image.open(image_path)
    #     draw = ImageDraw.Draw(image)
    #     width, height = image.size
    #
    #     [draw.rectangle([gt_bbox.left, gt_bbox.top, gt_bbox.right, gt_bbox.bottom], outline="#008FFB", width=3) for gt_bbox in gt_bbox_coordinates]
    #     [draw.rectangle([pred_bbox.left, pred_bbox.top, pred_bbox.right, pred_bbox.bottom], outline="#FF4560", width=3) for pred_bbox in pred_bbox_coordinates]
    #
    #     if len(pred_bbox_coordinates) > 0 or len(gt_bbox_coordinates) > 0:
    #         if include_legend:
    #             # draw legends
    #             draw.text((width - width * 0.1, height - height * 0.18), "True Label", '#008FFB', font=self.font, align="center")
    #             draw.line([(width - width * 0.1, height - height * 0.15), (width - width * 0.01, height - height * 0.15)], fill="#008FFB", width=5)
    #             draw.text((width - width * 0.1, height - height * 0.13), "Predicted Label", '#FF4560', font=self.font, align="center")
    #             draw.line([(width - width * 0.1, height - height * 0.1), (width - width * 0.01, height - height * 0.1)], fill="#FF4560", width=5)
    #         image.save(image_output_path, 'PNG')
    def draw_bounding_box_on_image(self, image_path: str, image_output_path: str, gt_bbox_coordinates: List[DataFrame], pred_bbox_coordinates: List[DataFrame],
                                   include_legend: bool = True) -> None:

        image = cv2.imread(image_path)
        height,width, channels = image.shape


        [cv2.rectangle(image, (gt_bbox.left, gt_bbox.top), (gt_bbox.right, gt_bbox.bottom), color=(251, 143, 0),
                       thickness=2) for
         gt_bbox in gt_bbox_coordinates]
        [cv2.rectangle(image, (pred_bbox.left, pred_bbox.top), (pred_bbox.right, pred_bbox.bottom), color=(96, 69, 255),
                       thickness=2)
         for pred_bbox in pred_bbox_coordinates]

        if len(pred_bbox_coordinates) > 0 or len(gt_bbox_coordinates) > 0:
            if include_legend:
                # draw legends
                cv2.putText(image, "True Label", (0, int(height - height * 0.16)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (251, 143, 0), 1)
                cv2.line(image, (0, int(height - height * 0.15)), (int(width * 0.1), int(height - height * 0.15)), (251, 143,
                                                                                                                                                    0), 2)

                cv2.putText(image, "Predicted Label", (0, int(height - height * 0.11)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (96, 69, 255), 1)
                cv2.line(image, (0, int(height - height * 0.1)), (int(width * 0.1), int(height - height * 0.1)), (96, 69,
                                                                                                                                                  255), 2)

            cv2.imwrite(image_output_path, image)

