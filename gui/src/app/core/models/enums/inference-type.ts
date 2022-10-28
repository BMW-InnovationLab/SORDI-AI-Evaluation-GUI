import {SelectionShape} from "../selection-shape";

export enum InferenceType {
  OBJECT_DETECTION = "object_detection",
  IMAGE_CLASSIFICATION = "image_classification"
}

export const datasetTypes: SelectionShape[] = [
  {
    name: 'Image Classification',
    value: 'image_classification'
  },
  {
    name: 'Object Detection',
    value: 'object_detection'
  }
];


export const getInferenceTypeName = (requestedValue?: string): string => {
  return datasetTypes.find(type => type.value == requestedValue)?.name;
}
