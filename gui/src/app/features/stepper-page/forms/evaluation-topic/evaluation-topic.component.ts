import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {InferenceService} from '../../../../core/models/inference-service.model';
import {InferencePageService} from '../../../../core/services/inference-page.service';
import {EvaluationJob} from '../../../../core/models/evaluation-job-model';
import {datasetTypes, InferenceType} from "../../../../core/models/enums/inference-type";

@Component({
  selector: 'app-evaluation-topic',
  templateUrl: './evaluation-topic.component.html',
  styleUrls: ['./evaluation-topic.component.css']
})
export class EvaluationTopicComponent implements OnInit {
  @Input() datasetName: string;
  @Input() jobType: string;
  @Output() hideObjectDetectionForm: EventEmitter<boolean> = new EventEmitter<boolean>();
  public commonFormFields: FormGroup;
  public mobile: boolean;
  public availableServiceUrls = [];
  public availableModels = [];
  datasetTypes = datasetTypes;

  private allServices: InferenceService[] = [
    new InferenceService(
      'dummy',
      'dummyUrl:4343',
      ['model'],
      InferenceType.OBJECT_DETECTION
    )
  ];


  constructor(private fb: FormBuilder,
              private inferenceJobService: InferencePageService) {
  }


  ngOnInit(): void {
    this.handleScreenResize();
    this.commonFormFields = this.fb.group({
      job_name: ['', [Validators.required]],
      author_name: ['', [Validators.required]],
      batch_size: [50, [Validators.required]],
      service: ['', [Validators.required]],
      model: ['', [Validators.required]],
    });
    this.refresh();
  }

  public validate(): void {
    // tslint:disable-next-line:forin
    for (const key in this.commonFormFields.controls) {
      this.commonFormFields.controls[key].markAsDirty();
      this.commonFormFields.controls[key].updateValueAndValidity();
    }
  }

  public submitForm(): EvaluationJob {
    return new EvaluationJob(
      '',
      this.commonFormFields.value.author_name,
      // value was put as both name and url to identify services with different urls
      this.commonFormFields.value.service.split('|')[1].trim(),
      this.commonFormFields.value.model,
      this.commonFormFields.value.job_name,
      '',
      this.commonFormFields.value.batch_size
    );
  }

  public typeChange(jobType: string): void {
    this.setInferenceServices(jobType);
    this.hideObjectDetectionForm.emit(jobType === 'image_classification');
  }

  public filterModels($event: string): void {
    $event = $event.split('|')[1].trim();
    this.availableModels = this.allServices.filter(item => item.url === $event)[0].models;
  }

  private refresh(): void {
    this.inferenceJobService.getAll()
      .subscribe(data => {
        this.allServices = data;
      });
  }

  private setInferenceServices(requiredType = 'image_classification'): void {
    this.availableServiceUrls = this.allServices
      .filter(inferenceService => inferenceService.inferenceType === requiredType)
      .map(inferenceService => {
        return {
          name: inferenceService.name + ' | ' + inferenceService.url,
          value: inferenceService.name + ' | ' + inferenceService.url
        };
      });
  }

  private handleScreenResize(): void {
    this.mobile = window.screen.width < 768;
    window.onresize = () => {
      this.mobile = window.screen.width < 768;
    };
  }
}
