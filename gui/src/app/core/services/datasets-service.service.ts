import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../../environments/environment';
import {DatasetInformation} from "../models/dataset-information";

@Injectable({
    providedIn: 'root'
})
export class DatasetsService {
    private url = environment.url + '/datasets';
    public readonly uploadUrl = environment.url + '/datasets/upload';

    constructor(private http: HttpClient) {
    }

    getAvailableDatasets(): Observable<DatasetInformation> {
        const url = this.url;
        return this.http.get<DatasetInformation>(url);
    }

    upload(formData: FormData): Observable<any> {
        return this.http.post(this.uploadUrl, formData, {reportProgress: true, observe: 'events'});
    }

}
