

import { ssr_host, csr_host, getAuthorizationHeader } from "./Common";

const functions_api_endpoint = "/functions";


export async function apiGetFunctionsAsync() {
    const response = await fetch(ssr_host + functions_api_endpoint,
        {
            method: "GET",
            cache: "no-cache",
            headers: { ...getAuthorizationHeader() },
        }
    )

    console.log("apiGetFunctionsAsync response:", response);
    if (!response.ok) { throw "Functions not found"; }

    const data = await response.json();
    console.log("apiGetFunctionsAsync data:", data);

    return data;
}


export async function apiGetFunctionInfoAsync(f_name: string) {
    const response = await fetch(`${csr_host}${functions_api_endpoint}/${f_name}/info`,
        {
            method: "GET",
            cache: "no-cache",
            headers: { ...getAuthorizationHeader() },
        }
    )

    console.log("apiGetFunctionInfoAsync response:", response);
    if (!response.ok) { throw "Tables not found"; }

    const data = await response.json();
    console.log("apiGetFunctionInfoAsync data:", data);

    return data;
}

export async function apiExecuteFunctionAsync(f_name: string, params: any) {
    const response = await fetch(`${csr_host}${functions_api_endpoint}/${f_name}?${new URLSearchParams(params)}`,
        {
            method: "GET",
            cache: "no-cache",
            headers: { ...getAuthorizationHeader() },
        }
    )

    console.log("apiExecuteFunctionAsync response:", response);
    if (!response.ok) { throw "Tables not found"; }

    const data = await response.json();
    console.log("apiExecuteFunctionAsync data:", data);

    return data;
}

