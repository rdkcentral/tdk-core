import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditRadioStreamDetailsComponent } from './edit-radio-stream-details.component';

describe('EditRadioStreamDetailsComponent', () => {
  let component: EditRadioStreamDetailsComponent;
  /**
   * The fixture for the EditRadioStreamDetailsComponent.
   * 
   * @remarks
   * This fixture is used for testing the EditRadioStreamDetailsComponent.
   */
  let fixture: ComponentFixture<EditRadioStreamDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditRadioStreamDetailsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EditRadioStreamDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
