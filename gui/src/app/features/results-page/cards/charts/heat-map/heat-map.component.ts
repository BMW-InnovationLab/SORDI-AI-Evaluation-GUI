import {Component, Input, OnInit, ViewChild} from '@angular/core';

import {
    ApexAxisChartSeries,
    ApexChart,
    ApexDataLabels,
    ApexPlotOptions,
    ApexResponsive,
    ApexStroke,
    ApexTitleSubtitle,
    ApexXAxis,
    ApexYAxis,
    ChartComponent
} from 'ng-apexcharts';
import {GraphResponseModel} from '../../../../../core/models/graph-response-model';

export type ChartOptions = {
    series: ApexAxisChartSeries;
    chart: ApexChart;
    dataLabels: ApexDataLabels;
    title: ApexTitleSubtitle;
    plotOptions: ApexPlotOptions;
    responsive: ApexResponsive[];
    stroke: ApexStroke;
    colors: any;
    xaxis: ApexXAxis;
    yaxis: ApexYAxis;
};

@Component({
    selector: 'app-heat-map',
    templateUrl: './heat-map.component.html',
    styleUrls: ['./heat-map.component.css']
})
export class HeatMapComponent implements OnInit {
    @Input() chartData: GraphResponseModel;
    @ViewChild('chart') chart: ChartComponent;
    public chartOptions: Partial<ChartOptions>;
  showOverlay: any = false;

    ngOnInit(): void {
        this.chartOptions = {
            series: this.formatData(),
            chart: {
                height: 288,
                type: 'heatmap'
            },
            responsive: [
                {
                    breakpoint: 1920,
                    options: {
                        chart: {
                            height: 10
                        }
                    }
                }
            ],
            colors: ['#008ffb'],
            stroke: {
                width: 2,
                colors: ['#008ffb']
            },
            dataLabels: {
                enabled: true,
                style: {
                    colors: ['#4a4a4a']
                }
            },
            title: {
                text: this.chartData.title
            },
            xaxis: {
                title: {
                    text: 'Predicted Labels'
                }
            },
            yaxis: {

                title: {
                    text: 'Predicted Labels'
                }
            },
            plotOptions: {
                heatmap: {
                    colorScale: {
                        ranges: [{
                            from: 0,
                            to: 2,
                            color: '#e3f7ff',
                            name: 'none'
                        }]
                    }
                }
            },
        };
    }

    private formatData(): any {
        const seriesData = [];
        let dataToFormat = this.chartData.series.map(serie => serie.data[0]);
        dataToFormat = dataToFormat.map((_, colIndex) => dataToFormat.map(row => row[colIndex]));
        dataToFormat.forEach(data => data.reverse());
        for (const index in this.chartData.labels) {
            const formattedData = [];
            // tslint:disable-next-line:forin
            for (const preFormat in dataToFormat) {
                formattedData.push({
                    x: this.chartData.labels[preFormat],
                    y: dataToFormat[preFormat][index]
                });
            }
            seriesData.push({
                name: this.chartData.labels[this.chartData.labels.length - 1 - Number(index)],
                data: formattedData
            });
        }
        return seriesData;
    }

  toggleOverlay() {
    this.showOverlay = !this.showOverlay;
  }
}
