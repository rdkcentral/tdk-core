import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListScriptTagComponent } from './list-script-tag.component';

describe('ListScriptTagComponent', () => {
  let component: ListScriptTagComponent;
  let fixture: ComponentFixture<ListScriptTagComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListScriptTagComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ListScriptTagComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
