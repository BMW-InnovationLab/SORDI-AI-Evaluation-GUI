import {AfterContentInit, Component, OnDestroy, ViewChild} from '@angular/core';
import {Router} from '@angular/router';
import {NzMessageService} from 'ng-zorro-antd/message';
import {JobsPageService} from '../../core/services/jobs-page.service';
import {EvaluationJobStatus} from '../../core/models/evaluation-job-status-model';
import {EvaluationJobAdapter} from '../../core/domain/adapters/evaluation-job-adapter';
import {JobStatus} from '../../core/models/enums/job-status';
import {SearchComponent} from "./components/search/search.component";
import {FilterQuery} from "./models/filter-query";
import {FilterType} from "./models/filter-type";


@Component({
  selector: 'app-jobs-page',
  templateUrl: './jobs-page.component.html',
  styleUrls: ['./jobs-page.component.css']
})
export class JobsPageComponent implements AfterContentInit, OnDestroy {
  @ViewChild(SearchComponent, {static: false}) searchComponent: SearchComponent;
  // public readonly PAGE_SIZE = 2;
  // public currentPage = 1;
  public evaluationJobsStatusList: EvaluationJobStatus[] = [];
  public evaluationJobsStatusListToDisplay: EvaluationJobStatus[] = [];
  private refreshInterval;


  constructor(public jobsPageService: JobsPageService,
              private evaluationJobService: JobsPageService,
              public router: Router,
              private evaluationJobAdapter: EvaluationJobAdapter,
              private message: NzMessageService) {
  }

  public get jobStatus(): typeof JobStatus {
    return JobStatus;
  }

  ngAfterContentInit(): void {
    this.refreshPage();
    this.refreshInterval = setInterval(() => this.refreshPage(), 10000);
  }

  ngOnDestroy(): void {
    clearInterval(this.refreshInterval);
  }

  // public moveToPage(evt: number): void {
  //   this.currentPage = evt;
  //   this.updatePage();
  // }

  public navigateToResultsPage(selectedJob: EvaluationJobStatus): void {
    if (selectedJob.progress == 0)
      this.message.create('error', 'Results are not ready yet.', {
        nzPauseOnHover: true,
        nzDuration: 2500
      })
    else this.resultsReadyForNavigation(selectedJob);
  }


  public removeJob(job: EvaluationJobStatus): void {
    const index = this.evaluationJobsStatusList.indexOf(job);
    this.jobsPageService.delete(job.uid).subscribe(() => {
        this.evaluationJobsStatusListToDisplay.splice(index, 1);
        this.refreshPage();
      }
      , error => {
      this.message.create('error', error, {nzPauseOnHover: true, nzDuration: 2500});
      });
  }

  showFiltered($event: EvaluationJobStatus[]) {
    this.evaluationJobsStatusListToDisplay = $event;
  }

  // private updatePage(): void {
  //   this.evaluationJobsStatusListToDisplay = [...this.evaluationJobsStatusList].splice
  //   ((this.currentPage - 1) * this.PAGE_SIZE, this.PAGE_SIZE);
  // }

  activateFilter($event: FilterQuery) {
    const query = this.searchComponent.filterQuery;

    switch ($event.filter) {
      case FilterType.DATASET:
        query.dataset = [$event.value];
        break;
      case FilterType.MODEL:
        query.model = [$event.value];
        break;
    }
    this.searchComponent.filterQuery = query;
  }

  private refreshPage(): void {
    this.jobsPageService.getJobsStatuses()
      .subscribe((jobsStatusData) => {
        this.evaluationJobsStatusList = jobsStatusData;
        this.searchComponent?.refreshFilter(jobsStatusData);
      }, error => {
        this.message.error('Can\'t get results');
      });
  }

  private resultsReadyForNavigation(selectedJob): void {
    this.router.navigate(['/', 'jobs', 'results', selectedJob.uid], {
      state: {
        uuid: selectedJob.uid,
        pageTitle: selectedJob.job_name,
        isDone: (selectedJob.status === this.jobStatus.Done)
      }
    });
  }
}
