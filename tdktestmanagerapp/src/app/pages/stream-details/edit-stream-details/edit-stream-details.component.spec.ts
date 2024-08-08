import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditStreamDetailsComponent } from './edit-stream-details.component';

describe('EditStreamDetailsComponent', () => {
  let component: EditStreamDetailsComponent;
  let fixture: ComponentFixture<EditStreamDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditStreamDetailsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EditStreamDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
