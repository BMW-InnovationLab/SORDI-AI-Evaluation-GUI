import {Component, EventEmitter, Input, OnChanges, OnInit, Output} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {InferenceService} from '../../../../core/models/inference-service.model';
import {SelectionShape} from '../../../../core/models/selection-shape';
import {InferenceType} from "../../../../core/models/enums/inference-type";

@Component({
    selector: 'app-modal-add-service',
    templateUrl: './modal-add-service.component.html',
    styleUrls: ['./modal-add-service.component.css']
})
export class ModalAddServiceComponent implements OnInit, OnChanges {
    @Input() readonly datasetTypes: SelectionShape[];
    @Output() newServiceAdded: EventEmitter<InferenceService> = new EventEmitter<InferenceService>();
    public inferenceForm: FormGroup;
    @Input() settings = {
        isVisible: false,
        adding: false
    };
    public input: InferenceService;
    models = ['model'];


    ngOnChanges(): void {
        // detect change in isVisible
        this.resetForm();
    }

    constructor(private fb: FormBuilder) {
    }

    ngOnInit(): void {
        this.prepareForm();
        this.toggleModelsValidator();
    }

    private prepareForm(): void {
        this.resetForm();

        this.inferenceForm = this.fb.group({
            serviceName: [this.input.name, [Validators.required]],
            url: [this.input.url, [Validators.required]],
            modelsList: [[], [Validators.required]],
            datasetType: ['object_detection', [Validators.required]],
            discoverModels: [this.input.discoverModels]
        });
        for (const i in this.inferenceForm.controls) {
            this.inferenceForm.controls[i].markAsPristine();
        }
    }

    private resetForm(): void {
        this.input = new InferenceService(
            '',
            '',
            [],
            InferenceType.IMAGE_CLASSIFICATION,
            '',
        );

    }

    private isFormValid(): boolean {
        for (const i in this.inferenceForm.controls) {
            this.inferenceForm.controls[i].markAsDirty();
            this.inferenceForm.controls[i].updateValueAndValidity();
        }
        return this.inferenceForm.valid;
    }

    handleOk(): void {
        if (this.isFormValid()) {
            const service = new InferenceService(
                this.inferenceForm.value.serviceName,
                this.inferenceForm.value.url,
                [],
                this.inferenceForm.value.datasetType
            );
            service.discoverModels = this.inferenceForm.value.discoverModels;
            if (!service.discoverModels) {
                service.models = this.inferenceForm.value.modelsList;
            }
            this.settings.adding = true;
            this.newServiceAdded.emit(service);
        }
    }


    handleCancel(): void {
        this.settings.isVisible = false;
    }

    toggleModelsValidator(): void {
        if (!this.inferenceForm.value.discoverModels) {
            this.inferenceForm.controls.modelsList.setValidators(Validators.required);
        } else {
            this.inferenceForm.controls.modelsList.clearValidators();
        }
    }
}
