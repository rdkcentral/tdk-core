import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListBoxtypeComponent } from './list-boxtype.component';

describe('ListBoxtypeComponent', () => {
  let component: ListBoxtypeComponent;
  let fixture: ComponentFixture<ListBoxtypeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListBoxtypeComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ListBoxtypeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
