import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

import {InferenceServicePageComponent} from './inference-service-page.component';

const routes: Routes = [{path: '', component: InferenceServicePageComponent}];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class InferenceServicePageRoutingModule {
}
