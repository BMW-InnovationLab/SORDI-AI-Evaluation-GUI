import {AfterContentInit, Component, OnInit} from '@angular/core';
import {NavigationEnd, Router} from '@angular/router';
import {filter} from 'rxjs/operators';

@Component({
  selector: 'app-side-nav',
  templateUrl: './side-nav.component.html',
  styleUrls: ['./side-nav.component.css'],
})
export class SideNavComponent implements OnInit, AfterContentInit{
  public isCollapsed = true;
  public mobile = false;

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
    this.mobile = window.screen.width <= 1024;
    window.onresize = () => {
      this.mobile = window.screen.width <= 1024;
    };
  }

  ngAfterContentInit() {
    this.isCollapsed=true;
  }

  toggleMenu() {
    this.isCollapsed = !this.isCollapsed;
  }
}
