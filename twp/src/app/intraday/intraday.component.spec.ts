import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IntradayComponent } from './intraday.component';

describe('IntradayComponent', () => {
  let component: IntradayComponent;
  let fixture: ComponentFixture<IntradayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ IntradayComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(IntradayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
