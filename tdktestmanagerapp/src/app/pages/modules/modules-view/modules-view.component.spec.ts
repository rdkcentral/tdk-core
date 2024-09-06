import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModulesViewComponent } from './modules-view.component';

describe('ModulesViewComponent', () => {
  let component: ModulesViewComponent;
  let fixture: ComponentFixture<ModulesViewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ModulesViewComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ModulesViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
