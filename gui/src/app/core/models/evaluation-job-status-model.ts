export class EvaluationJobStatus {
    constructor(
        public uid: string,
        // tslint:disable-next-line:variable-name
        public job_name: string,
        public status: string,
        public progress?: number,
        // tslint:disable-next-line:variable-name
        public dataset_name?: string,
        // tslint:disable-next-line:variable-name
        public model_name?: string,
        // tslint:disable-next-line:variable-name
        public author_name?: string,
    ) {
    }
}
