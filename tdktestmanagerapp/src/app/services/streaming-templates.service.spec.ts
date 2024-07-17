import { TestBed } from '@angular/core/testing';

import { StreamingTemplatesService } from './streaming-templates.service';

describe('StreamingTemplatesService', () => {
  let service: StreamingTemplatesService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(StreamingTemplatesService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
