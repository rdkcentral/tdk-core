import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditRdkVersionsComponent } from './edit-rdk-versions.component';

describe('EditRdkVersionsComponent', () => {
  let component: EditRdkVersionsComponent;
  let fixture: ComponentFixture<EditRdkVersionsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditRdkVersionsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EditRdkVersionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
