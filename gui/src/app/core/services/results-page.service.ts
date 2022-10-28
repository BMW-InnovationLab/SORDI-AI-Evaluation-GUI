import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../../environments/environment';
import {GraphRequestModel} from '../models/graph-request-model';
import {MetricsRequest} from "../models/metrics-request";
import {JobMetric} from "../models/job-metric";
// import {of} from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})
export class ResultsPageService {
  private url = environment.url + '/graphs/web';

  constructor(private http: HttpClient) {
  }

  getGraphResult(graphRequest: GraphRequestModel): Observable<any> {
    return this.http.post(this.url, graphRequest);
  }

  getMetrics(metricsRequest: MetricsRequest): Observable<JobMetric[]> {
    let url =  environment.url + '/evaluation/jobs/metrics/' + metricsRequest.uid;
    if(metricsRequest.label_name) url += '/' + metricsRequest.label_name;
    return this.http.get<JobMetric[]>(url);
  }
}
