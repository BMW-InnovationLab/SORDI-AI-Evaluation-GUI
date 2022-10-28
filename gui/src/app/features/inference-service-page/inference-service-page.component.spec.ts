import {ComponentFixture, TestBed} from '@angular/core/testing';

import {InferenceServicePageComponent} from './inference-service-page.component';

describe('InferenceServicePageComponent', () => {
    let component: InferenceServicePageComponent;
    let fixture: ComponentFixture<InferenceServicePageComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [InferenceServicePageComponent]
        })
            .compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(InferenceServicePageComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
