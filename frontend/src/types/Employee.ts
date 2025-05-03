import { ISession } from "./Session";

export enum Role {
    Frontend_Developer="Frontend Developer",
    Backend_Developer="Backend Developer",
    Full_Stack_Developer="Full Stack Developer",
    DevOps_Engineer="DevOps Engineer",
    Mobile_App_Developer="Mobile App Developer",
    QA_Engineer="QA Engineer",
    Machine_Learning_Engineer="Machine Learning Engineer",
    Data_Engineer="Data Engineer",
    Security_Engineer="Security Engineer",
    Site_Reliability_Engineer="Site Reliability Engineer",
    Cloud_Engineer="Cloud Engineer",
    Software_Architect="Software Architect",
    Game_Developer="Game Developer",
    Embedded_Systems_Engineer="Embedded Systems Engineer",
    Software_Engineer="Software Engineer"
}

export interface IEmployee {
  id: string;
  corporate_id: string;
  corporate_password: string;
  fullname: string;
  role: Role;
  email: string;
  joined_at: string;

  sessions: ISession[]
}
