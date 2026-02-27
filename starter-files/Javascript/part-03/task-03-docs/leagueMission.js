const fs = require("fs");

function readBlueprint(filename) {
    return fs.readFileSync(filename, "utf8");
}

function extractSecrets(content) {
    return [...content.matchAll(/\{\* (.*?) \*\}/g)].map((m) => m[1]);
}

function categorizeSecrets(secrets) {
    return secrets.reduce((acc, s) => {
        const key = s.includes(":") ? s.split(":")[0].trim() : "UNKNOWN";
        acc[key] = (acc[key] ?? 0) + 1;
        return acc;
    }, {});
}

function decodeBlueprintSafe(filename) {
    try {
        return extractSecrets(readBlueprint(filename));
    } catch (err) {
        console.log(`Error: '${filename}' not found.`);
        return [];
    }
}
