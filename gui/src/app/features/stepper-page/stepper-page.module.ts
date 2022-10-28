import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';

import {StepperPageRoutingModule} from './stepper-page-routing.module';
import {StepperPageComponent} from './stepper-page.component';
import {NzStepsModule} from 'ng-zorro-antd/steps';
import {NzButtonModule} from 'ng-zorro-antd/button';
import {NzCardModule} from 'ng-zorro-antd/card';
import {EvaluationTopicComponent} from './forms/evaluation-topic/evaluation-topic.component';
import {NzFormModule} from 'ng-zorro-antd/form';
import {NzSelectModule} from 'ng-zorro-antd/select';
import {NzInputModule} from 'ng-zorro-antd/input';
import {NzRadioModule} from 'ng-zorro-antd/radio';
import {NzCheckboxModule} from 'ng-zorro-antd/checkbox';
import {ObjectDetectionComponent} from './forms/object-detection/object-detection.component';
import {NzInputNumberModule} from 'ng-zorro-antd/input-number';
import {NzToolTipModule} from 'ng-zorro-antd/tooltip';
import {NzUploadModule} from 'ng-zorro-antd/upload';
import {NzIconModule} from 'ng-zorro-antd/icon';
import {ChooseDatasetComponent} from './forms/choose-dataset/choose-dataset.component';
import {DragDropModule} from '@angular/cdk/drag-drop';
import {SharedModule} from '../../shared/shared.module';
import {NzProgressModule} from 'ng-zorro-antd/progress';
import {NzTreeSelectModule} from "ng-zorro-antd/tree-select";
import {NzDescriptionsModule} from "ng-zorro-antd/descriptions";

@NgModule({
    declarations: [
        StepperPageComponent,
        EvaluationTopicComponent,
        ObjectDetectionComponent,
        ChooseDatasetComponent,
    ],
    imports: [
        CommonModule,
        StepperPageRoutingModule,
        NzStepsModule,
        NzButtonModule,
        NzCardModule,
        FormsModule,
        ReactiveFormsModule,
        NzFormModule,
        NzSelectModule,
        NzInputModule,
        NzRadioModule,
        NzCheckboxModule,
        NzInputNumberModule,
        NzToolTipModule,
        NzUploadModule,
        NzIconModule,
        DragDropModule,
        SharedModule,
        NzProgressModule,
        NzTreeSelectModule,
        NzDescriptionsModule,
    ]
})
export class StepperPageModule {
}
