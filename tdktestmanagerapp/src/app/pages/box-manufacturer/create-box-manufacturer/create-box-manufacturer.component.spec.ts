import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateBoxManufacturerComponent } from './create-box-manufacturer.component';
import { By } from '@angular/platform-browser';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonFormComponent } from '../../../utility/component/common-form/common-form.component';


  describe('CreateBoxManufacturerComponent', () => {
    let component: CreateBoxManufacturerComponent;
    let fixture: ComponentFixture<CreateBoxManufacturerComponent>;
  
    beforeEach(async () => {
      await TestBed.configureTestingModule({
        declarations: [CreateBoxManufacturerComponent, CommonFormComponent],
        imports: [ ReactiveFormsModule ]
      })
      .compileComponents();
      
      // fixture = TestBed.createComponent(CreateBoxManufacturerComponent);
      // component = fixture.componentInstance;
      // fixture.detectChanges();
    });
    beforeEach(() => {
      fixture = TestBed.createComponent(CreateBoxManufacturerComponent);
      component = fixture.componentInstance;
      fixture.detectChanges();
    });
    it("should pass this test case", function() {
      expect(true).toBe(true);
    });
    it('should create', () => {
      expect(component).toBeTruthy();
    });
  
 
    it('should make the name input required', () => {
      const commnFormName = fixture.debugElement.query(By.directive(CommonFormComponent)).componentInstance;
      const control = commnFormName.createUpdateForm.get('name');
      expect(control?.valid).toBeFalsy();
      expect(control?.errors.required).toBeTruthy();
   

      // control.setValue('boManufacturerNameTest');
      // expect(control?.valid).toBeTruthy();


      // control.setValue('');
      // expect(control?.valid).toBeFalsy();
  
    });

  });

  // beforeEach(async () => {
  //   await TestBed.configureTestingModule({
  //     imports: [CreateBoxManufacturerComponent]
  //   })
  //   .compileComponents();
    
  //   const fixture = TestBed.createComponent(CreateBoxManufacturerComponent);
  //   component = fixture.componentInstance;
  //   fixture.detectChanges();
  // });



