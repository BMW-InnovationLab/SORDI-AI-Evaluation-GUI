import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
    name: 'formatText'
})
export class FormatTextPipe implements PipeTransform {
    transform(value: string): string {
        return value.length >= 10 ? value.substring(0, 9) + '...' : value;
    }
}
