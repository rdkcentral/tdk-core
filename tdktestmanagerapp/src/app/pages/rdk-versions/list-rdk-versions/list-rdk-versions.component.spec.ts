import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListRdkVersionsComponent } from './list-rdk-versions.component';

describe('ListRdkVersionsComponent', () => {
  let component: ListRdkVersionsComponent;
  let fixture: ComponentFixture<ListRdkVersionsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListRdkVersionsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ListRdkVersionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
