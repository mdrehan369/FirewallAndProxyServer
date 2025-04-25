"use client";

import { IRequest } from "@/types/Request";
import { Badge } from "../ui/badge";
import { IResponse } from "@/types/Response";
import { formatDateTime } from "@/utils/formatDatetime";
import { convertToObject } from "@/utils/convertToObject";
import CopyBox from "../CopyBox";

export default function ShowLogDetails(apiResponse: IRequest | IResponse) {
  const headers = convertToObject(apiResponse.headers, "__n__", ":");
  const cookies = convertToObject(apiResponse.cookies, "__n__", ":");

  return (
    <div className="flex flex-col items-start justify-start gap-3">
      <code className="text-2xl font-bold text-gray-200 my-3 bg-white/10 p-2 rounded-md">
        {apiResponse.url}
      </code>
      <div className="flex items-center justify-start gap-2">
        <Badge className="bg-purple-600 font-bold">#{apiResponse.id}</Badge>
        <Badge className="bg-green-600 font-bold">{apiResponse.method}</Badge>
        <Badge className="bg-yellow-600 font-bold">
          {apiResponse.session.system_ip}
        </Badge>
        <Badge className="bg-blue-400 font-bold">
          {formatDateTime(apiResponse.time)}
        </Badge>
      </div>
      <div>
        <h3 className="text-xl font-bold">Headers</h3>
        <CopyBox copyText={apiResponse.headers}>
          {Object.keys(headers).map((header) => (
            <div key={header}>
              <code className="text-red-400">{header.toUpperCase()}</code>
              {" : "}
              <code className="">{headers[header]}</code>
            </div>
          ))}
        </CopyBox>
      </div>

      <div>
        <h3 className="text-xl font-bold">Cookies</h3>
        <CopyBox copyText={apiResponse.cookies}>
          {Object.keys(cookies).map((cookie) => (
            <div key={cookie}>
              <code className="text-red-400">{cookie.toUpperCase()}</code>
              {" : "}
              <code className="">{cookies[cookie]}</code>
            </div>
          ))}
        </CopyBox>
      </div>

      <div>
        <h3 className="text-xl font-bold">Employee Details</h3>
        <CopyBox copyText={JSON.stringify(apiResponse.session.employee)}>
          <div>
            <code className="text-red-400">CORPORATE ID</code>
            {" : "}
            <code>{apiResponse.session.employee["corporate_id"]}</code>
          </div>

          <div>
            <code className="text-red-400">FULLNAME</code>
            {" : "}
            <code>{apiResponse.session.employee["fullname"]}</code>
          </div>

          <div>
            <code className="text-red-400">EMAIL</code>
            {" : "}
            <code>{apiResponse.session.employee["email"]}</code>
          </div>

          <div>
            <code className="text-red-400">Role</code>
            {" : "}
            <code>{apiResponse.session.employee["role"]}</code>
          </div>
        </CopyBox>
      </div>

      <div>
        <h3 className="text-xl font-bold">Session Details</h3>
        <CopyBox copyText={JSON.stringify(apiResponse.session)}>
          <div>
            <code className="text-red-400">SESSION ID</code>
            {" : "}
            <code>#{apiResponse.session.id}</code>
          </div>

          <div>
            <code className="text-red-400">LOGGED IN AT</code>
            {" : "}
            <code>{formatDateTime(apiResponse.session["loggedin_at"])}</code>
          </div>

          <div>
            <code className="text-red-400">LOGGED OUT AT</code>
            {" : "}
            <code>{apiResponse.session["did_logged_out"] ? formatDateTime(apiResponse.session["loggedout_at"]) : "Not Yet!"}</code>
          </div>

          <div>
            <code className="text-red-400">SYSTEM IP</code>
            {" : "}
            <code>{apiResponse.session["system_ip"]}</code>
          </div>
        </CopyBox>
      </div>
    </div>
  );
}
