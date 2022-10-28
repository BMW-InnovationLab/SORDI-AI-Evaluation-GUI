import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

const routes: Routes = [
    {path: '', pathMatch: 'full', redirectTo: '/jobs'},
    {
        path: 'jobs',
        loadChildren: () => import('./features/jobs-page/jobs-page.module').then(m => m.JobsPageModule)
    },
    {
        path: 'inference-services',
        loadChildren: () => import('./features/inference-service-page/inference-service-page.module')
            .then(m => m.InferenceServicePageModule)
    },
    {
        path: 'start-job',
        loadChildren: () => import('./features/stepper-page/stepper-page.module').then(m => m.StepperPageModule)
    },
    {path: '**', redirectTo: '/jobs', pathMatch: 'full'}
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule {
}
