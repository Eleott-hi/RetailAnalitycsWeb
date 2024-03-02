
// const ssr_host = "http://fastapi:8000/api/v1";
export const ssr_host = "http://localhost:8000/api/v1";
export const csr_host = "http://localhost:8000/api/v1";
export const AuthorizationHeader = { "Authorization": "" };

const token_storage_key = 'token'

export function getTokenFromLocalStorage() {
    if (typeof window === 'undefined') return "";
    return localStorage.getItem(token_storage_key) || "";
}

export function setTokenToLocalStorage(token: string) {
    if (typeof window === 'undefined') return;
    localStorage.setItem(token_storage_key, token);
}
export function removeTokenFromLocalStorage() {
    if (typeof window === 'undefined') return;
    localStorage.removeItem(token_storage_key);
}

export function getAuthorizationHeader() {
    return { "Authorization": "Bearer " + getTokenFromLocalStorage() };
}

