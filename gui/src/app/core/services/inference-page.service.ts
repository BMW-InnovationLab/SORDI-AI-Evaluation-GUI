import {Injectable} from '@angular/core';
import {BaseService} from './base-service';
import {Observable} from 'rxjs';
import {HttpClient} from '@angular/common/http';
import {map} from 'rxjs/operators';
import {InferenceService} from '../models/inference-service.model';
import {InferenceServiceAdapter} from '../domain/adapters/inference-service-adapter';
import {environment} from '../../../environments/environment';

@Injectable({
    providedIn: 'root'
})
export class InferencePageService extends BaseService<InferenceService> {
    private url: string = environment.url + '/services/inference';

    constructor(private http: HttpClient,
                private inferenceAdapter: InferenceServiceAdapter) {
        super();
    }

    getAll(): Observable<InferenceService[]> {
        return this.http.get(this.url)
            .pipe(map((inferenceData: any[]) =>
                inferenceData.map(item => this.inferenceAdapter.adaptToUi(item))));
    }

    post(item: InferenceService): Observable<any> {
        const url = this.url + '/add';
        return this.http.post(url, this.inferenceAdapter.adaptToRequest(item));
    }

    put(item: InferenceService): Observable<any> {
        const url = this.url + '/edit';
        return this.http.post(url, this.inferenceAdapter.adaptToRequest(item));
    }

    delete(uuid: string): Observable<any> {
        const deleteUrl = this.url + '/delete/?uuid=' + uuid;
        return this.http.post(deleteUrl, null);
    }
}
