const fs = require("fs");

function decodeBlueprint(filename) {
    const content = fs.readFileSync(filename, "utf8");
    const pattern = /\{\* (.*?) \*\}/g;
    const matches = [...content.matchAll(pattern)];
    const secrets = matches.map((match) => match[1]);
    return secrets;
}

// Enhanced version with error handling
// If file doesn't exist, return empty array and print error message
function decodeBlueprintSafe(filename) {
    try {
        return decodeBlueprint(filename);
    } catch (err) {
        console.log(`Error: File '${filename}' not found.`);
        return [];
    }
}

// Function to format and display secrets in a professional report
// Includes header, separator lines, numbered list, and footer
function displaySecretsReport(secrets) {
    const separator = "=".repeat(50);
    console.log("\n" + separator);
    console.log("🔐 DECODED SECRETS REPORT".padEnd(50));
    console.log(separator);
    console.log(`Total secrets found: ${secrets.length}\n`);

    secrets.forEach((secret, index) => {
        const num = String(index + 1).padStart(2, " ");
        console.log(`  [${num}] ${secret}`);
    });

    console.log("\n" + separator + "\n");
}

// Use it
const secrets = decodeBlueprintSafe("blueprint-data.txt");
displaySecretsReport(secrets);

module.exports = {
    decodeBlueprint,
    decodeBlueprintSafe,
    displaySecretsReport,
};
