import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateStreamDetailsComponent } from './create-stream-details.component';

describe('CreateStreamDetailsComponent', () => {
  let component: CreateStreamDetailsComponent;
  /**
   * The fixture for the CreateStreamDetailsComponent.
   */
  let fixture: ComponentFixture<CreateStreamDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateStreamDetailsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CreateStreamDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
