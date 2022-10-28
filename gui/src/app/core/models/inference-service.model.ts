import {InferenceType} from "./enums/inference-type";

export class InferenceService {
    constructor(
        public name: string,
        public url: string,
        public models: string[] = [],
        public inferenceType: InferenceType,
        public uuid?: string,
        public editable: boolean = false,
        public discoverModels: boolean = false,
        public refreshing: boolean = false,
    ) {
    }
}
