import {Component, ElementRef, Input, OnInit, ViewChild} from '@angular/core';
import {Definitions, getDefinitions} from "../definitions";
import {animate, style, transition, trigger} from "@angular/animations";

@Component({
  selector: 'app-help',
  templateUrl: './help.component.html',
  styleUrls: ['./help.component.css'],
  animations: [
    trigger(
      'showHideDefinitionsAnimation',
      [
        transition(
          ':enter',
          [
            style({
              height: 0,
              width: 0,
              opacity: 0,
            }),
            animate('0.4s ease-in-out',
              style({height: '60vh', width: '30vw', opacity: 1}))
          ]
        ),
        transition(
          ':leave',
          [
            style({height: '60vh', width: '30vw', opacity: 1}),
            animate('0.4s ease',
              style({height: 0, width: 0, opacity: 0}))
          ]
        )
      ]
    )
  ]
})
export class HelpComponent implements OnInit {
  @Input() jobType: 'object_detection' | 'image_classification';
  @ViewChild('definitionsContainer') definitionsContainer: ElementRef;
  public definitions: Definitions[] = [];
  public showDefinitions: boolean = false;

  constructor() {
  }


  ngOnInit(): void {
    this.definitions = getDefinitions(this.jobType);

  }

  toggleDefinitions() {
    this.showDefinitions = !this.showDefinitions;
    // console.log(this.showDefinitions)
  }
}
