import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {InferenceServicePageRoutingModule} from './inference-service-page-routing.module';
import {InferenceServicePageComponent} from './inference-service-page.component';
import {NzGridModule} from 'ng-zorro-antd/grid';
import {NzCardModule} from 'ng-zorro-antd/card';
import {NzIconModule} from 'ng-zorro-antd/icon';
import {NzButtonModule} from 'ng-zorro-antd/button';
import {NzTagModule} from 'ng-zorro-antd/tag';
import {NzModalModule} from 'ng-zorro-antd/modal';
import {NzFormModule} from 'ng-zorro-antd/form';
import {NzInputModule} from 'ng-zorro-antd/input';
import {NzRadioModule} from 'ng-zorro-antd/radio';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {NzSelectModule} from 'ng-zorro-antd/select';
import {NzToolTipModule} from 'ng-zorro-antd/tooltip';
import {NzCheckboxModule} from 'ng-zorro-antd/checkbox';
import {NzTabsModule} from 'ng-zorro-antd/tabs';
import {ModalAddServiceComponent} from './components/modal-add-service/modal-add-service.component';
import {NzDividerModule} from 'ng-zorro-antd/divider';
import {ModelsPaginationComponent} from './components/models-pagination/models-pagination.component';
import {FormatTextPipe} from './pipes/format-text.pipe';
import {NzPopconfirmModule} from 'ng-zorro-antd/popconfirm';
import {SharedModule} from '../../shared/shared.module';
import {NzSkeletonModule} from 'ng-zorro-antd/skeleton';
import {NzDropDownModule} from 'ng-zorro-antd/dropdown';

@NgModule({
  declarations: [InferenceServicePageComponent, ModalAddServiceComponent, ModelsPaginationComponent, FormatTextPipe],
  imports: [
    CommonModule,
    InferenceServicePageRoutingModule,
    NzGridModule,
    NzCardModule,
    NzIconModule,
    NzButtonModule,
    NzTagModule,
    NzModalModule,
    NzFormModule,
    NzInputModule,
    NzRadioModule,
    FormsModule,
    NzSelectModule,
    NzToolTipModule,
    ReactiveFormsModule,
    NzCheckboxModule,
    NzTabsModule,
    NzDividerModule,
    NzPopconfirmModule,
    SharedModule,
    NzSkeletonModule,
    NzDropDownModule
  ]
})
export class InferenceServicePageModule {
}
