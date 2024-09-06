import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateRdkVersionsComponent } from './create-rdk-versions.component';

describe('CreateRdkVersionsComponent', () => {
  let component: CreateRdkVersionsComponent;
  let fixture: ComponentFixture<CreateRdkVersionsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateRdkVersionsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CreateRdkVersionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
