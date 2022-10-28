import {
  AfterContentInit,
  Component,
  EventEmitter,
  Input,
  OnChanges,
  Output,
  SimpleChanges,
  ViewChild
} from '@angular/core';
import {EvaluationJobStatus} from '../../../../core/models/evaluation-job-status-model';
import {JobStatus} from '../../../../core/models/enums/job-status';
import {getKeywords} from "../../helpers";
import {NzSelectComponent} from "ng-zorro-antd/select";

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements AfterContentInit, OnChanges {
  @Input() jobs: EvaluationJobStatus[] = [];
  @Output() filterResults: EventEmitter<EvaluationJobStatus[]> = new EventEmitter<EvaluationJobStatus[]>();

  public searchQuery: string;
  private _filterQuery = {
    model: [],
    dataset: [],
    statusFiltersOptions: [
      {label: 'Done Jobs', value: JobStatus.Done, checked: true},
      {label: 'Evaluating Jobs', value: JobStatus.InProgress, checked: true},
    ]
  };
  public models: string[] = [];
  public datasets: string[] = [];


  get filterQuery(): { statusFiltersOptions: ({ checked: boolean; label: string; value: JobStatus })[]; model: any[]; dataset: any[] } {
    return this._filterQuery;
  }

  set filterQuery(value: { statusFiltersOptions: ({ checked: boolean; label: string; value: JobStatus })[]; model: any[]; dataset: any[] }) {
    this._filterQuery = value;
    this.filter();
  }

  constructor() {
  }

  ngAfterContentInit(): void {
    this.initData();
  }

  public refreshFilter(jobs: EvaluationJobStatus[]): EvaluationJobStatus[] {
    // todo remove after websockets
    this.jobs = jobs;
    this.initData();
    return this.filter();
  }

  public filter(): EvaluationJobStatus[] {
    const results = this.matchFilters();
    this.filterResults.emit(results);
    return results;
  }

  public initData(): void {
    this.models = [...new Set(this.jobs.map(job => job.model_name))];
    this.datasets = [...new Set(this.jobs.map(job => job.dataset_name))];
  }

  public checkStatusValues($event: any[]) {
    // console.log($event);
    this.filter();
  }

  ngOnChanges(changes: SimpleChanges): void {
    this.initData();
    this.search();
  }

  public search() {
    if (this.searchQuery == '' || !this.searchQuery) {
      const res = this.matchFilters();
      this.filterResults.emit(res);
      return res;
    }
    const keywords = getKeywords(this.searchQuery);
    const nameMatches = this.matchFilters()
      .filter(job => {
        for (let keyword of keywords) {
          if (job.job_name.includes(keyword))
            return true;
        }
        return false;
      });
    this.filterResults.emit(nameMatches);
    return nameMatches;
  }

  private matchFilters(): EvaluationJobStatus[] {
    return this.jobs.filter(job => {
      // if (this.filterQuery.model.length) console.log(this.filterQuery.model);
      const matches: boolean[] = [];
      const statusMatch: boolean[] = [];
      if (this._filterQuery.model.length) matches.push(this._filterQuery.model.includes(job.model_name));
      if (this._filterQuery.dataset.length) matches.push(this._filterQuery.dataset.includes(job.dataset_name));// && console.log(this.filterQuery.dataset.includes(job.dataset_name));
      if (this._filterQuery.statusFiltersOptions[0].checked) statusMatch.push(job.status == JobStatus.Done);
      if (this._filterQuery.statusFiltersOptions[1].checked) statusMatch.push(job.status == JobStatus.InProgress);

      return matches.every(value => value) && statusMatch.some(value => value);
    });
  }

  public clipOption(item: string) {
    return (item.length > 15)? item.substr(0, 14) + "..." : item;
  }
}
