import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

import {ResultsPageComponent} from './results-page.component';

const routes: Routes = [{path: '', component: ResultsPageComponent}];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class ResultsPageRoutingModule {
}
