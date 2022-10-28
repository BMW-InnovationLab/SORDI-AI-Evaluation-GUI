import math

from domain.models.bounding_box import BoundingBox


def get_euclidean_distance(gt_centroid: tuple, prediction_centroid: tuple) -> float:
    x_difference: float = prediction_centroid[0] - gt_centroid[0]
    y_difference: float = prediction_centroid[1] - gt_centroid[1]
    ED: float = round(math.sqrt(x_difference ** 2 + y_difference ** 2), 4)
    return ED


def get_iou(gt_bounding_box: BoundingBox, prediction_bounding_box: BoundingBox) -> float:
    # If there is no intersection between the boxes
    if gt_bounding_box.left > prediction_bounding_box.right or gt_bounding_box.right < prediction_bounding_box.left or \
            gt_bounding_box.top > prediction_bounding_box.bottom or \
            gt_bounding_box.bottom < prediction_bounding_box.top:

        inter_right = inter_left = inter_top = inter_bottom = 0

    else:  # in case of intersection
        inter_left: float = max(gt_bounding_box.left, prediction_bounding_box.left)
        inter_top: float = max(gt_bounding_box.top, prediction_bounding_box.top)
        inter_right: float = min(gt_bounding_box.right, prediction_bounding_box.right)
        inter_bottom: float = min(gt_bounding_box.bottom, prediction_bounding_box.bottom)

    # Finding the Intersection Area needed for calculation of IoU
    inter_area: float = (inter_right - inter_left) * (inter_bottom - inter_top)

    # Intersection / Union Score ====> IoU Score
    try:
        IoU: float = float(inter_area) / (
                float(gt_bounding_box.area) + float(prediction_bounding_box.area) - float(inter_area))
    except ZeroDivisionError:  # only case of except if all areas are 0 so the division will be by zero ==> Error
        IoU = 0.0

    return IoU


def get_bounding_box_info(bbox: BoundingBox) -> BoundingBox:
    bbox.width = bbox.right - bbox.left
    bbox.height = bbox.bottom - bbox.top
    return bbox
