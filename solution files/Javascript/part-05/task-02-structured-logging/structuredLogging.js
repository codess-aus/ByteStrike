/**
 * Emit a structured audit log. Never include actual secret values.
 * @param {string} url
 * @param {number} secretsCount
 * @param {boolean} success
 * @param {string} [reason]
 */
function logMissionResult(url, secretsCount, success, reason = "") {
    console.log(
        JSON.stringify({
            timestamp: new Date().toISOString(),
            source: url,
            secrets_recovered: secretsCount,
            success,
            reason,
        })
    );
}

// Good - logs metadata only:
logMissionResult("https://raw.githubusercontent.com/...", 5, true);

module.exports = { logMissionResult };
