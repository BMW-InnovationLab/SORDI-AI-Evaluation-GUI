import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {JobsPageRoutingModule} from './jobs-page-routing.module';
import {JobsPageComponent} from './jobs-page.component';
import {NzLayoutModule} from 'ng-zorro-antd/layout';
import {NzListModule} from 'ng-zorro-antd/list';
import {NzCardModule} from 'ng-zorro-antd/card';
import {NzGridModule} from 'ng-zorro-antd/grid';
import {NzPaginationModule} from 'ng-zorro-antd/pagination';
import {NzIconModule} from 'ng-zorro-antd/icon';
import {NzTagModule} from 'ng-zorro-antd/tag';
import {NzButtonModule} from 'ng-zorro-antd/button';
import {NzDropDownModule} from 'ng-zorro-antd/dropdown';
import {SharedModule} from '../../shared/shared.module';
import {JobItemComponent} from './components/job-item/job-item.component';
import {NzInputModule} from 'ng-zorro-antd/input';
import {FormsModule} from '@angular/forms';
import {SearchComponent} from './components/search/search.component';
import {NzSelectModule} from 'ng-zorro-antd/select';
import {NzFormModule} from 'ng-zorro-antd/form';
import {NzCheckboxModule} from 'ng-zorro-antd/checkbox';
import {NzProgressModule} from 'ng-zorro-antd/progress';
import {NzPopconfirmModule} from "ng-zorro-antd/popconfirm";
import {NzDrawerModule} from "ng-zorro-antd/drawer";
import {NzDescriptionsModule} from "ng-zorro-antd/descriptions";
import {NzDividerModule} from "ng-zorro-antd/divider";
import {NzToolTipModule} from "ng-zorro-antd/tooltip";


@NgModule({
  declarations: [JobsPageComponent, JobItemComponent, SearchComponent],
    imports: [
        CommonModule,
        JobsPageRoutingModule,
        NzLayoutModule,
        NzListModule,
        NzCardModule,
        NzGridModule,
        NzPaginationModule,
        NzIconModule,
        NzTagModule,
        NzButtonModule,
        NzDropDownModule,
        SharedModule,
        NzInputModule,
        FormsModule,
        NzSelectModule,
        NzFormModule,
        NzCheckboxModule,
        NzProgressModule,
        NzPopconfirmModule,
        NzDrawerModule,
        NzDescriptionsModule,
        NzDividerModule,
        NzToolTipModule,
    ]
})
export class JobsPageModule {
}
