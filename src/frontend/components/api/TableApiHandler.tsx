import { ssr_host, csr_host, getAuthorizationHeader } from "./Common";

const graphql_api_url = "/graphql";

export async function apiGetTablesAsync() {
    const response = await fetch(ssr_host + graphql_api_url,
        {
            method: "POST",
            cache: "no-cache",
            headers: { "Content-Type": "application/json", ...getAuthorizationHeader() },
            body: JSON.stringify({ query: "{ tables }" })
        }
    )

    console.log("apiGetTablesAsync response:", response);
    if (!response.ok) { throw "Tables not found"; }

    const data = await response.json();
    console.log("apiGetTablesAsync data:", data);

    return data.data.tables;
}

export async function apiGetTableFieldsAsync(t_name: string) {
    const response = await fetch(ssr_host + graphql_api_url,
        {
            method: "POST",
            cache: "no-cache",
            headers: { "Content-Type": "application/json", ...getAuthorizationHeader() },
            body: JSON.stringify({ query: `{ table_fields(t_name: "${t_name}") }` })
        }
    )


    console.log("apiGetTableFieldsAsync response:", response);
    if (!response.ok) { throw "Error fetching table's fields"; }

    const data = await response.json();
    console.log("apiGetTableFieldsAsync data:", data);

    return data.data.table_fields;
}


export async function apiGetTableAsync(t_name: string) {
    const t_fields = (await apiGetTableFieldsAsync(t_name));

    const response = await fetch(ssr_host + graphql_api_url,
        {
            method: "POST",
            cache: "no-cache",
            headers: { "Content-Type": "application/json", ...getAuthorizationHeader() },
            body: JSON.stringify({ query: `{ table_all(t_name: "${t_name}") { ... on ${t_name} { ${t_fields} } } }` })
        }
    )

    console.log("apiGetTableAsync response:", response);
    if (!response.ok) { throw "Table not found"; }

    const table = (await response.json()).data.table_all;
    console.log("apiGetTableAsync data:", table);

    return [table, t_fields];
}

export async function apiDeleteTableAsync(t_name: string) {
    const response = await fetch(csr_host + graphql_api_url,
        {
            method: "POST",
            headers: { 'Content-Type': 'application/json', ...getAuthorizationHeader() },
            body: JSON.stringify({ query: `mutation { delete_table(t_name: "${t_name}") }` })
        });

    console.log("apiDeleteTableAsync response:", response);
    if (!response.ok) { throw "Error deleting table"; }

    const data = await response.json();
    console.log("apiDeleteTableAsync data:", data);

    return data;
}


export async function apiCreateItemAsync(t_name: string, item: any) {
    console.log("Creating item", item);

    const response = await fetch(csr_host + graphql_api_url,
        {
            method: "POST",
            headers: { 'Content-Type': 'application/json', ...getAuthorizationHeader() },
            body: JSON.stringify({ query: ` mutation { create_table_item(t_name: "${t_name}", item: ${JSON.stringify(JSON.stringify(item))}){ ... on ${t_name} { id } } }` })
        });

    console.log("apiCreateItemAsync response:", response);
    if (!response.ok) { throw "Error creating item"; }

    const data = await response.json();
    console.log("apiCreateItemAsync data:", data);

    return data;
}


export async function apiUpdateItemAsync(t_name: string, id: string, item: any) {
    console.log("Updating item", item);

    const response = await fetch(csr_host + graphql_api_url,
        {
            method: "POST",
            headers: { 'Content-Type': 'application/json', ...getAuthorizationHeader() },
            body: JSON.stringify({ query: ` mutation { update_table_item(t_name: "${t_name}", id: ${id}, item: """${JSON.stringify(item)}"""){ ... on ${t_name} { id } } }` })
        });

    console.log("apiCreateItemAsync response:", response);
    if (!response.ok) { throw "Error creating item"; }

    const data = await response.json();
    console.log("apiCreateItemAsync data:", data);

    return data;
}


export async function apiDeleteItemAsync(t_name: string, id: string) {
    const response = await fetch(csr_host + graphql_api_url,
        {
            method: "POST",
            headers: { 'Content-Type': 'application/json', ...getAuthorizationHeader() },
            body: JSON.stringify({ query: `mutation { delete_table_item(t_name: "${t_name}", id: ${id}) }` })
        })

    console.log("apiDeleteItemAsync response:", response);
    if (!response.ok) { throw "Error deleting item"; }

    const data = await response.json();
    console.log("apiDeleteItemAsync data:", data);

    return data;
}
