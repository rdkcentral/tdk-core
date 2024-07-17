import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditBoxManufacturerComponent } from './edit-box-manufacturer.component';

describe('EditBoxManufacturerComponent', () => {
  let component: EditBoxManufacturerComponent;
  let fixture: ComponentFixture<EditBoxManufacturerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditBoxManufacturerComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EditBoxManufacturerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
