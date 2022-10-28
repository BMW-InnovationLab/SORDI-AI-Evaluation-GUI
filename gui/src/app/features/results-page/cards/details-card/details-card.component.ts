import {Component, Input, OnInit} from '@angular/core';
import {EvaluationJob} from '../../../../core/models/evaluation-job-model';

@Component({
    selector: 'app-details-card',
    templateUrl: './details-card.component.html',
    styleUrls: ['./details-card.component.css']
})
export class DetailsCardComponent implements OnInit {
    @Input() evaluationJobDetails: EvaluationJob;
    public listItems: string[][] = [];

    constructor() {
    }

    ngOnInit(): void {
        const {uid, jobName, labelsType, ...toDisplay} = this.evaluationJobDetails;
        if (this.evaluationJobDetails.jobType === 'image_classification') {
            const {iouThreshold, iouAverageThreshold, iouGoodThreshold, ...classificationSpecific} = toDisplay;
            this.listItems = Object.keys(classificationSpecific).map(key => [key, classificationSpecific[key]]);
        } else {
            this.listItems = Object.keys(toDisplay).map(key => [key, toDisplay[key]]);
        }
    }

}
