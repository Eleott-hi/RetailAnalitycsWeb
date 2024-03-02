import { csr_host, ssr_host, getAuthorizationHeader } from "./Common";

const register_api_endpoint = "/auth/register";
const login_api_endpoint = "/auth/login";
const islogged_api_endpoint = "/auth/islogged";

export async function apiRegisterAsync(formData: Object) {
    const response = await fetch(csr_host + register_api_endpoint,
        {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

    console.log("apiRegisterAsync response:", response);
    const data = await response.json();

    console.log("apiRegisterAsync data:", data);
    if (!response.ok) throw data.detail;

    return data;
}


export async function apiLoginAsync(formData: Object) {
    console.log(formData);
    const response = await fetch(csr_host + login_api_endpoint,
        {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

    console.log("apiLoginAsync response:", response);
    const data = await response.json();


    console.log("apiLoginAsync data:", data);
    if (!response.ok) throw data.detail;

    return data
}

export async function apiIsLoggedIn() {

    const response = await fetch(csr_host + islogged_api_endpoint,
        {
            method: "GET",
            headers: { ...getAuthorizationHeader() },
        });

    console.log("apiIsLoggedIn response:", response);
    if (response.status === 401) return false;
    return true;

}

