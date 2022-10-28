export class Definitions{
  term: string;
  definition: string;
  boundaries?: string = '';
}
const commonDefinitions: Definitions[] = [
  {
    term: "Accuracy",
    definition: "Fraction of prediction that the model predicted correctly",
  },
  {
    term: "Precision",
    definition: "Ratio of predicted positive and are actually positive.",
    boundaries: "Best: 1 - Worse 0"
  },
  {
    term: "Recall",
    definition: "Ratio of correctly identified true positives to all positive observations.",
    boundaries: "Best: 1 - Worse 0"
  },
  {
    term: "F-Score",
    definition: "Evaluate the machine learning model in one number by combining precision and recall." +
      "A good f-score means that the model is effective in terms of how precisely it classifies the data and " +
      "that it covers a good proportion of the cases that it should have classified correctly.",
    boundaries: "Best: 1 - Worse 0"
  },
  {
    term: "Confidence",
    definition: "How much the model is sure of its prediction",
  },
  {
    term: "TP",
    definition: "True positive: predicted positive and actual positive prediction.",
  },
  {
    term: "TN",
    definition: "True negative: predicted negative and actual negative prediction",
  },
  {
    term: "FP",
    definition: "False positive: predicted positive and actual negative prediction."
  },
  {
    term: "FN",
    definition: "False negative: predicted positive and actual negative prediction"
  },

]


export const classification = [
  ...commonDefinitions
];

export const objectDetection = [
  ...commonDefinitions,
  {
    term: "Average IoU",
    definition: "Value of IoU considered average"
  },
  {
    term: "Bad IoU",
    definition: "Value of IoU under which the prediction is considered incorrect"
  },
  {
    term: "IoU Grouping",
    definition: "Used to discard Prediction associated with a ground truth having an IoU smaller than IoU grouping"
  },
];

export const getDefinitions = (type: 'object_detection' | 'image_classification'): Definitions[] =>  {
  switch (type) {
    case "object_detection":
      return objectDetection;
    case "image_classification":
      return classification;
  }
}

