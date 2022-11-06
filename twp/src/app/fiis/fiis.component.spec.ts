import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FiisComponent } from './fiis.component';

describe('FiisComponent', () => {
  let component: FiisComponent;
  let fixture: ComponentFixture<FiisComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FiisComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FiisComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
