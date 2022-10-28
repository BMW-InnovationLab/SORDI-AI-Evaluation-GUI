import {ComponentFixture, TestBed} from '@angular/core/testing';

import {ModelsPaginationComponent} from './models-pagination.component';

describe('ModelsPaginationComponent', () => {
    let component: ModelsPaginationComponent;
    let fixture: ComponentFixture<ModelsPaginationComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [ModelsPaginationComponent]
        })
            .compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(ModelsPaginationComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
