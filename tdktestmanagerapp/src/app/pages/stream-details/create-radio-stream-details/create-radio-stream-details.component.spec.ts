import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateRadioStreamDetailsComponent } from './create-radio-stream-details.component';

describe('CreateRadioStreamDetailsComponent', () => {
  let component: CreateRadioStreamDetailsComponent;
  /**
   * The fixture for the CreateRadioStreamDetailsComponent.
   */
  let fixture: ComponentFixture<CreateRadioStreamDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateRadioStreamDetailsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CreateRadioStreamDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
