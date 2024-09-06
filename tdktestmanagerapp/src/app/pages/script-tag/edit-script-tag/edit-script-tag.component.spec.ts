import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditScriptTagComponent } from './edit-script-tag.component';

describe('EditScriptTagComponent', () => {
  let component: EditScriptTagComponent;
  let fixture: ComponentFixture<EditScriptTagComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditScriptTagComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EditScriptTagComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
