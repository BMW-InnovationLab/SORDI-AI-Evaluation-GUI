import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {EvaluationJob} from '../../../../core/models/evaluation-job-model';

@Component({
    selector: 'app-object-detection',
    templateUrl: './object-detection.component.html',
    styleUrls: ['./object-detection.component.css']
})
export class ObjectDetectionComponent implements OnInit {
    public objectDetectionForm: FormGroup;


    constructor(private fb: FormBuilder) {
    }

    ngOnInit(): void {
        this.objectDetectionForm = this.fb.group({
            labelType: ['json', [Validators.required]],
            iouThreshold: [, [Validators.required]],
            averageThreshold: [, [Validators.required, this.validIoU]],
            goodThreshold: [, [Validators.required]],
            confidenceThreshold : [, [Validators.required]]
        });
    }


    public validIoU = (control: FormControl): { [s: string]: boolean } => {
        if (!control.value) {
            return {required: true};
        }
        if (control.value >= this.objectDetectionForm.value.goodThreshold) {
            return {iouValueError: true, error: true};
        }
        return {};
    }

    public validate(): void {
        // tslint:disable-next-line:forin
        for (const key in this.objectDetectionForm.controls) {
            this.objectDetectionForm.controls[key].markAsDirty();
            this.objectDetectionForm.controls[key].updateValueAndValidity();
        }
    }

    public submitForm(): EvaluationJob {
      return  new EvaluationJob(
        '', '', '', '', '', '', 50, '',
        this.objectDetectionForm.value.labelType,
        this.objectDetectionForm.value.iouThreshold,
        this.objectDetectionForm.value.averageThreshold,
        this.objectDetectionForm.value.goodThreshold,
        this.objectDetectionForm.value.confidenceThreshold
      );
    }

    public updateIoUValidator(): any {
        return Promise.resolve().then(() => this.objectDetectionForm.controls.averageThreshold.updateValueAndValidity());
    }
}
