import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StreamingtemplatesCreateComponent } from './streamingtemplates-create.component';

describe('StreamingtemplatesCreateComponent', () => {
  let component: StreamingtemplatesCreateComponent;
  let fixture: ComponentFixture<StreamingtemplatesCreateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StreamingtemplatesCreateComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(StreamingtemplatesCreateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
