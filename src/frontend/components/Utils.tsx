
export function toCamelCase(str: string) {
    if (!str) return str;

    str = str.charAt(0).toLowerCase() + str.slice(1);
    return str
}