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


export async function proceedRegistrationAsync(formData: Object, on_done: (data: any) => void = () => { }, on_error: (data: any) => void = () => { }) {
    let is_ok = true;
    const response = await fetch(csr_host + base_auth_api_url + "/register",
        {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

    const data = await response.json();

    if (!response.ok) throw data.detail;

    return data;
}


export async function proceedLoginAsync(formData: Object) {
    console.log(formData);
    const response = await fetch(csr_host + base_auth_api_url + "/login",
        {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

    const data = await response.json();


    if (!response.ok) throw data.detail;

    return data
}

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




export async function apiGetFunctionsAsync() {
    const response = await fetch(ssr_host + base_functions_api_url,
        {
            method: "GET",
            cache: "no-cache",
            headers: { ...AuthorizationHeader }
        }
    )

    console.log("apiGetFunctionsAsync response:", response);
    if (!response.ok) {
        throw "Functions not found";
    }

    const data = await response.json();
    console.log("apiGetFunctionsAsync data:", data);

    return data;
}


// export function apiEditItem(t_name: string, id: string, item: any, on_done: (data: any) => void, on_error: (data: any) => void) {
//     fetch(csr_host + base_table_api_url + '/' + t_name + "/" + id,
//         {
//             method: "PUT",
//             headers: { ...AuthorizationHeader, 'Content-Type': 'application/json' },
//             body: JSON.stringify(item)
//         })
//         .then(response => { if (response.status !== 200) throw Error("Could not edit item"); return response.json() })
//         .then(data => { console.log(data); on_done(data); })
//         .catch(error => { console.error('Error editing item:', error); on_error(error) });
// }


// export function apiCreateItem(t_name: string, item: any, on_done: (data: any) => void, on_error: (data: any) => void) {
//     console.log("Creating item", item);
//     fetch(csr_host + base_table_api_url + '/' + t_name,
//         {
//             method: "POST",
//             headers: { ...AuthorizationHeader, 'Content-Type': 'application/json' },
//             body: JSON.stringify(item)
//         })
//         .then(response => { if (response.status !== 200) throw Error("Could not create item"); return response.json() })
//         .then(data => { console.log(data); on_done(data) })
//         .catch(error => { console.error('Error creating item:', error); on_error(error) });
// }

export function apiDeleteItem(t_name: string, id: string, on_done: (data: any) => void) {
    fetch(csr_host + base_table_api_url + '/' + t_name + "/" + id,
        {
            method: "DELETE",
            headers: { ...AuthorizationHeader }
        })
        .then((data) => { console.log(data); on_done(data) })
        .catch(error => console.error('Error deleting item:', error));
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


export function apiGetFunctionInfo(f_name: string, on_done: (data: any) => void) {
    fetch(csr_host + base_functions_api_url + "/" + f_name,
        {
            method: "GET",
            headers: { ...AuthorizationHeader }
        })
        .then(response => response.json())
        .then(data => { console.log(data); on_done(data); })
        .catch(error => console.error('Error fetching function info:', error));
}

export function apiExecuteFunction(f_name: string, params: any, on_done: (data: any) => void, on_error: (data: any) => void) {
    fetch(csr_host + base_functions_api_url + "/" + f_name + "/execute",
        {
            method: "POST",
            headers: { ...AuthorizationHeader, 'Content-Type': 'application/json' },
            body: JSON.stringify(params),
        })
        .then(response => { if (response.status !== 200) throw Error("Could not execute function"); return response.json() })
        .then(data => { console.log(data); on_done(data); })
        .catch(error => { console.error('Error fetching tables:', error); on_error(error) });
}

export function apiSendSqlRequest(sqlRequest: string, on_done: (data: any) => void, on_error: (data: any) => void) {
    fetch(csr_host + base_sql_request_api_url + `?request=${sqlRequest}`,
        {
            method: "GET",
            headers: { ...AuthorizationHeader }
        })
        .then(response => { console.log(response); return response })
        .then(response => { if (response.status !== 200) throw Error("Could not execute function"); return response.json() })
        .then(on_done)
        .catch(error => { console.error('Error fetching sql request:', error); on_error(error) });
}
