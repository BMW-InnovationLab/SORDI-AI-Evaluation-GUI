import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {EvaluationJobStatus} from '../../../../core/models/evaluation-job-status-model';
import {JobStatus} from '../../../../core/models/enums/job-status';
import {Router} from '@angular/router';
import {environment} from '../../../../../environments/environment';
import {FilterQuery} from "../../models/filter-query";
import {FilterType} from "../../models/filter-type";

@Component({
  selector: 'app-job-item',
  templateUrl: './job-item.component.html',
  styleUrls: ['./job-item.component.css']
})
export class JobItemComponent implements OnInit {
  @Input('job') item: EvaluationJobStatus;
  @Output() jobDeleted: EventEmitter<EvaluationJobStatus> = new EventEmitter();
  @Output() requestResults: EventEmitter<EvaluationJobStatus> = new EventEmitter();
  @Output() triggerFilter: EventEmitter<FilterQuery> = new EventEmitter<FilterQuery>();
  public showFilterIconModel = false;
  public showFilterIconDataset = false;


  constructor(public router: Router) {
  }

  public get jobStatus(): typeof JobStatus {
    return JobStatus;
  }

  public downloadResults(uid: string): void {
    const url = environment.url + '/results/' + uid + '.zip';
    window.open(url);
  }

  ngOnInit(): void {
  }

  removeJob(): void {
    this.jobDeleted.emit(this.item);
  }

  navigateToResultsPage(): void {
    this.requestResults.emit(this.item);
  }

  triggerFilterForDataset(dataset_name: string) {
    this.triggerFilter.emit({
      filter: FilterType.DATASET,
      value: dataset_name
    })
  }

  triggerFilterForModel(model_name: string) {
    this.triggerFilter.emit({
      filter: FilterType.MODEL,
      value: model_name
    })
  }
}
