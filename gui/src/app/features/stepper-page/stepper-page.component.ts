import {Component, OnInit, ViewChild} from '@angular/core';
import {Router} from '@angular/router';
import {EvaluationTopicComponent} from './forms/evaluation-topic/evaluation-topic.component';
import {ObjectDetectionComponent} from './forms/object-detection/object-detection.component';
import {NzMessageService} from 'ng-zorro-antd/message';
import {first} from 'rxjs/operators';
import {ChooseDatasetComponent} from './forms/choose-dataset/choose-dataset.component';
import {JobsPageService} from '../../core/services/jobs-page.service';
import {EvaluationJob} from '../../core/models/evaluation-job-model';
import {DatasetInformation} from '../../core/models/dataset-information';
import {getInferenceTypeName, InferenceType} from '../../core/models/enums/inference-type';

@Component({
  selector: 'app-stepper-page',
  templateUrl: './stepper-page.component.html',
  styleUrls: ['./stepper-page.component.css']
})
export class StepperPageComponent implements OnInit {
  @ViewChild(ChooseDatasetComponent) datasetComponent: ChooseDatasetComponent;
  @ViewChild(EvaluationTopicComponent) evaluationTopic: EvaluationTopicComponent;
  @ViewChild(ObjectDetectionComponent) objectDetection: ObjectDetectionComponent;
  public objectDetectionHidden = true;
  public submitDisabled = false;
  public current: number;
  public nextButtonLoading = false;
  inferenceTypeName = getInferenceTypeName;


  constructor(private router: Router,
              private evaluationJobService: JobsPageService,
              private message: NzMessageService) {
  }

  ngOnInit(): void {
    this.current = 0;
  }

  public done(): void {
    this.router.navigate(['jobs']);
  }

  public submitForm(): void {
    this.evaluationTopic.validate();
    if (this.objectDetectionHidden) {
      this.submitClassificationForm();
    } else {
      this.objectDetection.validate();
      this.submitObjectDetectionForm();
    }
  }

  public toggleFields($event: boolean): void {
    this.objectDetectionHidden = $event;
  }

  public next(): void {
    if (this.datasetComponent.validate()) {
      this.current++;
      this.evaluationTopic.typeChange(this.getDataset().type);
    }
  }

  public goBack(): void {
    this.current--;
  }

  getDataset(): DatasetInformation {
    if (this.datasetComponent) {
      const form = Object.assign(this.datasetComponent.datasetForm.value);
      return form.datasetName || '';
    }
    return {name: '', type: InferenceType.IMAGE_CLASSIFICATION};
  }

  public changeNextButtonStatus($event: 'loading' | 'done'): void {
    this.nextButtonLoading = ($event === 'loading');
  }

  private submitClassificationForm(): void {
    if (this.evaluationTopic.commonFormFields.valid) {
      const newEvaluationJob: EvaluationJob = {
        ...this.evaluationTopic.submitForm(),
        ...this.datasetComponent.datasetForm.value.name
      };
      newEvaluationJob.datasetName = this.getDataset().name;
      newEvaluationJob.jobType = this.getDataset().type;
      this.sendPost(newEvaluationJob);
    }
  }

  private submitObjectDetectionForm(): void {
    if (!this.evaluationTopic.commonFormFields.valid || !this.objectDetection.objectDetectionForm.valid) {
      return;
    }

    const {
      labelsType,
      iouThreshold,
      iouAverageThreshold,
      iouGoodThreshold,
      confidenceThreshold,
      ...baseValues
    } = this.evaluationTopic.submitForm();
    const newEvaluationJob: EvaluationJob = {
      ...this.objectDetection.submitForm(),
      ...baseValues,
      ...this.datasetComponent.datasetForm.value
    };
    // todo update in choose dataset
    newEvaluationJob.datasetName = this.getDataset().name;
    newEvaluationJob.jobType = this.getDataset().type;
    this.sendPost(newEvaluationJob);
  }

  private sendPost(newJob: EvaluationJob): void {
    this.submitDisabled = true;
    this.evaluationJobService.post(newJob)
      .pipe(first())
      .subscribe((res: EvaluationJob) => {
          setTimeout(() => {
            this.router.navigate(['/jobs']);
          }, 1000);
        },
        error => {
          this.submitDisabled = false;
          this.message.create('error', error, {nzPauseOnHover: true, nzDuration: 2500});
        });
  }
}
