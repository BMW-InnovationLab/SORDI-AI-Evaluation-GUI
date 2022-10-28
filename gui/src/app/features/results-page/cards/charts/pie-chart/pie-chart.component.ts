import {Component, Input, OnInit, ViewChild} from '@angular/core';
import {ApexChart, ApexNonAxisChartSeries, ApexResponsive, ApexTitleSubtitle, ChartComponent} from 'ng-apexcharts';
import {GraphResponseModel} from '../../../../../core/models/graph-response-model';

export type ChartOptions = {
    series: ApexNonAxisChartSeries;
    chart: ApexChart;
    title: ApexTitleSubtitle;
    responsive: ApexResponsive[];
    labels: any;
};


@Component({
    selector: 'app-pie-chart',
    templateUrl: './pie-chart.component.html',
    styleUrls: ['./pie-chart.component.css']
})
export class PieChartComponent implements OnInit {
    @Input() chartData: GraphResponseModel;
    @ViewChild('chart') chart: ChartComponent;
    public chartOptions: Partial<ChartOptions>;
    showOverlay: boolean = false;

    constructor() {

    }

    private formatLabel(labels: string[]): string[] {
        const formatted = [];
        labels.forEach(label => {
            switch (label) {
                case 'TP':
                    formatted.push('True Positive');
                    break;
                case 'TN':
                    formatted.push('True Negative');
                    break;
                case 'FP':
                    formatted.push('False Positive');
                    break;
                case 'FN':
                    formatted.push('False Negative');
                    break;
                default:
                    formatted.push(label);
            }
        });

        return formatted;
    }

    ngOnInit(): void {
        this.chartOptions = {
            series: this.chartData.series,
            labels: this.formatLabel(this.chartData.labels),
            chart: {
                height: 288,
                type: 'pie'
            },
            responsive: [
                {
                    breakpoint: 1920,
                    options: {
                        chart: {
                            height: 362
                        },
                        legend: {
                            position: 'bottom'
                        }
                    }
                },
                {
                    breakpoint: 768,
                    options: {
                        chart: {
                            height: 320
                        },
                    }
                },
            ],
            title: {
                text: this.chartData.title
            }
        };
    }
  toggleOverlay() {
    this.showOverlay = !this.showOverlay;
  }
}
