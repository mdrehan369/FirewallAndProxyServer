import { IEmployee } from "./Employee";
import { IRequest } from "./Request";
import { IResponse } from "./Response";

export interface ISession {
    id: string;
    employee_corporate_id: string;
    loggedin_at: string;
    loggedout_at: string;
    did_logged_out: string;
    system_ip: string;

    employee: IEmployee
    requests: IRequest[]
    responses: IResponse[]
}