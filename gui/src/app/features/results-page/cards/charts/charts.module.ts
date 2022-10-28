import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {HeatMapComponent} from './heat-map/heat-map.component';
import {HistogramComponent} from './histogram/histogram.component';
import {PieChartComponent} from './pie-chart/pie-chart.component';
import {ScatterChartComponent} from './scatter-chart/scatter-chart.component';
import {NgApexchartsModule} from 'ng-apexcharts';
import {NzModalModule} from "ng-zorro-antd/modal";


@NgModule({
    declarations: [
        HeatMapComponent,
        HistogramComponent,
        PieChartComponent,
        ScatterChartComponent
    ],
    imports: [
        CommonModule,
        NgApexchartsModule,
        NzModalModule
    ],
    exports: [
        HeatMapComponent,
        HistogramComponent,
        PieChartComponent,
        ScatterChartComponent
    ]
})
export class ChartsModule {
}
