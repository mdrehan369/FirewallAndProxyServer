import { IRequest } from "./Request";
import { ISession } from "./Session";

export interface IResponse {
    id: string;
    session_id: string;
    cookies: string;
    headers: string;
    data: string;
    url: string;
    time: string;
    method: string;
    request_id: string;
    request: IRequest;
    session: ISession
}