import { ISession } from "./Session";

export enum Role {
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "DevOps Engineer",
    "Mobile App Developer",
    "QA Engineer",
    "Machine Learning Engineer",
    "Data Engineer",
    "Security Engineer",
    "Site Reliability Engineer",
    "Cloud Engineer",
    "Software Architect",
    "Game Developer",
    "Embedded Systems Engineer",
    "Software Engineer"
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
