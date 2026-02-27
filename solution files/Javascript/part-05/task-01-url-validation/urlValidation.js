const ALLOWED_HOSTS = new Set([
    "raw.githubusercontent.com",
    "league-blueprints.internal",
]);

/**
 * Throw an Error if the URL is not HTTPS or the host is not in the allowlist.
 * @param {string} url
 */
function validateUrl(url) {
    const parsed = new URL(url);
    if (parsed.protocol !== "https:")
        throw new Error(`URL must use HTTPS. Got: '${parsed.protocol}'`);
    if (!ALLOWED_HOSTS.has(parsed.hostname))
        throw new Error(`Host '${parsed.hostname}' is not in the allowed list.`);
}

module.exports = { validateUrl };
