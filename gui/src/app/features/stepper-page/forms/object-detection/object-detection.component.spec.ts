import {ComponentFixture, TestBed} from '@angular/core/testing';

import {ObjectDetectionComponent} from './object-detection.component';

describe('ObjectDetectionComponent', () => {
    let component: ObjectDetectionComponent;
    let fixture: ComponentFixture<ObjectDetectionComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            declarations: [ObjectDetectionComponent]
        })
            .compileComponents();
    });

    beforeEach(() => {
        fixture = TestBed.createComponent(ObjectDetectionComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
