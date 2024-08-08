import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListSocVendorComponent } from './list-soc-vendor.component';

describe('ListSocVendorComponent', () => {
  let component: ListSocVendorComponent;
  let fixture: ComponentFixture<ListSocVendorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListSocVendorComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ListSocVendorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
