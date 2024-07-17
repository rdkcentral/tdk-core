import { TestBed } from '@angular/core/testing';

import { BoxManufactureService } from './box-manufacture.service';

describe('BoxManufactureService', () => {
  let service: BoxManufactureService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BoxManufactureService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
