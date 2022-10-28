import {Component, EventEmitter, NgZone, OnInit, Output} from '@angular/core';
import {NzUploadChangeParam, NzUploadXHRArgs, UploadFilter} from 'ng-zorro-antd/upload';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {Subscription} from 'rxjs';
import {NzMessageService} from 'ng-zorro-antd/message';
import {InferencePageService} from '../../../../core/services/inference-page.service';
import {JobsPageService} from '../../../../core/services/jobs-page.service';
import {DatasetsService} from '../../../../core/services/datasets-service.service';
import {filter, tap} from 'rxjs/operators';
import {HttpEvent, HttpEventType, HttpResponse} from '@angular/common/http';
import {DatasetInformation} from "../../../../core/models/dataset-information";
import {getInferenceTypeName} from "../../../../core/models/enums/inference-type";

@Component({
  selector: 'app-choose-dataset',
  templateUrl: './choose-dataset.component.html',
  styleUrls: ['./choose-dataset.component.css'],
})
export class ChooseDatasetComponent implements OnInit {
  @Output() uploadStatusChanged: EventEmitter<'loading' | 'done'> = new EventEmitter<'loading' | 'done'>();
  public progress: number = 0;
  public uploadSettings = {
    percentage: 0,
    status: 'active'
  };
  public datasetForm: FormGroup;
  public disableDatasetField = false;
  public availableDatasets = ['dummy_dataset'];
  public nzDatasetTree = [];
  private readonly ALLOWED_UPLOADS = ['application/x-zip-compressed', 'application/zip'];
  public filterUploads: UploadFilter[] = [
    {
      name: 'get-type',
      fn: (fileList) => {
        // since only one file can be uploaded at a time checking the first is enough
        if (!this.ALLOWED_UPLOADS.includes(fileList[0].type)) {
          this.message.error('Only zip files are allowed.');
        }
        return fileList.filter(file => this.ALLOWED_UPLOADS.includes(file.type));
      }
    }
  ];

  constructor(private fb: FormBuilder,
              private inferenceJobService: InferencePageService,
              private jobsServices: JobsPageService,
              private datasetService: DatasetsService,
              private message: NzMessageService,
              private zone: NgZone) {
  }

  ngOnInit(): void {
    this.datasetForm = this.fb.group({
      datasetName: ['', [Validators.required]]
    });
    this.refresh();
  }

  public uploadDataset = (toUpload: NzUploadXHRArgs): Subscription => {
    this.uploadSettings.status = 'active';
    const formData = new FormData();
    formData.append('filename', toUpload.file.filename);
    formData.append('content_type', 'application/zip');
    formData.append('dataset', toUpload.file as any);
    return this.datasetService.upload(formData).pipe(tap((event: HttpEvent<any>) => {
      if (event.type === HttpEventType.UploadProgress) {
        this.zone.run(() => {
          this.progress = Math.round((100 * event.loaded) / event.total);
          this.uploadSettings = {...this.uploadSettings};
          toUpload.file.percent = this.uploadSettings.percentage;
        });
      }
    })).pipe(filter(event => event instanceof HttpResponse))
      .subscribe((event) => {
        toUpload.onSuccess(event.body, toUpload.file, event);
        this.disableDatasetField = true;
        this.uploadSettings.percentage = 0;
        this.uploadSettings.status = 'success';
        this.datasetForm.controls.datasetName.setValue(event.body);
      }, err => {
        toUpload.onError(err, toUpload.file);
        this.uploadSettings.percentage = 0;
        this.uploadSettings.status = 'exception';
      });
  }

  public validate(): boolean {
    // tslint:disable-next-line:forin
    for (const key in this.datasetForm.controls) {
      this.datasetForm.controls[key].markAsDirty();
      this.datasetForm.controls[key].updateValueAndValidity();
    }

    return this.datasetForm.valid;
  }

  public handleChange(fileInfo: NzUploadChangeParam): void {
    const status = fileInfo.file.status;
    if (status === 'uploading') {
      this.uploadStatusChanged.emit('loading');
    }
    if (status === 'removed' && fileInfo.fileList.length === 0) {
      // make dataset name required again
      this.disableDatasetField = false;
      this.uploadSettings.status = 'active';
      this.progress = 0;
      this.refresh();
    }
    if (status === 'done') {
      const formData = new FormData();
      this.uploadStatusChanged.emit('done');
      formData.append('uploaded_dataset', fileInfo.file as any);
    }
    if (status === 'error') {
      this.uploadStatusChanged.emit('done');
    }
  }

  datasetNodeClicked(node: any, $event) {
    if (!node.isLeaf) {
      node.isSelectable = false;
      node.isExpanded = !node.isExpanded;
      $event.stopPropagation();
      $event.preventDefault();
    }
  }

  private refresh(): void {
    this.datasetService.getAvailableDatasets()
      .subscribe((data: DatasetInformation[]) => {
        // this.availableDatasets = data;
        this.nzDatasetTree = [];
        const types = [...new Set(data.map(dataset => dataset.type))];
        types.forEach(type => {
          const children = data.filter(dataset => dataset.type == type)
            .map(dataset => {
              return {
                title: dataset.name,
                key: dataset,
                isLeaf: true
              }
            });
          this.nzDatasetTree.push({
            title: getInferenceTypeName(type),
            children: children
          });
        })
      });
  }
}
