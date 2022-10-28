import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {EmptyComponent} from './components/empty/empty.component';
import {NzEmptyModule} from 'ng-zorro-antd/empty';
import {NzButtonModule} from 'ng-zorro-antd/button';
import {NzIconModule} from 'ng-zorro-antd/icon';
import { TitleComponent } from './components/title/title.component';
import {NzLayoutModule} from 'ng-zorro-antd/layout';
import {NzDividerModule} from 'ng-zorro-antd/divider';
import {NzMenuModule} from 'ng-zorro-antd/menu';
import {RouterModule} from '@angular/router';
import { LayoutComponent } from './components/layout/layout.component';
import {MatchMediaDirective} from './directives/match-media.directive';
import {NzDropDownModule} from "ng-zorro-antd/dropdown";
import { HelpComponent } from './components/help/help.component';
import {NzPopoverModule} from "ng-zorro-antd/popover";
import {NzDescriptionsModule} from "ng-zorro-antd/descriptions";

@NgModule({
    declarations: [EmptyComponent, TitleComponent, LayoutComponent, MatchMediaDirective, HelpComponent],
    imports: [
        CommonModule,
        NzEmptyModule,
        NzButtonModule,
        NzIconModule,
        NzLayoutModule,
        NzDividerModule,
        NzMenuModule,
        RouterModule,
        NzDropDownModule,
        NzPopoverModule,
        NzDescriptionsModule,
    ],
  exports: [EmptyComponent, TitleComponent, MatchMediaDirective, LayoutComponent, HelpComponent]
})
export class SharedModule {
}
