import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StreamingtemplatesEditComponent } from './streamingtemplates-edit.component';

describe('StreamingtemplatesEditComponent', () => {
  let component: StreamingtemplatesEditComponent;
  let fixture: ComponentFixture<StreamingtemplatesEditComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StreamingtemplatesEditComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(StreamingtemplatesEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
