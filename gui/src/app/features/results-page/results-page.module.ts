import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {ResultsPageRoutingModule} from './results-page-routing.module';
import {ResultsPageComponent} from './results-page.component';
import {NzCardModule} from 'ng-zorro-antd/card';
import {NzGridModule} from 'ng-zorro-antd/grid';
import {ImageCarouselComponent} from './cards/image-carousel/image-carousel.component';
import {NzCarouselModule} from 'ng-zorro-antd/carousel';
import {ChartsModule} from './cards/charts/charts.module';
import {DetailsCardComponent} from './cards/details-card/details-card.component';
import {NzListModule} from 'ng-zorro-antd/list';
import {NzSpinModule} from 'ng-zorro-antd/spin';
import {CamelToSentence} from './cards/details-card/pipes/camel-to-sentence';
import {SharedModule} from '../../shared/shared.module';
import {NzTabsModule} from 'ng-zorro-antd/tabs';
import {NzDividerModule} from 'ng-zorro-antd/divider';
import {NzLayoutModule} from 'ng-zorro-antd/layout';
import {NzIconModule} from 'ng-zorro-antd/icon';
import {NzWaveModule} from 'ng-zorro-antd/core/wave';
import {NzButtonModule} from 'ng-zorro-antd/button';
import {NzTypographyModule} from "ng-zorro-antd/typography";
import {NzImageModule} from "ng-zorro-antd/image";
import { OverlayComponent } from './components/overlay/overlay.component';
import {NzDescriptionsModule} from "ng-zorro-antd/descriptions";
import {NzProgressModule} from "ng-zorro-antd/progress";
import {NzStatisticModule} from "ng-zorro-antd/statistic";

@NgModule({
  declarations: [
    ResultsPageComponent,
    ImageCarouselComponent,
    DetailsCardComponent,
    CamelToSentence,
    OverlayComponent
  ],
    imports: [
        CommonModule,
        ResultsPageRoutingModule,
        NzCardModule,
        NzGridModule,
        NzCarouselModule,
        ChartsModule,
        NzListModule,
        NzSpinModule,
        SharedModule,
        NzTabsModule,
        NzDividerModule,
        NzLayoutModule,
        NzIconModule,
        NzWaveModule,
        NzButtonModule,
        NzTypographyModule,
        NzImageModule,
        NzDescriptionsModule,
        NzProgressModule,
        NzStatisticModule
    ]
})
export class ResultsPageModule {
}
