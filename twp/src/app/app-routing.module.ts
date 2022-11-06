import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { IntradayComponent } from './intraday/intraday.component';
import { FiisComponent } from './fiis/fiis.component';

const routes: Routes = [
  { path: 'intraday-component', component: IntradayComponent },
  { path: 'fiis-component', component: FiisComponent },
];
@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
