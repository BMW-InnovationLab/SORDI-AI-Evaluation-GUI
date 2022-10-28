import {AfterContentInit, Component, OnDestroy, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {forkJoin} from 'rxjs';
import {tap} from 'rxjs/operators';
import {NzMessageService} from 'ng-zorro-antd/message';
import {environment} from '../../../environments/environment.prod';
import {GraphResponseModel} from '../../core/models/graph-response-model';
import {EvaluationJob} from '../../core/models/evaluation-job-model';
import {ResultsPageService} from '../../core/services/results-page.service';
import {JobsPageService} from '../../core/services/jobs-page.service';
import {EvaluationJobAdapter} from '../../core/domain/adapters/evaluation-job-adapter';
import {GraphRequestModel} from '../../core/models/graph-request-model';
import {GraphNamesClassification, GraphNamesObjectDetection} from '../../core/models/enums/graph-names';
import {EvaluationJobStatus} from "../../core/models/evaluation-job-status-model";
import {JobMetric} from "../../core/models/job-metric";

@Component({
  selector: 'app-results-page',
  templateUrl: './results-page.component.html',
  styleUrls: ['./results-page.component.css']
})

export class ResultsPageComponent implements OnInit, AfterContentInit, OnDestroy {
  public graphsData: GraphResponseModel[] = [];
  public pageReady = false;
  public requestedJob: EvaluationJob;
  public requestedJobStatus: EvaluationJobStatus;
  public metrics: JobMetric[] = [];
  public mobile: boolean;
  public pageTitle: string;
  public tabs = ['General', 'Label_1', 'Label_2', 'Other'];
  private requestedUuid: string;
  private currentTab = 'General';
  private readonly baseImageUrl = environment.url + '/images/';
  public imageSource = {
    url: this.baseImageUrl,
    perLabel: false
  };
  private refreshInterval;

  constructor(private router: Router,
              private route: ActivatedRoute,
              public resultsPageService: ResultsPageService,
              private evaluationJobService: JobsPageService,
              private message: NzMessageService,
              private evaluationJobAdapter: EvaluationJobAdapter
  ) {

    this.route.params.subscribe(params => {
      const uid = params['uid'];
      // if(!uid) this.router.navigateByUrl('/jobs').then();
      this.requestedUuid = uid;
    });
    this.baseImageUrl += this.requestedUuid + '/';
  }

  ngOnInit(): void {
    this.updatePage();
    this.imageSource.url = this.baseImageUrl;
    this.initMobile();
  }

  ngAfterContentInit() {
    this.refreshPage();
    this.refreshInterval = setInterval(() => this.refreshPage(), 5000);
  }

  ngOnDestroy() {
    clearInterval(this.refreshInterval);
  }

  public updateLabels(uuid: string): void {
    this.evaluationJobService.getJobLabels(uuid)
      .subscribe(res => {
        this.tabs = ['General', ...res];
      }, () => {
        this.tabs = ['General', 'Label_1', 'Label_2', 'Other'];
      });
  }

  public downloadResults(): void {
    const url = environment.url + '/results/' + this.requestedUuid + '.zip';
    window.open(url);
  }

  public changeTab(labelIndex: number) {
    const newLabelClicked = this.tabs[labelIndex];
    // console.log(newLabelClicked);
    this.currentTab = newLabelClicked;
    this.imageSource = (newLabelClicked !== 'General') ?
      {url: this.baseImageUrl + newLabelClicked + '/', perLabel: true}
      : {url: this.baseImageUrl, perLabel: false};
    this.updatePage();
  }


  private refreshPage(): void {
    this.evaluationJobService.getJobStatus(this.requestedUuid)
      .subscribe((jobsStatusData) => {
        this.requestedJobStatus = jobsStatusData;
        if (this.requestedJobStatus.progress == 100) clearInterval(this.refreshInterval);
      }, _ => this.message.error('Can\'t get results'));
  }

  private initMobile(): void {
    this.mobile = window.screen.width <= 1024;
    window.onresize = () => {
      this.mobile = window.screen.width <= 1024;
    };
  }

  private updatePage(): void {
    this.updateLabels(this.requestedUuid);
    this.evaluationJobService.get(this.requestedUuid).subscribe(jobParameters => {
      this.pageReady = false;
      this.requestedJob = this.evaluationJobAdapter.adaptToUi(jobParameters);
      this.pageTitle = this.requestedJob.jobName;
      this.getGraphs(this.currentTab);
      const requestedLabel = (this.currentTab !== 'General') ? this.currentTab : null;
      this.metrics = [];
      this.resultsPageService.getMetrics({uid: this.requestedUuid, label_name : requestedLabel})
        .subscribe(res => {
          this.metrics = res;
          if (requestedLabel) {
            this.metrics =   res.filter(  ( ele ) => {
              return ele.metric !== 'Average Precision';
            });
          }
          res.find(v => v.metric === 'Average Precision').metric = 'mAP';
        });
    });
  }

  private getGraphs(labelName = 'General'): void {
    const requiredGraphs = this.getRequiredGraphs(this.requestedJob.jobType, this.currentTab !== 'General');
    const graphObservables = {};
    const requestedLabel = (labelName !== 'General') ? labelName : null;
    requiredGraphs.forEach(graphName => {
      const request: GraphRequestModel = {
        uid: this.requestedJob.uid,
        graph_name: graphName,
        label_name: requestedLabel,
        job_type: this.requestedJob.jobType,
        iou_good_threshold: this.requestedJob.iouGoodThreshold,
        iou_average_threshold: this.requestedJob.iouAverageThreshold
      };
      graphObservables[graphName] = this.resultsPageService.getGraphResult(request)
        .pipe(tap((data) => {
          this.graphsData[graphName] = data;
        }));
    });
    this.getData(graphObservables);
  }

  private getData(graphObservables = {}): void {
    this.graphsData = [];
    forkJoin(graphObservables).subscribe(() => {
      this.pageReady = true;
    }, _ => {
      this.router.navigateByUrl('/jobs-page').then(() => {
        this.message.create('error', 'Results are not ready yet.', {nzPauseOnHover: true, nzDuration: 2500});
      });
    });
  }

  private getRequiredGraphs(labelType = 'object_detection' || 'image_classification', withLabel = false): string[] {
    const graphsNames = (labelType === 'object_detection') ? GraphNamesObjectDetection : GraphNamesClassification;
    let graphs = Object.values(graphsNames);
    if (withLabel) {
      graphs = graphs.filter(item => item !== 'heat_map');
    }
    return graphs;
  }
}
