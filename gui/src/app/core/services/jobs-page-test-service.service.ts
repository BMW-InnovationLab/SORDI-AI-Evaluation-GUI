import {Injectable} from '@angular/core';
import {EMPTY, Observable, of} from 'rxjs';
import {EvaluationJobStatus} from '../models/evaluation-job-status-model';
import {JobStatus} from '../models/enums/job-status';
import {EvaluationJob} from '../models/evaluation-job-model';

@Injectable({
  providedIn: 'root'
})
export class JobsPageTestServiceService {

  private jobsOverview: EvaluationJobStatus[] = [
    {
      uid: '1',
      job_name: 'job1',
      status: JobStatus.InProgress,
      author_name: 'aaaaaaaaaa',
      dataset_name: 'dataset1',
      model_name: 'model1 looooooooooooooooooooooooooooooooooooooong',
      progress: 30
    },
    {
      uid: '2',
      job_name: 'job2',
      status: JobStatus.InProgress,
      author_name: 'Author1',
      dataset_name: 'dataset1',
      model_name: 'model2',
      progress: 45
    },
    {
      uid: 'ew1',
      job_name: 'job3',
      status: JobStatus.Done,
      author_name: 'Author1',
      dataset_name: 'dataset2',
      model_name: 'model3',
      progress: 100
    },
    {
      uid: 'e4re1',
      job_name: 'job4',
      status: JobStatus.InProgress,
      author_name: 'Author1',
      dataset_name: 'dataset1',
      model_name: 'model1',
      progress: 10
    },
    {
      uid: '1fsfs',
      job_name: 'job6',
      status: JobStatus.InProgress,
      author_name: 'Author1',
      dataset_name: 'dataset1',
      model_name: 'model1',
      progress: 70
    },
  ];

  constructor() {
  }

  getJobsStatuses(): Observable<EvaluationJobStatus[]> {
    return of(this.jobsOverview);
  }

  get(uuid: string): Observable<any> {
    return EMPTY;
  }

  getJobLabels(uuid: string): Observable<any> {
    return EMPTY;
  }


  post(item: EvaluationJob): Observable<any> {
    return EMPTY;
  }

  delete(uuid: string): Observable<any> {
    return EMPTY;

  }
}
