import fs from "fs";

export function readBlueprint(filename) {
    return fs.readFileSync(filename, "utf8");
}

/**
 * Extract all secrets marked between {* and *} delimiters from a string.
 *
 * Searches the given content for all occurrences of the pattern {* ... *}
 * and returns the text found between each pair of markers.
 *
 * @param {string} content - The raw text to search. May contain zero or more secret markers.
 * @returns {string[]} An array of extracted secret strings in the order they appear.
 *   Returns an empty array if no markers are found.
 *
 * @example
 * extractSecrets("data {* VAULT_CODE: DELTA-7 *} and {* PROTOCOL *}");
 * // => ['VAULT_CODE: DELTA-7', 'PROTOCOL']
 */
export function extractSecrets(content) {
    return [...content.matchAll(/\{\* (.*?) \*\}/g)].map((m) => m[1]);
}

export function categorizeSecrets(secrets) {
    return secrets.reduce((acc, s) => {
        const key = s.includes(":") ? s.split(":")[0].trim() : "UNKNOWN";
        acc[key] = (acc[key] ?? 0) + 1;
        return acc;
    }, {});
}

export function decodeBlueprintSafe(filename) {
    try {
        return extractSecrets(readBlueprint(filename));
    } catch (err) {
        console.log(`Error: '${filename}' not found.`);
        return [];
    }
}
