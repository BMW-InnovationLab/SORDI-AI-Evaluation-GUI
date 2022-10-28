import {Injectable} from '@angular/core';
import {AdapterInterface} from './adapter-interface';
import {EvaluationJob} from '../../models/evaluation-job-model';

@Injectable({
    providedIn: 'root'
})
export class EvaluationJobAdapter implements AdapterInterface<EvaluationJob> {
    adaptToUi(evaluationJobResponse: any): EvaluationJob {
        return new EvaluationJob(
            evaluationJobResponse.dataset_name,
            evaluationJobResponse.author_name,
            evaluationJobResponse.url,
            evaluationJobResponse.model_name,
            evaluationJobResponse.job_name,
            evaluationJobResponse.job_type,
          evaluationJobResponse.batch_size || 20,
            evaluationJobResponse.uid,
            evaluationJobResponse.labels_type,
            evaluationJobResponse.iou_threshold,
            evaluationJobResponse.iou_average_threshold,
            evaluationJobResponse.iou_good_threshold,
          evaluationJobResponse.confidence_threshold
        );
    }

    adaptToRequest(item: EvaluationJob): any {
        return {
            uid: item.uid,
            author_name: item.authorName,
            dataset_name: item.datasetName,
            job_name: item.jobName,
            job_type: item.jobType,
            batch_size: item.batchSize,
            url: item.url,
            model_name: item.modelName,
            labels_type: item.labelsType || 'json',
            iou_threshold: item.iouThreshold,
            iou_average_threshold: item.iouAverageThreshold,
            iou_good_threshold: item.iouGoodThreshold,
            confidence_threshold: item.confidenceThreshold
        };
    }
}
