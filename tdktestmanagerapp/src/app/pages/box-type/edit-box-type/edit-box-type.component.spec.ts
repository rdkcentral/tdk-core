import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditBoxTypeComponent } from './edit-box-type.component';

describe('EditBoxTypeComponent', () => {
  let component: EditBoxTypeComponent;
  let fixture: ComponentFixture<EditBoxTypeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditBoxTypeComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EditBoxTypeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
