import { TestBed } from '@angular/core/testing';

import { SocVendorService } from './soc-vendor.service';

describe('SocVendorService', () => {
  let service: SocVendorService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SocVendorService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});