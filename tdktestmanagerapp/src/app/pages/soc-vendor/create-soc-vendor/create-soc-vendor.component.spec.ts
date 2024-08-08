import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateSocVendorComponent } from './create-soc-vendor.component';

describe('CreateSocVendorComponent', () => {
  let component: CreateSocVendorComponent;
  let fixture: ComponentFixture<CreateSocVendorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateSocVendorComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CreateSocVendorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
