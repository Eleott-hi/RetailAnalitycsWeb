import { toCamelCase } from "@/components/Utils";

// const ssr_host = "http://fastapi:8000/api/v1";
const ssr_host = "http://localhost:8000/api/v1";
const csr_host = "http://localhost:8000/api/v1";

// const AuthorizationHeader = { "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNzA4MzI0MTQ1fQ.q7NB3uOZYawFAKC7iOangu12X6v6tBlHwjpSBGpxzOM" };
const AuthorizationHeader = { "Authorization": "" };

const base_auth_api_url = "/auth";
const graphql_api_url = "/graphql";
const base_table_api_url = "/tables";
const base_sql_request_api_url = "/sql-request"
const base_functions_api_url = "/functions";


function getBearerToken() {
    if (typeof window === 'undefined') return "";
    return localStorage.getItem('token') || "";
}

function getAuthorizationHeader() {
    return { "Authorization": "Bearer " + getBearerToken() };
}

export function setBearerToken(access_token: string) {
    if (typeof window === 'undefined') return;
    localStorage.setItem('token', access_token);
}

export function clearBearerToken() {
    if (typeof window === 'undefined') return;
    localStorage.removeItem('token');
}

export function apiImportTable(t_name: string, table: any[], on_done: (data: any) => void) {
    fetch(csr_host + base_table_api_url + '/' + t_name + "/import",
        {
            method: "POST",
            headers: { ...AuthorizationHeader, 'Content-Type': 'application/json' },
            body: JSON.stringify(table)
        })
        .then(data => { console.log(data); on_done(data); })
        .catch(error => console.error('Error importing table:', error));
}

