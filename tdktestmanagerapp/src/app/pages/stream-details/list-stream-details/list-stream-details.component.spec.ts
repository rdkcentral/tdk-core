import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListStreamDetailsComponent } from './list-stream-details.component';

describe('ListStreamDetailsComponent', () => {
  let component: ListStreamDetailsComponent;
  /**
   * The fixture for the ListStreamDetailsComponent.
   */
  let fixture: ComponentFixture<ListStreamDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListStreamDetailsComponent]
    })
      .compileComponents();

    fixture = TestBed.createComponent(ListStreamDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
