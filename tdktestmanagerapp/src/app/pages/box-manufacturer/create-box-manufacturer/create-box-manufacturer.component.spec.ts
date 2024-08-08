import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateBoxManufacturerComponent } from './create-box-manufacturer.component';

describe('CreateBoxManufacturerComponent', () => {
  let component: CreateBoxManufacturerComponent;
  let fixture: ComponentFixture<CreateBoxManufacturerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateBoxManufacturerComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CreateBoxManufacturerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
