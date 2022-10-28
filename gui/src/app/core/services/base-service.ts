import {Observable} from 'rxjs';


export abstract class BaseService<T> {
    abstract getAll(): Observable<T[]>;

    abstract post(item: T): Observable<T>;

    abstract put(item: T): Observable<any>;

    abstract delete(id: string): Observable<any>;
}
