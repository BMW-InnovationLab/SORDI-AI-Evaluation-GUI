import {Component, Input, OnInit} from '@angular/core';
import {NavigationEnd, Router} from "@angular/router";
import {filter} from "rxjs/operators";

@Component({
  selector: 'app-title',
  templateUrl: './title.component.html',
  styleUrls: ['./title.component.css']
})
export class TitleComponent implements OnInit {
  @Input() title: string;
  public mobile: boolean;

  public navItems = [
    {icon: 'unordered-list', title: 'Jobs List', routerLink: '/jobs', isSelected: false},
    {icon: 'form', title: 'Evaluate Job', routerLink: '/start-job', isSelected: false},
    {icon: 'cloud', title: 'Inference API Services', routerLink: '/inference-services', isSelected: false},
  ];

  constructor(private router: Router) {
    this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .subscribe((navigation: NavigationEnd) => {
        this.navItems.forEach(navItem => navItem.isSelected = false);
        const active = this.navItems.find(item => navigation.url.includes(item.routerLink));
        if (active) active.isSelected = true;
      });
  }

  ngOnInit(): void {
    this.mobile = window.screen.width < 768;
    window.onresize = () => {
      this.mobile = window.screen.width < 768;
    };
  }
}
