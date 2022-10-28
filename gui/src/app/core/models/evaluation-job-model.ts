export class EvaluationJob {
    constructor(
        public datasetName: string,
        public authorName: string,
        public url: string,
        public modelName: string,
        public jobName: string,
        public jobType: string,
        public batchSize: number = 50,
        public uid?: string,
        public labelsType?: string,
        public iouThreshold?: number,
        public iouAverageThreshold?: number,
        public iouGoodThreshold?: number,
        public confidenceThreshold?: number,
    ) {
    }
}
