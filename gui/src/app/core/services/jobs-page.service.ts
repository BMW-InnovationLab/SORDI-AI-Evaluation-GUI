import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {map, tap} from 'rxjs/operators';
import {environment} from '../../../environments/environment';
import {EvaluationJobStatus} from '../models/evaluation-job-status-model';
import {EvaluationJob} from '../models/evaluation-job-model';
import {EvaluationJobAdapter} from '../domain/adapters/evaluation-job-adapter';

@Injectable({
    providedIn: 'root'
})
export class JobsPageService {
    private url: string = environment.url + '/evaluation/jobs';

    constructor(private http: HttpClient, private evaluationJobAdapter: EvaluationJobAdapter) {
    }

    get(uuid: string): Observable<any> {
        const url = this.url + '/parameters?uid=' + uuid;
        return this.http.get(url)
            .pipe(
                tap((inferenceData) => {
                    inferenceData = this.evaluationJobAdapter.adaptToUi(inferenceData);
                    return inferenceData;
                }));
    }

    getJobsStatuses(): Observable<EvaluationJobStatus[]> {
        const url = this.url + '/status';
        return this.http.get(url)
            .pipe(map((jobStatusData: any[]) =>
                jobStatusData.map((jobStatus: any) => new EvaluationJobStatus(
                    jobStatus.uid,
                    jobStatus.job_name,
                    jobStatus.status,
                    jobStatus.progress,
                    jobStatus.dataset_name,
                    jobStatus.model_name,
                    jobStatus.author_name
                ))));
    }

  getJobStatus(uuid: string): Observable<EvaluationJobStatus[]> {
    const url = this.url + '/status/'+uuid;
    return this.http.get(url)
      .pipe(map((jobStatus: any) =>  new EvaluationJobStatus(
          jobStatus.uid,
          jobStatus.job_name,
          jobStatus.status,
          jobStatus.progress,
          jobStatus.dataset_name,
          jobStatus.model_name,
          jobStatus.author_name
        )));
  }

    getJobLabels(uuid: string): Observable<any> {
        const url = this.url + '/labels?uid=' + uuid;
        return this.http.get(url);
    }


    post(item: EvaluationJob): Observable<any> {
        return this.http.post(this.url, this.evaluationJobAdapter.adaptToRequest(item));
    }

    delete(uuid: string): Observable<any> {
        const url = this.url + '/remove/?uid=' + uuid;
        return this.http.post(url, null);
    }

}
