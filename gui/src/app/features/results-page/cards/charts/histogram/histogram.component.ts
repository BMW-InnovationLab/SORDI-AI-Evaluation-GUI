import {Component, Input, OnInit, ViewChild} from '@angular/core';
import {
    ApexAxisChartSeries,
    ApexChart,
    ApexDataLabels,
    ApexFill,
    ApexLegend,
    ApexPlotOptions,
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
    plotOptions: ApexPlotOptions;
    title: ApexTitleSubtitle;
    yaxis: ApexYAxis;
    xaxis: ApexXAxis;
    fill: ApexFill;
    // tooltip: ApexTooltip;
    stroke: ApexStroke;
    legend: ApexLegend;
};

@Component({
    selector: 'app-histogram',
    templateUrl: './histogram.component.html',
    styleUrls: ['./histogram.component.css']
})
export class HistogramComponent implements OnInit {
    @Input() chartData: GraphResponseModel;
    @ViewChild('chart') chart: ChartComponent;
    public chartOptions: Partial<ChartOptions>;
  showOverlay: any = false;

    constructor() {
    }

    ngOnInit(): void {
        const seriesData = this.chartData.series.map(item => {
            function getColor(name: string): string {
                switch (name) {
                    case 'bad_iou':
                        return '#FF4560';
                    case 'average_iou':
                        return '#008ffb';
                    case 'good_iou':
                        return '#00e396';
                }
            }

            const formatted = [];
            for (const index in item.data) {
                formatted.push({
                    x: item.bins[index],
                    y: item.data[index],
                    fillColor: getColor(item.name)
                });
            }
            return {
                name: item.name,
                color: getColor(item.name),
                data: formatted
            };
        });

        const bins = this.chartData.series.map(item => item.bins);

        this.chartOptions = {
            series: seriesData,
            chart: {
                type: 'bar',
                // changed the height from 350 to 288
                height: 315
            },
            title: {
                text: this.chartData.title,
                align: 'center'
            },
            plotOptions: {
                bar: {
                    dataLabels: {
                        position: 'top'
                    },
                    horizontal: false,
                    columnWidth: '70%',
                    endingShape: 'rounded'
                }
            },
            dataLabels: {
                enabled: true,
                offsetY: -20,
                style: {
                    colors: ['#4a4a4a']
                }
            },
            stroke: {
                show: true,
                width: 2
            },
            xaxis: {
                type: 'numeric',
                categories: bins,
                title: {
                    text: this.chartData.labels[0]
                },
            },
            yaxis: {
                title: {
                    text: this.chartData.labels[1]
                }
            },
            fill: {
                opacity: 0.95
            },

        };
    }
  toggleOverlay() {
    this.showOverlay = !this.showOverlay;
  }

}
