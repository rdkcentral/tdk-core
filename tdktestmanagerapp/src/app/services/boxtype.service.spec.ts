import { TestBed } from '@angular/core/testing';

import { BoxtypeService } from './boxtype.service';

describe('BoxtypeService', () => {
  let service: BoxtypeService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BoxtypeService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
