import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StreamingtemplatesListComponent } from './streamingtemplates-list.component';

describe('StreamingtemplatesListComponent', () => {
  let component: StreamingtemplatesListComponent;
  let fixture: ComponentFixture<StreamingtemplatesListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StreamingtemplatesListComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(StreamingtemplatesListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
