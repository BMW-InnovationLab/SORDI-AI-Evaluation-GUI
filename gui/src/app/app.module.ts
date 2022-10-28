import {NgModule} from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';

import {AppComponent} from './app.component';
import {AppRoutingModule} from './app-routing.module';
import {IconsProviderModule} from './icons-provider.module';
import {NzLayoutModule} from 'ng-zorro-antd/layout';
import {NzMenuModule} from 'ng-zorro-antd/menu';
import {HTTP_INTERCEPTORS, HttpClientModule} from '@angular/common/http';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {en_US, NZ_I18N} from 'ng-zorro-antd/i18n';
import {CommonModule, registerLocaleData} from '@angular/common';
import en from '@angular/common/locales/en';
import {NzDividerModule} from 'ng-zorro-antd/divider';
import {NzTabsModule} from 'ng-zorro-antd/tabs';
import {NzButtonModule} from 'ng-zorro-antd/button';
import {NzMessageModule} from 'ng-zorro-antd/message';
import {ErrorHandler} from './core/interceptors/error-handler';
import {NzEmptyModule} from 'ng-zorro-antd/empty';
import {SideNavComponent} from './core/components/side-nav/side-nav.component';
import {BrowserModule} from '@angular/platform-browser';
import {RouterModule} from '@angular/router';
import {NzBackTopModule} from "ng-zorro-antd/back-top";
import {SharedModule} from "./shared/shared.module";


registerLocaleData(en);

@NgModule({
    declarations: [
        AppComponent,
        SideNavComponent
    ],
  imports: [
    AppRoutingModule,
    RouterModule,
    BrowserModule,
    IconsProviderModule,
    NzLayoutModule,
    NzMenuModule,
    HttpClientModule,
    BrowserAnimationsModule,
    NzDividerModule,
    NzTabsModule,
    NzButtonModule,
    NzMessageModule,
    FormsModule,
    ReactiveFormsModule,
    CommonModule,
    NzEmptyModule,
    NzBackTopModule,
    SharedModule,
  ],
    providers: [
        {
            provide: NZ_I18N, useValue: en_US
        },
        {
            provide: HTTP_INTERCEPTORS,
            useClass: ErrorHandler,
            multi: true
        }
    ],
    exports: [SideNavComponent],
    bootstrap: [AppComponent]
})
export class AppModule {
}
