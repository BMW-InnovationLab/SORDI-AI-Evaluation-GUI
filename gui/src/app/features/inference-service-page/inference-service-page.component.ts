import {Component, OnInit} from '@angular/core';
import {NzMessageService} from 'ng-zorro-antd/message';
import {first} from 'rxjs/operators';
import {InferencePageService} from '../../core/services/inference-page.service';
import {InferenceService} from '../../core/models/inference-service.model';
import {datasetTypes, getInferenceTypeName, InferenceType} from "../../core/models/enums/inference-type";

@Component({
  selector: 'app-inference-service-page',
  templateUrl: './inference-service-page.component.html',
  styleUrls: ['./inference-service-page.component.css']
})
export class InferenceServicePageComponent implements OnInit {
  public mobile = false;
  public inferenceServices: InferenceService[];
  public itemInEditing = false;
  public modifying = false;
  public modalSettings = {
    isVisible: false,
    adding: false
  };
  public tagValue: InferenceType;
  public modifyIconType = 'save';
  public loading = true;
  getInferenceTypeName = getInferenceTypeName;
  datasetTypes = datasetTypes;
  private initialServiceContent: InferenceService = this.initializeService();
  private editedServiceContent: InferenceService;

  constructor(
    private inferenceJobService: InferencePageService,
    private message: NzMessageService) {
  }

  ngOnInit(): void {
    this.refreshContent();
    this.mobile = window.screen.width <= 375;
    window.onresize = () => {
      this.mobile = window.screen.width <= 375;
    };
  }

  public addNewService(service: InferenceService): void {
    this.inferenceJobService.post(service)
      .pipe(first())
      .subscribe((_) => {
        this.modalSettings.isVisible = false;
        this.modalSettings.adding = false;
        this.inferenceServices.push(service);
        this.refreshContent();
      }, error => {
        this.modalSettings.isVisible = false;
        this.modalSettings.adding = false;
        this.message.create('error', error, {nzPauseOnHover: true, nzDuration: 3500});
      });
  }

  public showModal(): void {
    this.modalSettings.isVisible = !this.modalSettings.isVisible;
  }

  public removeService(index: number): void {
    const uuidToDelete = this.inferenceServices[index].uuid;
    this.inferenceJobService.delete(uuidToDelete);
    this.inferenceJobService.delete(uuidToDelete).subscribe(() => {
      this.inferenceServices.splice(index, 1);
    }, error => {
      this.message.create('error', error, {nzPauseOnHover: true, nzDuration: 3500});
    });
  }

  public editService(index): void {
    if (!this.itemInEditing) {
      const inEditing = this.inferenceServices[index];
      this.itemInEditing = true;
      this.inferenceServices[index].editable = true;
      this.initialServiceContent = new InferenceService(
        inEditing.name,
        inEditing.url,
        inEditing.models,
        inEditing.inferenceType,
        inEditing.uuid,
        true,
        inEditing.discoverModels
      );
      this.editedServiceContent = this.inferenceServices[index];
      this.tagValue = inEditing.inferenceType;
    }
  }

  public saveChanges(index: number): void {
    if (this.modifying) {
      return;
    }
    this.modifyIconType = 'loading';
    this.itemInEditing = false;
    this.getChanges(index);
    this.inferenceJobService.put(this.editedServiceContent).subscribe(() => {
      this.modifying = false;
      this.modifyIconType = 'save';
      this.modifyCardContent(index, this.editedServiceContent);
      this.refreshContent();
    }, error => {
      this.message.create('error', error, {nzPauseOnHover: true, nzDuration: 2500});
      this.modifyIconType = 'save';
      this.inferenceServices[index] = this.initialServiceContent;
      this.modifying = false;
    });
  }

  public cancelChanges(index: number): void {
    this.modifyIconType = 'save';
    this.itemInEditing = false;
    this.modifyCardContent(index, this.initialServiceContent);
  }

  public getChanges(index: number): void {
    this.editedServiceContent.name = document.getElementById('name' + index).innerText;
    this.editedServiceContent.inferenceType = this.tagValue;
    this.editedServiceContent.url = document.getElementById('url' + index).innerText;
  }

  public addModelToItem(item: InferenceService, value: string): void {
    item.models.push(value);
  }

  public refreshService(item: InferenceService) {
    const modifiedItem = {...item};
    modifiedItem.discoverModels = true;
    item.refreshing = true;
    this.inferenceJobService.put(modifiedItem).subscribe((updated) => {
      this.refreshContent();
      item.refreshing = false;
      item = updated;
    }, _ => {
      item.refreshing = false;
      this.message.create('error', 'Could not refresh service ' + item.name,
        {nzPauseOnHover: true, nzDuration: 2500});
    });
  }

  private refreshContent(): void {
    this.inferenceJobService.getAll().subscribe((data) => {
      this.inferenceServices = data;
      this.loading = false;
    });
  }

  private initializeService(): InferenceService {
    return new InferenceService(
      '',
      '',
      [],
      InferenceType.OBJECT_DETECTION,
      '',
    );
  }

  private modifyCardContent(index: number, newContent: InferenceService): void {
    newContent.editable = false;
    this.inferenceServices[index] = new InferenceService(
      newContent.name,
      newContent.url,
      newContent.models,
      newContent.inferenceType,
      newContent.uuid,
      false,
      newContent.discoverModels
    );
  }
}
