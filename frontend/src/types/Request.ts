import { IResponse } from "./Response";
import { ISession } from "./Session";

export interface IRequest {
    id: string;
    session_id: string;
    cookies: string;
    headers: string;
    data: string;
    url: string;
    time: string;
    method: string;
    response: IResponse
    session: ISession
}