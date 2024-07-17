import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListBoxManufacturerComponent } from './list-box-manufacturer.component';

describe('ListBoxManufacturerComponent', () => {
  let component: ListBoxManufacturerComponent;
  let fixture: ComponentFixture<ListBoxManufacturerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListBoxManufacturerComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ListBoxManufacturerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
