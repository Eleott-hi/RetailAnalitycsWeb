
// const ssr_host = "http://fastapi:8000/api/v1";
export const ssr_host = "http://localhost:8000/api/v1";
export const csr_host = "http://localhost:8000/api/v1";
export const AuthorizationHeader = { "Authorization": "" };

export function getAuthorizationHeader() {
    return { "Authorization": "Bearer " + "getBearerToken()" };
}
