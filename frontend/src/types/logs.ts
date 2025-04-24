export interface ILog {
  method: string;
  url: string;
  cookies: string;
  headers: string;
  data: string;
  system_ip: string;
  type: "Response" | "Request";
  time: string;
}
