import { Component } from '@angular/core';
import { Component1 } from './component1/component1.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'angular';
  component1 = new Component1;
}
