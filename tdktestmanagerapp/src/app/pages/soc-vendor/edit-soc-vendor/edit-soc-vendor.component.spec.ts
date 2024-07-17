import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditSocVendorComponent } from './edit-soc-vendor.component';

describe('EditSocVendorComponent', () => {
  let component: EditSocVendorComponent;
  let fixture: ComponentFixture<EditSocVendorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditSocVendorComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EditSocVendorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
