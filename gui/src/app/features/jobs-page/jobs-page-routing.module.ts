import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

import {JobsPageComponent} from './jobs-page.component';

const routes: Routes = [
    {path: '', component: JobsPageComponent},
    {path: 'results/:uid', loadChildren: () => import('../results-page/results-page.module').then(m => m.ResultsPageModule)}

];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class JobsPageRoutingModule {
}
