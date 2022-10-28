export interface GraphRequestModel {
    uid: string;
    job_type: string;
    graph_name: string;
    label_name?: string;
    iou_good_threshold?: number;
    iou_average_threshold?: number;
}
