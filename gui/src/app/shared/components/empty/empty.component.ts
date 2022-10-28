import {Component} from '@angular/core';
import {Router} from '@angular/router';

@Component({
    selector: 'app-empty',
    templateUrl: './empty.component.html',
    styleUrls: ['./empty.component.css']
})
export class EmptyComponent {

    constructor(public router: Router) {
    }

    public gotoJobsPage(): void {
        this.router.navigate(['/start-job']);
    }
}
