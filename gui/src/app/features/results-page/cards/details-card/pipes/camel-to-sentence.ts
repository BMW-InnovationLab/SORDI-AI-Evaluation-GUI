import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
    name: 'camelToSentence'
})
export class CamelToSentence implements PipeTransform {
    transform(value: string): string {
        const formatted = value.replace(/([A-Z])/g, ' $1');
        return formatted.charAt(0).toUpperCase() + formatted.slice(1);
    }
}
