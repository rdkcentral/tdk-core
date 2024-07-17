import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateBoxtypeComponent } from './create-boxtype.component';

describe('CreateBoxtypeComponent', () => {
  let component: CreateBoxtypeComponent;
  let fixture: ComponentFixture<CreateBoxtypeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateBoxtypeComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CreateBoxtypeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
