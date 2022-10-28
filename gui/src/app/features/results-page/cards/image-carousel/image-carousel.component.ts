import {Component, Input, OnInit, ViewChild} from '@angular/core';
import {NzCarouselComponent} from 'ng-zorro-antd/carousel';
import {NzImage, NzImageService} from "ng-zorro-antd/image";

@Component({
  selector: 'app-image-carousel',
  templateUrl: './image-carousel.component.html',
  styleUrls: ['./image-carousel.component.css']
})
export class ImageCarouselComponent implements OnInit {
  @ViewChild(NzCarouselComponent, {static:false}) carousel: NzCarouselComponent;

  @Input() source: {
    url: string,
    perLabel: boolean
  };
  public images = [];
  public noImagesFound = false;
  private errorCount = 0;

  constructor(private nzImageService: NzImageService) {
  }

  ngOnInit(): void {
    this.errorCount = 0;
    this.loadImages();
  }

  loadImages(): void {
    for (const index of [1, 2, 3]) {
      this.images.push(this.source.url + index + '.png');
    }
  }

  removeImage(index: number): string {
    this.images.splice(index, 1);
    if (++this.errorCount === 3) {
      this.errorCount = 0;
      // this.source.perLabel = false;
      this.noImagesFound = true;
    }
    return 'removed';
  }

  previewCarousel(image: any) {
    const nzImages: NzImage[] = [{
      src: image,
      alt: 'Could not load.'
    }];
    nzImages.push(...this.images.filter(image_=>image!=image_)
        .map(image => {
      return {src: image}
    }));
    this.nzImageService.preview(nzImages);
  }
}
