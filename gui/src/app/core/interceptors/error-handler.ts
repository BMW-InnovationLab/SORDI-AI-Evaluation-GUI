import {HttpErrorResponse, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';
import {Observable, throwError} from 'rxjs';
import {catchError} from 'rxjs/operators';

export class ErrorHandler implements HttpInterceptor {
    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        return next.handle(req).pipe(
            catchError((error: HttpErrorResponse) => {
                let errorMessage = error.error?.detail;
                if (!errorMessage || errorMessage === '' || error.status === 500) {
                    errorMessage = 'An error has occurred';
                }
                return throwError(errorMessage);
            }));
    }
}
