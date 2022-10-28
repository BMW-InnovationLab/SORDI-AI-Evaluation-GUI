import {Component, Input, OnChanges, OnInit} from '@angular/core';

@Component({
    selector: 'app-models-pagination',
    templateUrl: './models-pagination.component.html',
    styleUrls: ['./models-pagination.component.css']
})
export class ModelsPaginationComponent implements OnInit, OnChanges {
    @Input() models: string[] = [];
    public pageSize: number;
    public currentPage: number;
    public totalPages: number;
    public modelsDisplayed: string[] = [];

    constructor() {
    }

    ngOnInit(): void {
        this.currentPage = 1;
        this.setPageSettings();
        window.onresize = () => {
            this.setPageSettings();
        };
    }

    ngOnChanges(): void {
        this.setPageSettings();
    }

    private setPageSettings(): void {
        const windowWidth = window.screen.width;
        if (windowWidth <= 500) {
            this.pageSize = 2;
        } else if (windowWidth < 700) {
            this.pageSize = 4;
        } else if (windowWidth <= 1160) {
            this.pageSize = 4;
        } else {
            this.pageSize = 3;
        }

        this.totalPages = Math.ceil(this.models.length / this.pageSize);
        this.refresh();
    }

    private refresh(): void {
        this.modelsDisplayed = [...this.models]
            .splice((this.currentPage - 1) * this.pageSize, this.pageSize);
    }

    public previous(): any {
        if (this.currentPage > 1) {
            this.currentPage--;
            this.refresh();
        }
    }

    public next(): void {
        if (this.currentPage < this.pageSize) {
            this.currentPage += 1;
            this.refresh();
        }
    }
}
