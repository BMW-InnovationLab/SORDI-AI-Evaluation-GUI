import {Injectable} from '@angular/core';
import {AdapterInterface} from './adapter-interface';
import {InferenceService} from '../../models/inference-service.model';

@Injectable({
    providedIn: 'root'
})
export class InferenceServiceAdapter implements AdapterInterface<InferenceService> {
    adaptToUi(inferenceServiceResponse: any): InferenceService {
        return new InferenceService(inferenceServiceResponse.name,
            inferenceServiceResponse.url,
            inferenceServiceResponse.models,
            inferenceServiceResponse.inference_type,
            inferenceServiceResponse.uuid
        );
    }

    adaptToRequest(item: InferenceService): any {
        return {
            uuid: item.uuid,
            name: item.name,
            url: item.url,
            inference_type: item.inferenceType,
            models: item.models,
            discover_models: item.discoverModels
        };
    }
}
