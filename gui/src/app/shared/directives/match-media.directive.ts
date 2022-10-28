import {Directive, Input, TemplateRef, ViewContainerRef} from "@angular/core";

@Directive({ selector: '[media]' })
export class MatchMediaDirective {
  @Input() set media(query: string) {
    // cleanup old listener
    if (this.removeListener) {
      this.removeListener();
    }
    this.setListener(query);
  }
  private hasView = false;
  private removeListener: () => void;

  constructor(
    private readonly viewContainer: ViewContainerRef,
    private readonly template: TemplateRef<any>
  ) { }

  private setListener(query: string) {
    const mediaQueryList = window.matchMedia(query);
    const listener = event => {
      // create view if true and not created already
      if (event.matches && !this.hasView) {
        this.hasView = true;
        this.viewContainer.createEmbeddedView(this.template);
      }
      // destroy view if false and created
      if (!event.matches && this.hasView) {
        this.hasView = false;
        this.viewContainer.clear();
      }
    };
    // run once and then add listener
    listener(mediaQueryList);
    mediaQueryList.addEventListener('change', listener);
    // add cleanup listener

    this.removeListener = () => mediaQueryList.removeEventListener('change', listener);
  }
}
