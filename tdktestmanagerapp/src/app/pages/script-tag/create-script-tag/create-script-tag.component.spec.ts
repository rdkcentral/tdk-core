import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateScriptTagComponent } from './create-script-tag.component';

describe('CreateScriptTagComponent', () => {
  let component: CreateScriptTagComponent;
  let fixture: ComponentFixture<CreateScriptTagComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateScriptTagComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CreateScriptTagComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
