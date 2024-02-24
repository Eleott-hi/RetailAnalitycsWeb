// const ssr_host = "http://fastapi:8000/api/v1";
const ssr_host = "http://localhost:8000/api/v1";
const csr_host = "http://localhost:8000/api/v1";

// const AuthorizationHeader = { "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNzA4MzI0MTQ1fQ.q7NB3uOZYawFAKC7iOangu12X6v6tBlHwjpSBGpxzOM" };
const AuthorizationHeader = { "Authorization": "" };

const base_auth_api_url = "/auth";
const base_table_api_url = "/tables";
const base_sql_request_api_url = "/sql-request"
const base_functions_api_url = "/functions";


export function proceedRegistration(formData: Object, on_done: (data: any) => void = () => { }, on_error: (data: any) => void = () => { }) {
    let is_ok = true;
    fetch(csr_host + base_auth_api_url + "/register",
        {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        })
        .then(response => { console.log(response); return response })
        .then(response => { is_ok = response.ok; return response.json(); })
        .then(data => { if (!is_ok) throw data; return data; })
        .then(data => { console.log(data); on_done(data); })
        .catch(error => { console.error(error); on_error(error.detail) });
}


export async function proceedLogin(formData: Object) {
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


function setAuthorizationHeader(token_type: string, access_token: string) {
    localStorage.setItem('token', token_type + " " + access_token);
}

export function clearAuthorizationHeader() {
    localStorage.removeItem('token');
}

export function isLoggedIn() {
    return localStorage.getItem('token') != null;
}

export async function apiGetTablesAsync(on_done: (data: any) => void) {
    const data = await fetch(ssr_host + base_table_api_url,
        {
            method: "GET",
            cache: "no-cache",
            headers: { ...AuthorizationHeader }
        }
    )
    return data.json();
}

export async function apiGetTableAsync(t_name: string) {
    const response = await fetch(ssr_host + base_table_api_url + '/' + t_name,
        {
            method: "GET",
            cache: "no-cache",
            headers: { ...AuthorizationHeader }
        }
    )
    return response.json();
}

export async function apiGetTableColumnsAsync(t_name: string) {
    const response = await fetch(ssr_host + base_table_api_url + '/' + t_name + "/columns",
        {
            method: "GET",
            cache: "no-cache",
            headers: { ...AuthorizationHeader }
        }
    )
    return response.json();
}


export async function apiGetFunctionsAsync() {
    const response = await fetch(ssr_host + base_functions_api_url,
        {
            method: "GET",
            cache: "no-cache",
            headers: { ...AuthorizationHeader }
        }
    )
    return response.json();
}



export function apiGetTable(t_name: string, on_done: (data: any) => void) {
    fetch(csr_host + base_table_api_url + '/' + t_name,
        {
            method: "GET",
            headers: { ...AuthorizationHeader }
        })
        .then(response => response.json())
        .then(data => { console.log(data); on_done(data) })
        .catch(error => console.error('Error fetching tables:', error));
}


export function apiDeleteTable(t_name: string, on_done: CallableFunction) {
    fetch(csr_host + base_table_api_url + '/' + t_name,
        {
            method: "DELETE",
            headers: { ...AuthorizationHeader }
        })
        .then((data) => { console.log(data); return data })
        .then((data) => { console.log(data); on_done(data) })
        .catch(error => console.error('Error deleting tables:', error));
}


export function apiEditItem(t_name: string, id: string, item: any, on_done: (data: any) => void, on_error: (data: any) => void) {
    fetch(csr_host + base_table_api_url + '/' + t_name + "/" + id,
        {
            method: "PUT",
            headers: { ...AuthorizationHeader, 'Content-Type': 'application/json' },
            body: JSON.stringify(item)
        })
        .then(response => { if (response.status !== 200) throw Error("Could not edit item"); return response.json() })
        .then(data => { console.log(data); on_done(data); })
        .catch(error => { console.error('Error editing item:', error); on_error(error) });
}


export function apiCreateItem(t_name: string, item: any, on_done: (data: any) => void, on_error: (data: any) => void) {
    console.log("Creating item", item);
    fetch(csr_host + base_table_api_url + '/' + t_name,
        {
            method: "POST",
            headers: { ...AuthorizationHeader, 'Content-Type': 'application/json' },
            body: JSON.stringify(item)
        })
        .then(response => { if (response.status !== 200) throw Error("Could not create item"); return response.json() })
        .then(data => { console.log(data); on_done(data) })
        .catch(error => { console.error('Error creating item:', error); on_error(error) });
}

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
