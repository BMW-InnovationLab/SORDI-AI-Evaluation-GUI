export interface AdapterInterface<T> {
    adaptToUi(item: any): T;

    adaptToRequest(item: T): any;
}
